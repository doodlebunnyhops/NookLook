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
        """Show stash selection or create prompt"""
        from bot.services.stash_service import StashService
        from .stash_views import StashSelectView
        
        stash_service = StashService()
        stashes = await stash_service.get_user_stashes(interaction.user.id)
        
        if not stashes:
            # No stashes - auto-create a "Default" stash and add the item
            success, message, stash_id = await stash_service.create_stash(
                interaction.user.id, "Default"
            )
            
            if success and stash_id:
                # Add the item to the newly created stash
                add_success, add_message = await stash_service.add_to_stash(
                    stash_id, interaction.user.id,
                    self.ref_table, self.ref_id, self.display_name,
                    variant_id=self.variant_id
                )
                
                if add_success:
                    embed = discord.Embed(
                        title="📦 Added to Stash!",
                        description=f"Created your first stash **Default** and added **{self.display_name}**!\n\n"
                                   "💡 **Tips:**\n"
                                   "• Use `/stash list` to view your stashes\n"
                                   "• Use `/stash create <name>` to make more stashes\n"
                                   "• You can have up to 5 stashes with 50 items each",
                        color=discord.Color.green()
                    )
                else:
                    embed = discord.Embed(
                        title="❌ Error",
                        description=f"Created stash but couldn't add item: {add_message}",
                        color=discord.Color.red()
                    )
            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Couldn't create stash: {message}",
                    color=discord.Color.red()
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Check if already in any stashes (check for this specific variant)
        stashes_with_item = await stash_service.get_stashes_containing_item(
            interaction.user.id, self.ref_table, self.ref_id, variant_id=self.variant_id
        )
        
        # If user has exactly one stash and item isn't already in it, add directly
        if len(stashes) == 1 and not stashes_with_item:
            stash = stashes[0]
            add_success, add_message = await stash_service.add_to_stash(
                stash['id'], interaction.user.id,
                self.ref_table, self.ref_id, self.display_name,
                variant_id=self.variant_id
            )
            
            if add_success:
                embed = discord.Embed(
                    title="✅ Added to Stash",
                    description=f"**{self.display_name}** has been added to **{stash['name']}**",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="❌ Couldn't Add",
                    description=add_message,
                    color=discord.Color.red()
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            # Auto-delete the confirmation after a short delay
            asyncio.create_task(self._delete_after_delay(interaction, delay=3.0))
            return
        
        # Multiple stashes or item already in some - show selection UI
        if stashes_with_item:
            stash_names = ", ".join(f"**{s['name']}**" for s in stashes_with_item)
            embed = discord.Embed(
                title="📦 Already Stashed",
                description=f"**{self.display_name}** is already in: {stash_names}\n\n"
                           "Select a different stash to add it there too:",
                color=discord.Color.blue()
            )
        else:
            embed = discord.Embed(
                title="📦 Add to Stash",
                description=f"Select a stash for **{self.display_name}**:",
                color=discord.Color.blue()
            )
        
        view = StashSelectView(
            interaction_user=interaction.user,
            stashes=stashes,
            ref_table=self.ref_table,
            ref_id=self.ref_id,
            display_name=self.display_name,
            stash_service=stash_service,
            variant_id=self.variant_id
        )
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _delete_after_delay(self, interaction: discord.Interaction, delay: float = 3.0):
        """Delete the ephemeral message after a delay"""
        try:
            await asyncio.sleep(delay)
            await interaction.delete_original_response()
        except discord.NotFound:
            pass  # Message already deleted
        except discord.HTTPException:
            pass  # Can't delete, ignore


class RefreshImagesButton(discord.ui.Button):
    """Standalone button component for refreshing images with 30-second cooldown
    
    This button can be added to any view to provide image refresh functionality.
    It automatically detects if the parent view has a create_embed() method or
    falls back to using the current message embed.
    
    The button enforces a 30-second cooldown between refreshes to prevent spam.
    """
    
    def __init__(self):
        super().__init__(
            label="🔄 Refresh Images",
            style=discord.ButtonStyle.secondary,
            custom_id="refresh_images"
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
        logger.info(f"RefreshableStaticView for {self.content_type} timed out")
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
    """Combine an existing view with Nookipedia button, refresh, and stash functionality
    
    This utility function helps compose views by adding Nookipedia link buttons,
    refresh functionality, and stash buttons to existing views.
    
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
    # If we need to add refresh but have no existing view, create a simple one
    if add_refresh and not existing_view:
        existing_view = RefreshableStaticView(content_type)
    
    if existing_view and nookipedia_url:
        # Add Nookipedia button directly to existing view (no intermediate object)
        existing_view.add_item(_create_nookipedia_button(nookipedia_url))
    elif nookipedia_url and not add_refresh:
        # Only Nookipedia button needed - use lightweight NookipediaView
        existing_view = NookipediaView(nookipedia_url)
    elif nookipedia_url and add_refresh:
        # Create view with both nookipedia and refresh
        existing_view = RefreshableStaticView(content_type)
        existing_view.add_item(_create_nookipedia_button(nookipedia_url))
    
    # Add stash button if info provided
    if existing_view and stash_info:
        existing_view.add_item(AddToStashButton(
            ref_table=stash_info['ref_table'],
            ref_id=stash_info['ref_id'],
            display_name=stash_info['display_name']
        ))
    
    return existing_view
