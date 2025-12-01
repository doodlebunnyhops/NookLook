"""UI views for detailed entity information (villagers, critters)

This module contains views that display detailed information about ACNH entities
with multiple pages of information and navigation controls.
"""

import discord
import logging
from .base import UserRestrictedView, MessageTrackingMixin, RefreshableView, TimeoutPreservingView
from .common import get_combined_view
from bot.utils.localization import get_ui, translate_critter_detail

logger = logging.getLogger(__name__)


class VillagerDetailsView(UserRestrictedView, MessageTrackingMixin, RefreshableView, TimeoutPreservingView):
    """View for showing additional villager details with multi-page navigation
    
    This view provides multiple pages of villager information (About, House, Clothing, Other)
    that users can navigate between using buttons. It includes image refresh functionality
    with 30-second cooldown.
    
    Args:
        villager: The villager model with all details
        interaction_user: The Discord member who can interact with this view
        service: Business logic service for database access (used to resolve item IDs to names)
        current_view: Initial view to display ("main", "house", "clothing", or "other")
    
    Memory Management:
        This view doesn't create replacement instances, so no special cleanup needed beyond
        the automatic timeout handling.
    """
    
    def __init__(self, villager, interaction_user: discord.Member, service, current_view: str = "main"):
        super().__init__(interaction_user=interaction_user, timeout=120, refresh_cooldown=30)
        self.villager = villager
        self.service = service  # Business logic layer for database access
        self.current_view = current_view
    
    async def resolve_clothing_name(self, clothing_id_str: str) -> str:
        """Resolve clothing ID to name using the service layer
        
        Args:
            clothing_id_str: String representation of clothing ID or already a name
        
        Returns:
            Resolved clothing name or "Unknown Item (ID)" if not found
        """
        try:
            # If it's already a name (contains spaces or letters), return as-is
            if not clothing_id_str.isdigit():
                return clothing_id_str
            
            # Try to convert to int and resolve name by internal IDs
            clothing_id = int(clothing_id_str)
            
            # Try internal_id/internal_group_id first (more likely for villager references)
            clothing_name = await self.service.get_item_name_by_internal_id(clothing_id)
            
            # If that didn't work, try regular table ID as fallback
            if not clothing_name:
                clothing_name = await self.service.get_item_name_by_id(clothing_id)
            
            logger.debug(f"Resolving ID {clothing_id}: found name '{clothing_name}'")
            
            return clothing_name if clothing_name else f"Unknown Item ({clothing_id})"
        except (ValueError, TypeError) as e:
            logger.error(f"Error resolving clothing ID {clothing_id_str}: {e}")
            return clothing_id_str

    async def resolve_equipment_name(self, equipment_str: str) -> str:
        """Resolve equipment ID,variant to item name with variant
        
        Parses format like '3943,2_0' into item name with variant display
        (e.g., 'ironwood DIY workbench, Walnut')
        
        Args:
            equipment_str: Equipment string in format "internal_id,variant_indices"
        
        Returns:
            Formatted item name with variant, or "Error (input)" if parsing fails
        """
        try:
            if not equipment_str:
                return "None"
                
            # Parse internal_group_id,variant format
            if ',' in equipment_str:
                internal_id_str, variant_str = equipment_str.split(',', 1)
                internal_id = int(internal_id_str)
                
                # Parse variant indices (e.g., "2_0" -> primary=2, secondary=0)
                if '_' in variant_str:
                    primary_str, secondary_str = variant_str.split('_', 1)
                    primary_index = int(primary_str)
                    secondary_index = int(secondary_str) if secondary_str else None
                else:
                    primary_index = int(variant_str)
                    secondary_index = None
            else:
                internal_id = int(equipment_str)
                primary_index = 0
                secondary_index = None
            
            # Get item name and variant display name
            result = await self.service.get_item_variant_by_internal_group_and_indices(
                internal_id, primary_index, secondary_index
            )
            
            if result:
                item_name, variant_display = result
                if variant_display and variant_display != "Default":
                    return f"{item_name}, {variant_display}"
                else:
                    return item_name
            else:
                return f"Unknown Item ({equipment_str})"
                
        except (ValueError, Exception) as e:
            logger.error(f"Error resolving equipment name for '{equipment_str}': {e}")
            return f"Error ({equipment_str})"
    
    async def get_embed_for_view(self, view_type: str) -> discord.Embed:
        """Get the appropriate embed based on view type
        
        Args:
            view_type: One of "main", "house", "clothing", or "other"
        
        Returns:
            Discord embed for the requested view type
        """
        if view_type == "house":
            embed = discord.Embed(
                title=f"🏠 {self.villager.name}'s House",
                color=discord.Color.blue()
            )
            
            # Add wallpaper as its own field
            if self.villager.wallpaper:
                embed.add_field(
                    name="Wallpaper",
                    value=self.villager.wallpaper.title(),
                    inline=True
                )
            
            # Add flooring as its own field
            if self.villager.flooring:
                embed.add_field(
                    name="Flooring", 
                    value=self.villager.flooring.title(),
                    inline=True
                )
            
            # Add music as its own field (if available)
            if hasattr(self.villager, 'favorite_song') and self.villager.favorite_song:
                embed.add_field(
                    name="Music",
                    value=self.villager.favorite_song,
                    inline=True
                )
            
            # Format furniture list nicely
            if self.villager.furniture_name_list:
                # Split furniture items and format them
                furniture_items = [item.strip().lower() for item in self.villager.furniture_name_list.split(';') if item.strip()]
                
                if furniture_items:
                    # Group similar items and format nicely
                    formatted_furniture = []
                    item_counts = {}
                    
                    # Count occurrences of each item (case-insensitive)
                    for item in furniture_items:
                        normalized_item = item.strip().lower()
                        item_counts[normalized_item] = item_counts.get(normalized_item, 0) + 1
                    
                    # Format with counts, sorted alphabetically
                    for item, count in sorted(item_counts.items()):
                        if count > 1:
                            formatted_furniture.append(f"• {item.title()} ×{count}")
                        else:
                            formatted_furniture.append(f"• {item.title()}")
                    
                    # Split furniture into manageable chunks (max 8 items per field)
                    chunk_size = 6
                    furniture_chunks = [formatted_furniture[i:i + chunk_size] for i in range(0, len(formatted_furniture), chunk_size)]
                    
                    embed.add_field(
                        name="Furniture",
                        value="",
                        inline=False
                    )

                    # Add furniture fields (max 2 columns per row, chunk size 6)
                    for i, chunk in enumerate(furniture_chunks):
                        chunk_text = "\n".join(chunk)
                        
                        if len(furniture_chunks) == 1:
                            inline_field = False
                        else:
                            inline_field = True
                        
                        embed.add_field(
                            name="",
                            value=chunk_text,
                            inline=inline_field
                        )
                        
                        # Force new row after every 2 inline fields
                        if inline_field and (i + 1) % 2 == 0 and (i + 1) < len(furniture_chunks):
                            embed.add_field(name="", value="", inline=False)
            
            # Set description if no house details
            if not any([self.villager.wallpaper, self.villager.flooring, self.villager.furniture_name_list]):
                embed.description = "No house details available."
            
            # Set house images if available
            if hasattr(self.villager, 'house_interior_image') and self.villager.house_interior_image:
                embed.set_image(url=self.villager.house_interior_image)
            
            if self.villager.house_image:
                embed.set_thumbnail(url=self.villager.house_image)
                
        elif view_type == "clothing":
            embed = discord.Embed(
                title=f"👕 {self.villager.name}'s Style",
                color=discord.Color.green()
            )
            
            clothing_info = []
            if self.villager.default_clothing:
                clothing_name = await self.resolve_clothing_name(self.villager.default_clothing)
                clothing_info.append(f"**Default Clothing:** {clothing_name}")
            if self.villager.default_umbrella:
                umbrella_name = await self.resolve_clothing_name(self.villager.default_umbrella)
                clothing_info.append(f"**Default Umbrella:** {umbrella_name}")
            
            if clothing_info:
                embed.description = "\n".join(clothing_info)
            else:
                embed.description = "No clothing details available."
            
            # Set villager images for clothing view
            if hasattr(self.villager, 'photo_image') and self.villager.photo_image:
                embed.set_image(url=self.villager.photo_image)
            
            if hasattr(self.villager, 'icon_image') and self.villager.icon_image:
                embed.set_thumbnail(url=self.villager.icon_image)
                
        elif view_type == "other":
            embed = discord.Embed(
                title=f"🔧 {self.villager.name}'s Other Details",
                color=discord.Color.orange()
            )

            if hasattr(self.villager, 'icon_image') and self.villager.icon_image:
                embed.set_thumbnail(url=self.villager.icon_image)
            
            other_info = []
            if self.villager.diy_workbench:
                workbench_name = await self.resolve_equipment_name(self.villager.diy_workbench)
                other_info.append(f"**DIY Workbench:** {workbench_name}")
            if self.villager.kitchen_equipment:
                kitchen_name = await self.resolve_equipment_name(self.villager.kitchen_equipment)
                other_info.append(f"**Kitchen Equipment:** {kitchen_name}")
            if self.villager.version_added:
                other_info.append(f"**Version Added:** {self.villager.version_added}")
            if self.villager.subtype:
                other_info.append(f"**Subtype:** {self.villager.subtype}")
            
            if other_info:
                embed.description = "\n".join(other_info)
            else:
                embed.description = "No additional details available."
                
        else:  # main view
            embed = self.villager.to_discord_embed()
        
        return embed
    
    async def _get_refresh_embed(self) -> discord.Embed:
        """Get the embed for refresh functionality"""
        return await self.get_embed_for_view(self.current_view)
    
    async def _get_timeout_embed(self) -> discord.Embed:
        """Get the embed for timeout handling"""
        return await self.get_embed_for_view(self.current_view)
    
    @discord.ui.button(label="🏘️ About", style=discord.ButtonStyle.primary)
    async def about_villager(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show main villager info"""
        self.current_view = "main"
        embed = await self.get_embed_for_view("main")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🏠 House", style=discord.ButtonStyle.secondary)
    async def house_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show house details"""
        self.current_view = "house"
        embed = await self.get_embed_for_view("house")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="👕 Clothing", style=discord.ButtonStyle.secondary)
    async def clothing_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show clothing details"""
        self.current_view = "clothing"
        embed = await self.get_embed_for_view("clothing")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🔧 Other", style=discord.ButtonStyle.secondary)
    async def other_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show other details"""
        self.current_view = "other"
        embed = await self.get_embed_for_view("other")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🔄 Refresh Images", style=discord.ButtonStyle.secondary, row=1)
    async def refresh_images(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Refresh images in case Discord CDN fails to load them (30s cooldown)"""
        await self._handle_refresh(interaction)


class CritterAvailabilityView(UserRestrictedView, MessageTrackingMixin, RefreshableView,TimeoutPreservingView):
    """View for showing critter availability with hemisphere and month selection
    
    This view has two modes:
    1. Main mode: Shows basic critter details with "View Availability" button
    2. Availability mode: Shows detailed availability calendar with hemisphere/month selects
    
    Args:
        critter: The critter model with availability data
        interaction_user: The Discord member who can interact with this view
        show_availability: Whether to start in availability mode (default False)
    
    Memory Management:
        When switching between modes, this view creates a new instance and calls self.stop()
        on the old instance to prevent memory leaks. The message reference is transferred
        to the new view for proper timeout handling.
        
        Example mode switch:
            self.stop()  # Cancel old view's timeout
            new_view = CritterAvailabilityView(...)
            new_view.message = self.message  # Transfer message reference
            await interaction.response.edit_message(view=new_view)
    """
    
    def __init__(self, critter, interaction_user: discord.Member, show_availability: bool = False, language: str = 'en'):
        super().__init__(interaction_user=interaction_user, timeout=120, refresh_cooldown=30)
        self.critter = critter
        self.current_hemisphere = "NH"  # Default to Northern Hemisphere
        self.current_month = "jan"  # Default to January
        self.show_availability = show_availability
        self.language = language
        self.ui = get_ui(language)
        
        # Note: Buttons are added later via add_view_availability_button() or 
        # add_availability_action_buttons() to control ordering properly
    
    def get_availability_embed(self) -> discord.Embed:
        """Create embed showing availability for selected hemisphere and month"""
        embed = discord.Embed(
            title=f"🗓️ {self.critter.name} {self.ui.availability}",
            color=discord.Color.green()
        )

        if self.critter.icon_url:
            embed.set_thumbnail(url=self.critter.icon_url)
        
        # Get hemisphere display name (localized)
        hemisphere_name = self.ui.northern_hemisphere if self.current_hemisphere == "NH" else self.ui.southern_hemisphere
        
        # Get month display name (localized)
        month_name = self.ui.get_month_name(self.current_month)
        
        embed.description = f"**{self.ui.hemisphere}:** {hemisphere_name}\n**{self.ui.month_label}:** {month_name}"
        
        # Get availability for current selection
        field_name = f"{self.current_hemisphere.lower()}_{self.current_month}"
        availability = getattr(self.critter, field_name, None)
        
        if availability and availability.lower() not in ['none', 'null', '']:
            # Translate availability if translation exists
            availability = translate_critter_detail(availability, self.language) or availability
            # Available - show the time information
            embed.add_field(
                name=f"✅ {self.ui.available}", 
                value=f"**{self.ui.time_label}:** {availability}", 
                inline=False
            )
            embed.color = discord.Color.green()
        else:
            # Not available
            embed.add_field(
                name=f"❌ {self.ui.not_available_in(month_name)}", 
                value="", 
                inline=False
            )
            embed.color = discord.Color.red()
        
        # Add full year overview
        year_data = []
        for month in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]:
            field = f"{self.current_hemisphere.lower()}_{month}"
            month_avail = getattr(self.critter, field, None)
            month_short = self.ui.get_month_short(month)
            if month_avail and month_avail.lower() not in ['none', 'null', '']:
                year_data.append(f"✅ {month_short}")
            else:
                year_data.append(f"❌ {month_short}")
        
        # Split into quarters for better formatting
        quarters = [year_data[i:i+3] for i in range(0, 12, 3)]
        year_overview = "\n".join([" ".join(quarter) for quarter in quarters])
        
        embed.add_field(
            name=f"📅 {self.ui.full_year_overview} ({hemisphere_name})",
            value=f"```\n{year_overview}\n```",
            inline=False
        )
        
        # Add additional info if available (with translations)
        info_lines = []
        if self.critter.time_of_day:
            info_lines.append(f"**{self.ui.time_label}:** {translate_critter_detail(self.critter.time_of_day, self.language)}")
        if self.critter.location:
            info_lines.append(f"**{self.ui.location}:** {translate_critter_detail(self.critter.location, self.language)}")
        if self.critter.weather:
            info_lines.append(f"**{self.ui.weather}:** {translate_critter_detail(self.critter.weather, self.language)}")
        
        if info_lines:
            embed.add_field(name=f"ℹ️ {self.ui.additional_info}", value="\n".join(info_lines), inline=False)
        
        return embed
    
    async def _get_refresh_embed(self) -> discord.Embed:
        """Get the embed for refresh functionality"""
        if self.show_availability:
            return self.get_availability_embed()
        else:
            # Main critter details view
            embed = self.critter.to_discord_embed(language=self.language)
            
            # Add critter type info in footer (localized)
            critter_type = self.critter.get_type_display(self.language)
            
            footer_text = f"{critter_type}"
            if self.critter.location:
                footer_text += f" • {translate_critter_detail(self.critter.location, self.language) or self.critter.location}"
            embed.set_footer(text=footer_text)
            
            return embed
    
    async def _get_timeout_embed(self) -> discord.Embed:
        """Get the embed for timeout handling"""
        return await self._get_refresh_embed()
    
    def add_availability_controls(self):
        """Add hemisphere and month selects for availability view"""
        hemisphere_select = discord.ui.Select(
            placeholder=self.ui.choose_hemisphere,
            options=[
                discord.SelectOption(label=self.ui.northern_hemisphere, value="NH", emoji="🌎"),
                discord.SelectOption(label=self.ui.southern_hemisphere, value="SH", emoji="🌏")
            ],
            row=0
        )
        hemisphere_select.callback = self.hemisphere_callback
        
        month_select = discord.ui.Select(
            placeholder=self.ui.choose_month,
            options=[
                discord.SelectOption(label=self.ui.get_month_name("jan"), value="jan"),
                discord.SelectOption(label=self.ui.get_month_name("feb"), value="feb"),
                discord.SelectOption(label=self.ui.get_month_name("mar"), value="mar"),
                discord.SelectOption(label=self.ui.get_month_name("apr"), value="apr"),
                discord.SelectOption(label=self.ui.get_month_name("may"), value="may"),
                discord.SelectOption(label=self.ui.get_month_name("jun"), value="jun"),
                discord.SelectOption(label=self.ui.get_month_name("jul"), value="jul"),
                discord.SelectOption(label=self.ui.get_month_name("aug"), value="aug"),
                discord.SelectOption(label=self.ui.get_month_name("sep"), value="sep"),
                discord.SelectOption(label=self.ui.get_month_name("oct"), value="oct"),
                discord.SelectOption(label=self.ui.get_month_name("nov"), value="nov"),
                discord.SelectOption(label=self.ui.get_month_name("dec"), value="dec")
            ],
            row=1
        )
        month_select.callback = self.month_callback
        
        self.add_item(hemisphere_select)
        self.add_item(month_select)
        
        # Note: Action buttons (back, stash, refresh, nookipedia) are added separately
        # in add_action_buttons() to control ordering
    
    async def hemisphere_callback(self, interaction: discord.Interaction):
        """Handle hemisphere selection - interaction_check handles authorization"""
        self.current_hemisphere = interaction.data['values'][0]
        embed = self.get_availability_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def month_callback(self, interaction: discord.Interaction):
        """Handle month selection - interaction_check handles authorization"""
        self.current_month = interaction.data['values'][0]
        embed = self.get_availability_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def refresh_images_callback(self, interaction: discord.Interaction):
        """Refresh images in availability mode (30s cooldown)"""
        await self._handle_refresh(interaction)
    
    async def refresh_main_images_callback(self, interaction: discord.Interaction):
        """Refresh images for main critter view (30s cooldown)"""
        await self._handle_refresh(interaction)
    
    def add_back_button(self):
        """Add only the back to details button"""
        back_button = discord.ui.Button(label=f"📋 {self.ui.back_to_details}", style=discord.ButtonStyle.secondary, row=2)
        back_button.callback = self.back_callback
        self.add_item(back_button)
    
    def add_availability_action_buttons(self, nookipedia_url: str = None):
        """Add action buttons for availability view in correct order:
        Back to Details → Add to Stash → Refresh Images → Nookipedia
        """
        # 1. Back to Details (primary action for this view)
        back_button = discord.ui.Button(label=f"📋 {self.ui.back_to_details}", style=discord.ButtonStyle.secondary, row=2)
        back_button.callback = self.back_callback
        self.add_item(back_button)
        
        # 2. Add to Stash
        from .common import AddToStashButton
        self.add_item(AddToStashButton(
            ref_table="critters",
            ref_id=self.critter.id,
            display_name=self.critter.name,
            row=2,
            language=self.language
        ))
        
        # 3. Refresh Images
        refresh_button = discord.ui.Button(
            label=self.ui.refresh, 
            style=discord.ButtonStyle.secondary, 
            row=2
        )
        refresh_button.callback = self.refresh_images_callback
        self.add_item(refresh_button)
        
        # 4. Nookipedia Link (external, rightmost)
        if nookipedia_url:
            nookipedia_button = discord.ui.Button(
                label="Nookipedia",
                style=discord.ButtonStyle.link,
                url=nookipedia_url,
                emoji="📖",
                row=2
            )
            self.add_item(nookipedia_button)
    
    def add_view_availability_button(self):
        """Add only the view availability button (used when called from critters_commands)"""
        availability_button = discord.ui.Button(label=f"🗓️ {self.ui.view_availability}", style=discord.ButtonStyle.primary)
        availability_button.callback = self.availability_callback
        self.add_item(availability_button)
    
    def add_details_action_buttons(self, nookipedia_url: str = None):
        """Add action buttons for main details view in correct order:
        View Availability → Add to Stash → Refresh Images → Nookipedia
        """
        # 1. View Availability (primary action for this view)
        availability_button = discord.ui.Button(label=f"🗓️ {self.ui.view_availability}", style=discord.ButtonStyle.primary)
        availability_button.callback = self.availability_callback
        self.add_item(availability_button)
        
        # 2. Add to Stash
        from .common import AddToStashButton
        self.add_item(AddToStashButton(
            ref_table="critters",
            ref_id=self.critter.id,
            display_name=self.critter.name,
            language=self.language
        ))
        
        # 3. Refresh Images
        refresh_button = discord.ui.Button(
            label=self.ui.refresh, 
            style=discord.ButtonStyle.secondary
        )
        refresh_button.callback = self.refresh_main_images_callback
        self.add_item(refresh_button)
        
        # 4. Nookipedia Link (external, rightmost)
        if nookipedia_url:
            nookipedia_button = discord.ui.Button(
                label="Nookipedia",
                style=discord.ButtonStyle.link,
                url=nookipedia_url,
                emoji="📖"
            )
            self.add_item(nookipedia_button)
    
    async def back_callback(self, interaction: discord.Interaction):
        """Go back to the main critter details
        
        Memory Management: Stop current view's timeout, create new view, transfer message reference.
        This prevents the old view's timeout task from running after the view is replaced.
        """
        # Stop the current view's timeout since we're replacing it
        self.stop()
        
        embed = self.critter.to_discord_embed(language=self.language)
        
        # Add critter type info in footer (localized)
        critter_type = self.critter.get_type_display(self.language)
        
        footer_text = f"{critter_type}"
        if self.critter.location:
            footer_text += f" • {translate_critter_detail(self.critter.location, self.language)}"
        embed.set_footer(text=footer_text)
        
        # Create a new view with buttons in correct order
        view = CritterAvailabilityView(self.critter, self.interaction_user, show_availability=False, language=self.language)
        view.add_details_action_buttons(self.critter.nookipedia_url)
        
        # Transfer the message reference to the new view for timeout handling
        view.message = self.message
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def availability_callback(self, interaction: discord.Interaction):
        """Show availability interface
        
        Memory Management: Stop current view's timeout, create new view, transfer message reference.
        This prevents the old view's timeout task from running after the view is replaced.
        """
        # Stop the current view's timeout since we're replacing it
        self.stop()
        
        # Create new view with availability controls
        view = CritterAvailabilityView(self.critter, self.interaction_user, show_availability=True, language=self.language)
        view.add_availability_controls()
        
        # Add action buttons in correct order: Back → Stash → Refresh → Nookipedia
        view.add_availability_action_buttons(self.critter.nookipedia_url)
        
        # Transfer the message reference to the new view for timeout handling
        view.message = self.message
        
        embed = view.get_availability_embed()
        await interaction.response.edit_message(embed=embed, view=view)
