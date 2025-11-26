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
    content_type: str = "content"
) -> Optional[discord.ui.View]:
    """Combine an existing view with Nookipedia button and/or refresh functionality
    
    This utility function helps compose views by adding Nookipedia link buttons
    and refresh functionality to existing views. It handles various combinations:
    
    - If only nookipedia_url provided: Returns NookipediaView
    - If existing_view + nookipedia_url: Adds Nookipedia button to existing view
    - If add_refresh=True with no view: Creates RefreshableStaticView
    - If add_refresh=True + nookipedia_url: Creates RefreshableStaticView with Nookipedia
    
    Args:
        existing_view: An existing view to enhance, or None
        nookipedia_url: URL to Nookipedia article, or None
        add_refresh: Whether to add refresh functionality
        content_type: Content type description for logging (used with RefreshableStaticView)
    
    Returns:
        Combined view with requested functionality, or None if no enhancements needed
    
    Example:
        # Add both Nookipedia and refresh to an existing view
        view = VariantSelectView(item, user)
        view = get_combined_view(view, item.nookipedia_url, add_refresh=True)
    """
    # If we need to add refresh but have no existing view, create a simple one
    if add_refresh and not existing_view:
        existing_view = RefreshableStaticView(content_type)
    
    if existing_view and nookipedia_url:
        # Add Nookipedia button directly to existing view (no intermediate object)
        existing_view.add_item(_create_nookipedia_button(nookipedia_url))
        return existing_view
    elif nookipedia_url and not add_refresh:
        # Only Nookipedia button needed - use lightweight NookipediaView
        return NookipediaView(nookipedia_url)
    elif nookipedia_url and add_refresh:
        # Create view with both nookipedia and refresh
        refresh_view = RefreshableStaticView(content_type)
        refresh_view.add_item(_create_nookipedia_button(nookipedia_url))
        return refresh_view
    else:
        # Return existing view or None
        return existing_view
