"""Common UI components and utilities for Discord views

This module contains reusable UI components like refresh buttons and static views,
as well as utility functions for combining views.
"""

import discord
import asyncio
import logging
from typing import Optional
from .base import RefreshableView, MessageTrackingMixin, TimeoutPreservingView

logger = logging.getLogger(__name__)


class AddToStashButton(discord.ui.Button):
    """Button to add an item to a user's stash
    
    This button can be added to any view to allow users to save items
    to their personal stashes for later reference.
    
    Args:
        ref_table: The table type ('items', 'critters', 'recipes', etc.)
        ref_id: The ID of the item in that table
        display_name: The name to show in the stash
        variant_id: Optional variant ID for items with color/pattern variants
        variant_name: Optional variant description (e.g., "Red / Checkered")
    """
    
    def __init__(self, ref_table: str, ref_id: int, display_name: str, 
                 variant_id: int = None, variant_name: str = None, row: int = None):
        super().__init__(
            label="📦 Add to Stash",
            style=discord.ButtonStyle.secondary,
            custom_id=f"add_stash_{ref_table}_{ref_id}_{variant_id or 0}",
            row=row
        )
        self.ref_table = ref_table
        self.ref_id = ref_id
        self.variant_id = variant_id
        # Include variant in display name if provided
        if variant_name:
            self.display_name = f"{display_name} ({variant_name})"
        else:
            self.display_name = display_name
    
    async def callback(self, interaction: discord.Interaction):
        """Show quantity selection, then stash selection"""
        from bot.services.stash_service import StashService
        from .stash_views import StashSelectView
        
        stash_service = StashService()
        stashes = await stash_service.get_user_stashes(interaction.user.id)
        
        if not stashes:
            # No stashes - auto-create a "Default" stash first
            success, message, stash_id = await stash_service.create_stash(
                interaction.user.id, "Default"
            )
            
            if not success:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Couldn't create stash: {message}",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Refresh stashes list
            stashes = await stash_service.get_user_stashes(interaction.user.id)
        
        # Show quantity selection view
        view = StashQuantityView(
            interaction_user=interaction.user,
            stashes=stashes,
            ref_table=self.ref_table,
            ref_id=self.ref_id,
            display_name=self.display_name,
            stash_service=stash_service,
            variant_id=self.variant_id
        )
        
        embed = view.create_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class StashQuantityView(discord.ui.View):
    """View for selecting quantity and stash to add items to"""
    
    def __init__(self, interaction_user, stashes, ref_table, ref_id, 
                 display_name, stash_service, variant_id=None):
        super().__init__(timeout=60)
        self.interaction_user = interaction_user
        self.stashes = stashes
        self.ref_table = ref_table
        self.ref_id = ref_id
        self.display_name = display_name
        self.stash_service = stash_service
        self.variant_id = variant_id
        self.selected_quantity = 1
        self.selected_stash_id = stashes[0]['id'] if len(stashes) == 1 else None
        
        self._add_components()
    
    def _add_components(self):
        """Add quantity buttons and stash selector"""
        self.clear_items()
        
        # Row 0: Quantity buttons
        quantities = [1, 5, 10, 20, 40]
        for qty in quantities:
            btn = discord.ui.Button(
                label=str(qty),
                style=discord.ButtonStyle.primary if qty == self.selected_quantity else discord.ButtonStyle.secondary,
                custom_id=f"qty_{qty}",
                row=0
            )
            btn.callback = self._make_qty_callback(qty)
            self.add_item(btn)
        
        # Row 1: Stash selector (if multiple stashes)
        if len(self.stashes) > 1:
            options = []
            for stash in self.stashes[:25]:
                item_count = stash.get('item_count', 0)
                max_items = self.stash_service.max_items
                options.append(discord.SelectOption(
                    label=stash['name'][:100],
                    value=str(stash['id']),
                    description=f"{item_count}/{max_items} items",
                    emoji="📦",
                    default=(stash['id'] == self.selected_stash_id)
                ))
            
            select = discord.ui.Select(
                placeholder="Choose a stash...",
                options=options,
                custom_id="stash_select",
                row=1
            )
            select.callback = self._on_stash_select
            self.add_item(select)
        
        # Row 2: Confirm and Cancel buttons
        confirm_btn = discord.ui.Button(
            label="✅ Add to Stash",
            style=discord.ButtonStyle.success,
            custom_id="confirm",
            row=2,
            disabled=(self.selected_stash_id is None and len(self.stashes) > 1)
        )
        confirm_btn.callback = self._confirm
        self.add_item(confirm_btn)
        
        cancel_btn = discord.ui.Button(
            label="Cancel",
            style=discord.ButtonStyle.secondary,
            custom_id="cancel",
            row=2
        )
        cancel_btn.callback = self._cancel
        self.add_item(cancel_btn)
    
    def _make_qty_callback(self, qty: int):
        """Create a callback for quantity button"""
        async def callback(interaction: discord.Interaction):
            self.selected_quantity = qty
            self._add_components()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        return callback
    
    async def _on_stash_select(self, interaction: discord.Interaction):
        """Handle stash selection"""
        self.selected_stash_id = int(interaction.data['values'][0])
        self._add_components()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def _confirm(self, interaction: discord.Interaction):
        """Add the items to the stash"""
        stash_id = self.selected_stash_id or self.stashes[0]['id']
        stash_name = next((s['name'] for s in self.stashes if s['id'] == stash_id), "stash")
        
        # Get current item count
        current_count = await self.stash_service.get_stash_item_count(stash_id)
        max_items = self.stash_service.max_items
        available_space = max_items - current_count
        
        # Calculate how many we can actually add
        quantity_to_add = min(self.selected_quantity, available_space)
        
        if quantity_to_add <= 0:
            embed = discord.Embed(
                title="❌ Stash Full",
                description=f"**{stash_name}** is already at maximum capacity ({max_items} items).\nCreate a new stash `/stash create` to add more items. Or remove some items from this stash first with `/stash remove`.",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        
        # Add items
        success_count = 0
        for _ in range(quantity_to_add):
            success, _ = await self.stash_service.add_to_stash(
                stash_id, interaction.user.id,
                self.ref_table, self.ref_id, self.display_name,
                variant_id=self.variant_id
            )
            if success:
                success_count += 1
        
        # Build response
        if success_count == self.selected_quantity:
            # Added all requested
            if success_count == 1:
                desc = f"**{self.display_name}** has been added to **{stash_name}**"
            else:
                desc = f"**{self.display_name}** x{success_count} has been added to **{stash_name}**"
            embed = discord.Embed(
                title="✅ Added to Stash",
                description=desc,
                color=discord.Color.green()
            )
        elif success_count > 0:
            # Partial add due to capacity
            embed = discord.Embed(
                title="⚠️ Partially Added",
                description=f"Added **{self.display_name}** x{success_count} to **{stash_name}**\n\n"
                           f"Could only add {success_count} of {self.selected_quantity} requested "
                           f"(stash capacity: {max_items} items)",
                color=discord.Color.gold()
            )
        else:
            embed = discord.Embed(
                title="❌ Error",
                description="Failed to add items to stash.",
                color=discord.Color.red()
            )
        
        await interaction.response.edit_message(embed=embed, view=None)
        
        # Auto-delete after delay
        logger.info("Stash _confirm will be auto-deleted after delay")
        asyncio.create_task(self._delete_after_delay(interaction, delay=10.0))
    
    async def _cancel(self, interaction: discord.Interaction):
        """Cancel the operation"""
        await interaction.response.edit_message(content="Cancelled.", embed=None, view=None)
        logger.info("Stash _cancel will be auto-deleted after delay")
        asyncio.create_task(self._delete_after_delay(interaction, delay=5.0))
    
    async def _delete_after_delay(self, interaction: discord.Interaction, delay: float):
        """Delete the message after a delay"""
        try:
            await asyncio.sleep(delay)
            await interaction.delete_original_response()
        except:
            pass
    
    def create_embed(self) -> discord.Embed:
        """Create the quantity selection embed"""
        stash_id = self.selected_stash_id or (self.stashes[0]['id'] if len(self.stashes) == 1 else None)
        stash_name = next((s['name'] for s in self.stashes if s['id'] == stash_id), None) if stash_id else None
        
        embed = discord.Embed(
            title="📦 Add to Stash",
            color=discord.Color.blue()
        )
        
        desc_parts = [f"**Item:** {self.display_name}"]
        desc_parts.append(f"**Quantity:** {self.selected_quantity}")
        
        if stash_name:
            stash_info = next((s for s in self.stashes if s['id'] == stash_id), None)
            if stash_info:
                current = stash_info.get('item_count', 0)
                max_items = self.stash_service.max_items
                desc_parts.append(f"**Stash:** {stash_name} ({current}/{max_items} items)")
        elif len(self.stashes) > 1:
            desc_parts.append("**Stash:** *Select below*")
        
        desc_parts.append("\n💡 *Select quantity, then confirm to add to your stash!*")
        
        embed.description = "\n".join(desc_parts)
        return embed


class RefreshImagesButton(discord.ui.Button):
    """Standalone button component for refreshing images with 30-second cooldown
    
    This button can be added to any view to provide image refresh functionality.
    It automatically detects if the parent view has a create_embed() method or
    falls back to using the current message embed.
    
    The button enforces a 30-second cooldown between refreshes to prevent spam.
    
    Args:
        row: Optional row number (0-4) for button placement
    """
    
    def __init__(self, row: int = None):
        super().__init__(
            label="🔄 Refresh Images",
            style=discord.ButtonStyle.secondary,
            custom_id="refresh_images",
            row=row
        )
        self.last_refresh_time = 0
    
    async def callback(self, interaction: discord.Interaction):
        """Refresh the current view by regenerating the embed to force Discord to re-fetch images"""
        try:
            # Check cooldown (30 seconds between refreshes)
            import time
            current_time = time.time()
            if current_time - self.last_refresh_time < 30:
                remaining = int(30 - (current_time - self.last_refresh_time))
                await interaction.response.send_message(
                    f"Please wait {remaining} more second(s) before refreshing again.", 
                    ephemeral=True
                )
                return
            
            # Update last refresh time
            self.last_refresh_time = current_time
            
            # Get the current view
            view = self.view
            
            # Check if this view has a create_embed method
            if hasattr(view, 'create_embed'):
                import asyncio
                if asyncio.iscoroutinefunction(view.create_embed):
                    embed = await view.create_embed()
                else:
                    embed = view.create_embed()
            else:
                # For other views, just refresh the current embed
                embed = interaction.message.embeds[0] if interaction.message.embeds else None
                if not embed:
                    await interaction.response.send_message("❌ No embed to refresh", ephemeral=True)
                    return
            
            # Add a subtle indicator that images were refreshed
            original_footer = embed.footer.text if embed.footer else ""
            if "🔄 Images refreshed" not in original_footer:
                new_footer = f"{original_footer} | 🔄 Images refreshed" if original_footer else "🔄 Images refreshed"
                embed.set_footer(text=new_footer)
            
            # Edit the message with the refreshed embed to force Discord to re-fetch images
            await interaction.response.edit_message(embed=embed, view=view)
            
            # After a short delay, restore the original footer text
            await asyncio.sleep(2)
            
            # Restore original footer if the view still has create_embed
            try:
                if hasattr(view, 'create_embed'):
                    import asyncio
                    if asyncio.iscoroutinefunction(view.create_embed):
                        original_embed = await view.create_embed()
                    else:
                        original_embed = view.create_embed()
                    if original_footer:
                        original_embed.set_footer(text=original_footer)
                    else:
                        original_embed.set_footer(text=discord.Embed.Empty)
                    
                    # Only update if the message still exists and the view is still active
                    if hasattr(view, 'message') and view.message:
                        await view.message.edit(embed=original_embed, view=view)
            except:
                pass  # Ignore errors if message was deleted or interaction expired
            
        except Exception as e:
            logger.error(f"Error refreshing images: {e}")
            try:
                await interaction.response.send_message("❌ Failed to refresh images", ephemeral=True)
            except:
                pass


class RefreshableStaticView(MessageTrackingMixin, TimeoutPreservingView, RefreshableView):
    """Simple view with just a refresh images button for static content
    
    This view is useful for content that doesn't require user interaction beyond
    refreshing images. It has a shorter 15-second timeout since it's typically
    used for simple display purposes.
    
    Args:
        content_type: Description of the content type (for logging purposes)
    
    Example:
        view = RefreshableStaticView("recipe")
        message = await interaction.response.send_message(embed=embed, view=view)
        view.message = message
    """
    
    def __init__(self, content_type: str = "content"):
        # Use 60-second timeout to give users time to refresh if CDN is slow
        super().__init__(timeout=60, refresh_cooldown=30)
        self.content_type = content_type
        
        # Add refresh button
        self._refresh_button = discord.ui.Button(
            label="🔄 Refresh Images",
            style=discord.ButtonStyle.secondary
        )
        self._refresh_button.callback = self._refresh_callback
        self.add_item(self._refresh_button)
    
    async def _refresh_callback(self, interaction: discord.Interaction):
        """Handle refresh button click"""
        await self._handle_refresh(interaction)
    
    async def _get_refresh_embed(self) -> Optional[discord.Embed]:
        """Get the current embed from the message"""
        if self.message and self.message.embeds:
            return self.message.embeds[0]
        elif interaction := getattr(self, '_last_interaction', None):
            if interaction.message and interaction.message.embeds:
                return interaction.message.embeds[0]
        return None
    
    async def on_timeout(self):
        """Disable buttons when view times out"""
        logger.debug(f"RefreshableStaticView for {self.content_type} timed out")
        for item in self.children:
            if isinstance(item, discord.ui.Button) and item.style != discord.ButtonStyle.link:
                item.disabled = True
        
        if self.message:
            try:
                await self.message.edit(view=self)
            except:
                pass


class NookipediaView(discord.ui.View):
    """A view with a button linking to Nookipedia
    
    This view provides a simple link button to the Nookipedia article for an item.
    Link buttons don't require interaction handling and remain enabled after timeout.
    
    Args:
        nookipedia_url: URL to the Nookipedia article
    """
    
    def __init__(self, nookipedia_url: str):
        super().__init__(timeout=120)
        self.nookipedia_url = nookipedia_url
        
        # Create the Nookipedia link button
        if nookipedia_url:
            self.add_item(discord.ui.Button(
                label="Nookipedia",
                style=discord.ButtonStyle.link,
                url=nookipedia_url,
                emoji="📖"
            ))
    
    async def on_timeout(self):
        """Disable interactive items when view times out, but keep link buttons enabled"""
        # Note: NookipediaView typically only has link buttons, so this may not disable anything
        logger.debug(f"NookipediaView timed out for URL: {self.nookipedia_url}")
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if item.style != discord.ButtonStyle.link:
                    item.disabled = True
            elif isinstance(item, discord.ui.Select):
                item.disabled = True


def get_nookipedia_view(nookipedia_url: Optional[str]) -> Optional[NookipediaView]:
    """Get a Nookipedia view if URL is available, otherwise None
    
    Args:
        nookipedia_url: URL to the Nookipedia article, or None
    
    Returns:
        NookipediaView instance if URL is provided, otherwise None
    """
    if nookipedia_url:
        return NookipediaView(nookipedia_url)
    return None


def _create_nookipedia_button(nookipedia_url: str) -> discord.ui.Button:
    """Create a Nookipedia link button without creating an intermediate view"""
    return discord.ui.Button(
        label="Nookipedia",
        style=discord.ButtonStyle.link,
        url=nookipedia_url,
        emoji="📖"
    )


def get_combined_view(
    existing_view: Optional[discord.ui.View], 
    nookipedia_url: Optional[str], 
    add_refresh: bool = False, 
    content_type: str = "content",
    stash_info: Optional[dict] = None
) -> Optional[discord.ui.View]:
    """Combine an existing view with Stash, Refresh, and Nookipedia functionality
    
    This utility function helps compose views by adding stash buttons, refresh 
    functionality, and Nookipedia link buttons to existing views.
    
    Button order: Add to Stash → Refresh Images → Nookipedia (consistent across all views)
    
    Args:
        existing_view: An existing view to enhance, or None
        nookipedia_url: URL to Nookipedia article, or None
        add_refresh: Whether to add refresh functionality
        content_type: Content type description for logging (used with RefreshableStaticView)
        stash_info: Optional dict with 'ref_table', 'ref_id', 'display_name' for stash button
    
    Returns:
        Combined view with requested functionality, or None if no enhancements needed
    
    Example:
        # Add stash button along with Nookipedia and refresh
        view = get_combined_view(
            None, recipe.nookipedia_url, 
            add_refresh=True, content_type="recipe",
            stash_info={'ref_table': 'recipes', 'ref_id': recipe.id, 'display_name': recipe.name}
        )
    """
    # Determine if we need to create a view
    needs_view = add_refresh or nookipedia_url or stash_info
    
    if not needs_view:
        return existing_view
    
    # Create a new view if we need one and don't have one
    if not existing_view and (add_refresh or stash_info or nookipedia_url):
        existing_view = RefreshableStaticView(content_type)
        # Remove default refresh button - we'll add it in correct order below
        for item in existing_view.children[:]:
            if isinstance(item, discord.ui.Button) and "Refresh" in (item.label or ""):
                existing_view.remove_item(item)
    
    if existing_view:
        # Add buttons in consistent order: Stash → Refresh → Nookipedia
        
        # 1. Add stash button first
        if stash_info:
            existing_view.add_item(AddToStashButton(
                ref_table=stash_info['ref_table'],
                ref_id=stash_info['ref_id'],
                display_name=stash_info['display_name']
            ))
        
        # 2. Add refresh button second (if requested and not already present)
        if add_refresh:
            has_refresh = any(
                isinstance(item, (RefreshImagesButton, discord.ui.Button)) and 
                "Refresh" in (getattr(item, 'label', '') or "")
                for item in existing_view.children
            )
            if not has_refresh:
                existing_view.add_item(RefreshImagesButton())
        
        # 3. Add Nookipedia button last (external link, rightmost)
        if nookipedia_url:
            existing_view.add_item(_create_nookipedia_button(nookipedia_url))
    
    return existing_view
