"""UI components for pagination and results display"""

import discord
from discord.ext import commands
from typing import List, Dict, Any, Optional, Callable, Union
import logging
from bot.models.acnh_item import Item, ItemVariant, Critter, Recipe, Villager, Fossil, Artwork

logger = logging.getLogger(__name__)

class PaginationView(discord.ui.View):
    """Generic pagination view for browsing results"""
    
    def __init__(self, bot: commands.Bot, interaction_user: discord.Member, 
                 data: Dict[str, Any], format_func: Callable):
        super().__init__(timeout=300)  # 5 minute timeout
        self.bot = bot
        self.interaction_user = interaction_user
        self.data = data
        self.format_func = format_func
        self.current_page = data['pagination']['current_page']
        
        # Update button states
        self._update_buttons()
    
    def _update_buttons(self):
        """Update button enabled/disabled state based on pagination"""
        pagination = self.data['pagination']
        
        # Find and update buttons
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if item.custom_id == 'first_page':
                    item.disabled = not pagination['has_previous']
                elif item.custom_id == 'prev_page':
                    item.disabled = not pagination['has_previous']
                elif item.custom_id == 'next_page':
                    item.disabled = not pagination['has_next']
                elif item.custom_id == 'last_page':
                    item.disabled = not pagination['has_next']
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow the original user to interact"""
        return interaction.user == self.interaction_user
    
    def create_embed(self) -> discord.Embed:
        """Create embed for current page"""
        return self.format_func(self.data)
    
    @discord.ui.button(label='⏪', style=discord.ButtonStyle.secondary, custom_id='first_page')
    async def first_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Jump to first page"""
        if self.data['pagination']['has_previous']:
            await self._update_page(interaction, 0)
    
    @discord.ui.button(label='◀️', style=discord.ButtonStyle.primary, custom_id='prev_page')
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to previous page"""
        if self.data['pagination']['has_previous']:
            new_page = self.current_page - 1
            await self._update_page(interaction, new_page)
    
    @discord.ui.button(label='▶️', style=discord.ButtonStyle.primary, custom_id='next_page')
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to next page"""
        if self.data['pagination']['has_next']:
            new_page = self.current_page + 1
            await self._update_page(interaction, new_page)
    
    @discord.ui.button(label='⏩', style=discord.ButtonStyle.secondary, custom_id='last_page')
    async def last_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Jump to last page"""
        if self.data['pagination']['has_next']:
            last_page = self.data['pagination']['total_pages'] - 1
            await self._update_page(interaction, last_page)
    
    async def _update_page(self, interaction: discord.Interaction, new_page: int):
        """Update to a new page"""
        # This should be implemented by subclasses to fetch new data
        pass
    
    async def on_timeout(self):
        """Disable all buttons when view times out"""
        for item in self.children:
            if isinstance(item, (discord.ui.Button, discord.ui.Select)):
                item.disabled = True

class ItemsPaginationView(PaginationView):
    """Pagination view specifically for browsing items"""
    
    def __init__(self, bot: commands.Bot, interaction_user: discord.Member, 
                 data: Dict[str, Any], service, category: str = None, 
                 color: str = None, price_range: str = None):
        self.service = service
        self.category = category
        self.color = color
        self.price_range = price_range
        
        super().__init__(bot, interaction_user, data, self._format_items)
    
    def _format_items(self, data: Dict[str, Any]) -> discord.Embed:
        """Format items data into an embed"""
        items = data['items']
        pagination = data['pagination']
        
        embed = discord.Embed(
            title="🏠 Items Browser",
            color=0x3498db,
            description=f"Page {pagination['current_page'] + 1} of {pagination['total_pages']}"
        )
        
        # Add filters info if any
        filters = []
        if self.category:
            filters.append(f"Category: {self.category}")
        if self.color:
            filters.append(f"Color: {self.color}")
        if self.price_range:
            filters.append(f"Price: {self.price_range}")
        
        if filters:
            embed.add_field(name="Filters", value=" | ".join(filters), inline=False)
        
        # Add items
        if items:
            items_text = []
            for i, item in enumerate(items, 1):
                page_num = pagination['current_page'] * pagination['per_page'] + i
                
                # Format price
                price_text = f"{item.buy_price:,} bells" if item.buy_price else "Not for sale"
                
                # Format variants count using ACNH-style display
                variant_text = item.variation_pattern_summary if hasattr(item, 'variation_pattern_summary') else ""
                
                items_text.append(f"`{page_num:2d}.` **{item.name}**{variant_text} - {price_text}")
            
            embed.add_field(
                name=f"📦 Items ({pagination['total_items']} total)",
                value="\n".join(items_text),
                inline=False
            )
        else:
            embed.add_field(name="📦 Items", value="No items found.", inline=False)
        
        return embed
    
    async def _update_page(self, interaction: discord.Interaction, new_page: int):
        """Update to a new page by fetching fresh data"""
        try:
            self.data = await self.service.browse_items(
                category=self.category,
                color=self.color,
                price_range=self.price_range,
                page=new_page
            )
            self.current_page = new_page
            self._update_buttons()
            
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error updating page: {str(e)}", ephemeral=True
            )

class CrittersPaginationView(PaginationView):
    """Pagination view specifically for browsing critters"""
    
    def __init__(self, bot: commands.Bot, interaction_user: discord.Member, 
                 data: Dict[str, Any], service, kind: str = None, season: str = None):
        self.service = service
        self.kind = kind
        self.season = season
        
        super().__init__(bot, interaction_user, data, self._format_critters)
    
    def _format_critters(self, data: Dict[str, Any]) -> discord.Embed:
        """Format critters data into an embed"""
        critters = data['critters']
        pagination = data['pagination']
        
        embed = discord.Embed(
            title="Critters Browser",
            color=0x2ecc71,
            description=f"Page {pagination['current_page'] + 1} of {pagination['total_pages']}"
        )
        
        # Add filters info if any
        filters = []
        if self.kind:
            filters.append(f"Type: {self.kind.title()}")
        if self.season:
            filters.append(f"Season: {self.season}")
        
        if filters:
            embed.add_field(name="Filters", value=" | ".join(filters), inline=False)
        
        # Add critters
        if critters:
            critters_text = []
            for i, critter in enumerate(critters, 1):
                page_num = pagination['current_page'] * pagination['per_page'] + i
                
                # Format price
                price_text = f"{critter.sell_nook:,} bells" if critter.sell_nook else "No value"
                
                # Format icon
                icon = "🐛" if critter.critter_type == "insect" else "🐟" if critter.critter_type == "fish" else "🦀"
                
                # Format rarity/location
                location = critter.location if hasattr(critter, 'location') and critter.location else "Unknown location"
                
                critters_text.append(f"`{page_num:2d}.` {icon} **{critter.name}** - {price_text}\n     📍 {location}")
            
            embed.add_field(
                name=f"Critters ({pagination['total_items']} total)",
                value="\n".join(critters_text),
                inline=False
            )
        else:
            embed.add_field(name="Critters", value="No critters found.", inline=False)
        
        return embed
    
    async def _update_page(self, interaction: discord.Interaction, new_page: int):
        """Update to a new page by fetching fresh data"""
        try:
            self.data = await self.service.browse_critters(
                kind=self.kind,
                season=self.season,
                page=new_page
            )
            self.current_page = new_page
            self._update_buttons()
            
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error updating page: {str(e)}", ephemeral=True
            )

class VariantSelectView(discord.ui.View):
    """View for selecting variants of an item"""
    
    def __init__(self, item: Item, interaction_user: discord.Member):
        super().__init__(timeout=300)
        self.item = item
        self.interaction_user = interaction_user
        self.selected_variant = item.variants[0] if item.variants else None
        self.initial_variant = self.selected_variant  # Track the initial/default variant
        self.user_selected_different_variant = False  # Track if user selected a DIFFERENT variant
        
        # Add variant selector if item has multiple variants
        if len(item.variants) > 1:
            self.add_variant_selector()
    
    def add_variant_selector(self):
        """Add dropdown for variant selection - handles up to 25 variants per dropdown"""
        if not self.item.variants:
            return
            
        total_variants = len(self.item.variants)
        
        # If 25 or fewer variants, use single dropdown
        if total_variants <= 25:
            options = []
            for i, variant in enumerate(self.item.variants):
                # Create a descriptive label
                label = variant.display_name or f"Variant {i+1}"
                
                # Add color info if available
                if variant.color1:
                    if label == f"Variant {i+1}":
                        label = variant.color1
                    # else:
                    #     label += f" - {variant.color1}"
                
                # Mark the default/initial variant
                if variant == self.initial_variant:
                    label += " (Default)"
                
                # Ensure we don't exceed Discord's character limit
                label = label[:100]
                
                # Create description with available info
                # desc_parts = []
                # if variant.pattern_label:
                #     desc_parts.append(f"Pattern: {variant.pattern_label}")
                # if variant.color2:
                #     desc_parts.append(f"Secondary: {variant.color2}")
                # description = " | ".join(desc_parts)[:100] if desc_parts else None
                
                options.append(discord.SelectOption(
                    label=label,
                    value=str(variant.id),
                    # description=description
                ))
            
            select = VariantSelect(options, self.item)
            self.add_item(select)
        else:
            # For more than 25 variants, split into multiple pages of 25 each
            variants_per_page = 25
            total_pages = (total_variants + variants_per_page - 1) // variants_per_page
            
            for page in range(total_pages):
                start_idx = page * variants_per_page
                end_idx = min(start_idx + variants_per_page, total_variants)
                page_variants = self.item.variants[start_idx:end_idx]
                
                options = []
                for i, variant in enumerate(page_variants):
                    variant_num = start_idx + i + 1
                    
                    # Create a descriptive label
                    label = variant.display_name or f"Variant {variant_num}"
                    
                    # Add color info if available
                    if variant.color1:
                        if label == f"Variant {variant_num}":
                            label = f"{variant_num}. {variant.color1}"
                        else:
                            label = f"{variant_num}. {label}"
                    else:
                        label = f"{variant_num}. {label}"
                    
                    # Mark the default/initial variant
                    if variant == self.initial_variant:
                        label += " (Default)"
                    
                    # Ensure we don't exceed Discord's character limit
                    label = label[:100]
                    
                    # Create description
                    # desc_parts = []
                    # if variant.pattern_label:
                    #     desc_parts.append(f"Pattern: {variant.pattern_label}")
                    # if variant.color2:
                    #     desc_parts.append(f"Secondary: {variant.color2}")
                    # description = " | ".join(desc_parts)[:100] if desc_parts else None
                    
                    options.append(discord.SelectOption(
                        label=label,
                        value=str(variant.id),
                        # description=description
                    ))
                
                # Create select with page indicator
                select = VariantSelect(options, self.item, page=page+1, total_pages=total_pages)
                self.add_item(select)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow the original user to interact"""
        return interaction.user == self.interaction_user
    
    def create_embed(self) -> discord.Embed:
        """Create embed for the selected variant"""
        variant = self.selected_variant
        if not variant:
            return discord.Embed(title="❌ No variant selected", color=0xe74c3c)
        
        # Only show variant view if user selected a DIFFERENT variant than the initial one
        is_variant_view = self.user_selected_different_variant
        return self.item.to_discord_embed(variant, is_variant_view=is_variant_view)
        
        # Add image if available
        if variant.image_url:
            embed.set_image(url=variant.image_url)
        elif self.item.image_url:
            embed.set_image(url=self.item.image_url)
        
        # Add footer with variant count in ACNH style
        if len(self.item.variants) > 1:
            # Remove the parentheses from the variation_pattern_summary for footer
            variant_summary = self.item.variation_pattern_summary.strip("()")
            embed.set_footer(text=f"This item has {variant_summary}")
        
        return embed
    
    async def on_timeout(self):
        """Disable all items when view times out"""
        for item in self.children:
            if isinstance(item, (discord.ui.Button, discord.ui.Select)):
                item.disabled = True

class VariantSelect(discord.ui.Select):
    """Dropdown for selecting item variants"""
    
    def __init__(self, options: List[discord.SelectOption], item: Item, page: int = 1, total_pages: int = 1):
        # Create placeholder text that shows page info for multi-page selectors
        if total_pages > 1:
            placeholder = f"Choose variant (Page {page}/{total_pages})..."
            custom_id = f"variant_select_page_{page}"
        else:
            placeholder = "Choose a variant..."
            custom_id = "variant_select"
            
        super().__init__(
            placeholder=placeholder,
            options=options,
            custom_id=custom_id
        )
        self.item = item
    
    async def callback(self, interaction: discord.Interaction):
        """Handle variant selection"""
        try:
            logger.debug(f"Variant selection callback triggered with values: {self.values}")
            selected_variant_id = int(self.values[0])
            logger.debug(f"Looking for variant with ID: {selected_variant_id}")
            
            # Find the selected variant
            selected_variant = None
            for variant in self.item.variants:
                logger.debug(f"Checking variant ID: {variant.id}")
                if variant.id == selected_variant_id:
                    selected_variant = variant
                    break
            
            if not selected_variant:
                logger.error(f"Variant {selected_variant_id} not found!")
                await interaction.response.send_message(
                    "❌ Variant not found!", ephemeral=True
                )
                return
            
            logger.debug(f"Selected variant: {selected_variant.variation_label or 'Unknown'}")
            
            # Update the view's selected variant
            self.view.selected_variant = selected_variant
            
            # Only mark as different variant if it's actually different from the initial one
            if selected_variant != self.view.initial_variant:
                self.view.user_selected_different_variant = True
            else:
                self.view.user_selected_different_variant = False
            
            # Create new embed and update message
            embed = self.view.create_embed()
            logger.debug("Created embed, updating message")
            await interaction.response.edit_message(embed=embed, view=self.view)
            logger.debug("Message updated successfully")
            
        except Exception as e:
            logger.error(f"Error in variant selection callback: {e}")
            try:
                await interaction.response.send_message(
                    f"❌ Error selecting variant: {str(e)}", ephemeral=True
                )
            except:
                pass

class ColorSelect(discord.ui.Select):
    """Dropdown for selecting item color variants"""
    
    def __init__(self, options: List[discord.SelectOption], item: Item):
        super().__init__(
            placeholder="Choose a color...",
            options=options,
            custom_id="color_select"
        )
        self.item = item
    
    async def callback(self, interaction: discord.Interaction):
        """Handle color selection"""
        selected_value = self.values[0]
        
        # Update the view's color filter
        self.view.selected_color = selected_value
        
        # Update display with combined filters
        embed = self.view.update_display(interaction)
        
        if embed:
            await interaction.response.edit_message(embed=embed, view=self.view)
        else:
            await interaction.response.send_message(
                "❌ No variants found with that color combination!", ephemeral=True
            )

class PatternSelect(discord.ui.Select):
    """Dropdown for selecting item pattern variants"""
    
    def __init__(self, options: List[discord.SelectOption], item: Item):
        super().__init__(
            placeholder="Choose a pattern...",
            options=options,
            custom_id="pattern_select"
        )
        self.item = item
    
    async def callback(self, interaction: discord.Interaction):
        """Handle pattern selection"""
        selected_value = self.values[0]
        
        # Update the view's pattern filter
        self.view.selected_pattern = selected_value
        
        # Update display with combined filters
        embed = self.view.update_display(interaction)
        
        if embed:
            await interaction.response.edit_message(embed=embed, view=self.view)
        else:
            await interaction.response.send_message(
                "❌ No variants found with that pattern combination!", ephemeral=True
            )

class SearchResultsView(discord.ui.View):
    """View for displaying search results across multiple content types"""
    
    def __init__(self, results: List[Any], query: str, interaction_user: discord.Member):
        super().__init__(timeout=300)
        self.results = results
        self.query = query
        self.interaction_user = interaction_user
        self.current_index = 0
        
        # Add navigation buttons if there are multiple results
        if len(results) > 1:
            self.add_navigation_buttons()
    
    def add_navigation_buttons(self):
        """Add buttons for navigating through search results"""
        if self.current_index > 0:
            prev_button = discord.ui.Button(
                label="◀️ Previous",
                style=discord.ButtonStyle.primary,
                custom_id="prev_result"
            )
            prev_button.callback = self.previous_result
            self.add_item(prev_button)
        
        if self.current_index < len(self.results) - 1:
            next_button = discord.ui.Button(
                label="Next ▶️",
                style=discord.ButtonStyle.primary,
                custom_id="next_result"
            )
            next_button.callback = self.next_result
            self.add_item(next_button)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow the original user to interact"""
        return interaction.user == self.interaction_user
    
    def create_embed(self) -> discord.Embed:
        """Create embed for current search result"""
        if not self.results:
            return discord.Embed(
                title="Search Results",
                description=f"No results found for '{self.query}'",
                color=0xe74c3c
            )
        
        result = self.results[self.current_index]
        
        # Create embed based on result type
        if isinstance(result, Item):
            embed = result.to_embed()
        elif isinstance(result, Critter):
            embed = result.to_embed()
        elif isinstance(result, Recipe):
            embed = result.to_embed()
        elif isinstance(result, Villager):
            embed = result.to_embed()
        elif isinstance(result, Fossil):
            embed = result.to_embed()
        elif isinstance(result, Artwork):
            embed = result.to_embed()
        else:
            # Fallback generic embed
            embed = discord.Embed(
                title=getattr(result, 'name', 'Unknown'),
                color=0x95a5a6
            )
        
        # Add search context to title
        embed.title = f"{embed.title}"
        
        # Add footer with result navigation
        if len(self.results) > 1:
            embed.set_footer(
                text=f"Result {self.current_index + 1} of {len(self.results)} for '{self.query}'"
            )
        else:
            embed.set_footer(text=f"Search result for '{self.query}'")
        
        return embed
    
    async def previous_result(self, interaction: discord.Interaction):
        """Navigate to previous search result"""
        if self.current_index > 0:
            self.current_index -= 1
            await self._update_result(interaction)
    
    async def next_result(self, interaction: discord.Interaction):
        """Navigate to next search result"""
        if self.current_index < len(self.results) - 1:
            self.current_index += 1
            await self._update_result(interaction)
    
    async def _update_result(self, interaction: discord.Interaction):
        """Update the display with the current result"""
        # Clear and re-add navigation buttons
        self.clear_items()
        if len(self.results) > 1:
            self.add_navigation_buttons()
        
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        """Disable all buttons when view times out"""
        for item in self.children:
            if isinstance(item, (discord.ui.Button, discord.ui.Select)):
                item.disabled = True


class PaginatedResultView(discord.ui.View):
    """View for displaying paginated list of results (like search results)"""
    
    def __init__(self, results: List[Any], embed_title: str = "Results", per_page: int = 10):
        super().__init__(timeout=300)
        self.results = results
        self.embed_title = embed_title
        self.per_page = per_page
        self.current_page = 0
        self.total_pages = max(1, (len(results) + per_page - 1) // per_page)
        
        self._update_buttons()
    
    def _update_buttons(self):
        """Update button states based on current page"""
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if item.custom_id == 'first_page':
                    item.disabled = self.current_page == 0
                elif item.custom_id == 'prev_page':
                    item.disabled = self.current_page == 0
                elif item.custom_id == 'next_page':
                    item.disabled = self.current_page >= self.total_pages - 1
                elif item.custom_id == 'last_page':
                    item.disabled = self.current_page >= self.total_pages - 1
    
    def create_page_embed(self) -> discord.Embed:
        """Create embed for current page"""
        embed = discord.Embed(
            title=self.embed_title,
            color=0x3498db
        )
        
        if not self.results:
            embed.description = "No results found."
            return embed
        
        # Calculate page boundaries
        start_idx = self.current_page * self.per_page
        end_idx = min(start_idx + self.per_page, len(self.results))
        page_items = self.results[start_idx:end_idx]
        
        # Format items for this page
        description_lines = []
        for i, item in enumerate(page_items, start=start_idx + 1):
            if hasattr(item, 'name') and hasattr(item, 'category'):
                # Create a clean, consistent format for each item
                line = f"**{i}.** {item.name}"
                if hasattr(item, 'category') and item.category:
                    line += f" *({item.category})*"
                
                # Add price info if available
                price_parts = []
                if hasattr(item, 'buy_price') and item.buy_price:
                    price_parts.append(f"Buy: {item.buy_price:,}")
                if hasattr(item, 'sell_price') and item.sell_price:
                    price_parts.append(f"Sell: {item.sell_price:,}")
                
                if price_parts:
                    line += f" - {' | '.join(price_parts)}"
                
                description_lines.append(line)
            else:
                # Fallback for unknown item types
                description_lines.append(f"**{i}.** {getattr(item, 'name', 'Unknown Item')}")
        
        embed.description = '\n'.join(description_lines)
        
        # Add pagination info
        embed.set_footer(text=f"Page {self.current_page + 1}/{self.total_pages} | {len(self.results)} total results")
        
        return embed
    
    @discord.ui.button(label='⏪', style=discord.ButtonStyle.secondary, custom_id='first_page')
    async def first_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to first page"""
        self.current_page = 0
        self._update_buttons()
        embed = self.create_page_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label='◀️', style=discord.ButtonStyle.primary, custom_id='prev_page')
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self._update_buttons()
            embed = self.create_page_embed()
            await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label='▶️', style=discord.ButtonStyle.primary, custom_id='next_page')
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to next page"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._update_buttons()
            embed = self.create_page_embed()
            await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label='⏩', style=discord.ButtonStyle.secondary, custom_id='last_page')
    async def last_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to last page"""
        self.current_page = self.total_pages - 1
        self._update_buttons()
        embed = self.create_page_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        """Disable all buttons when view times out"""
        for item in self.children:
            if isinstance(item, (discord.ui.Button, discord.ui.Select)):
                item.disabled = True