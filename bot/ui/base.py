"""Base classes and mixins for Discord UI views

This module provides reusable base classes that handle common patterns across
all Discord UI views in the bot, including user authorization, timeout handling,
refresh functionality, and message tracking.

Memory Management:
    All views automatically clean up after timeout (default 120s). When creating
    replacement view instances (e.g., mode switching), always call view.stop() on
    the old view to cancel its timeout task and prevent memory leaks:
    
    Example:
        self.stop()  # Cancel old view's timeout
        new_view = MyView(...)
        new_view.message = self.message  # Transfer message reference
        await interaction.response.edit_message(view=new_view)
"""

import discord
import logging
import time
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)


class MessageTrackingMixin:
    """Mixin that adds message reference tracking to views
    
    This allows views to update their original message during timeout or
    other lifecycle events. The message reference should be set after sending:
    
    Example:
        view = MyView()
        message = await interaction.response.send_message(view=view)
        view.message = message
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message: Optional[discord.Message] = None


class UserRestrictedView(discord.ui.View):
    """Base view that restricts interactions to a specific user
    
    This prevents other users from interacting with buttons/selects that
    were created in response to someone else's command.
    
    Args:
        interaction_user: The Discord member who can interact with this view
        timeout: Seconds before view times out (default 120)
    """
    
    def __init__(self, interaction_user: discord.Member, timeout: float = 120, *args, **kwargs):
        super().__init__(timeout=timeout, *args, **kwargs)
        self.interaction_user = interaction_user
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow the original user to interact with this view"""
        return interaction.user == self.interaction_user


class TimeoutPreservingView(discord.ui.View):
    """Base view that preserves embed state when timing out
    
    When a view times out, this base class disables all interactive components
    while keeping link buttons enabled, and updates the embed footer to inform
    users that buttons have expired.
    
    This provides a better UX than leaving buttons active after timeout or
    completely removing the view.
    
    Args:
        timeout: Seconds before view times out (default 120)
    
    Note:
        Subclasses should implement a method to generate the current embed
        (e.g., create_embed() or get_embed_for_view()) that on_timeout() can call.
    """
    
    def __init__(self, timeout: float = 120, *args, **kwargs):
        super().__init__(timeout=timeout, *args, **kwargs)
    
    async def on_timeout(self):
        """Disable interactive buttons and update embed footer on timeout"""
        # Disable all buttons and selects except link buttons
        logger.debug(f"TimeoutPreservingView timed out for {self.content_type if hasattr(self, 'content_type') else 'unknown content'}")
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                # Keep link buttons enabled (they don't need interaction handling)
                if item.style != discord.ButtonStyle.link:
                    item.disabled = True
            elif isinstance(item, discord.ui.Select):
                item.disabled = True
        
        # Try to update the message to show disabled buttons
        if hasattr(self, 'message') and self.message:
            try:
                # Get current embed - subclasses should implement this method
                embed = await self._get_timeout_embed()
                
                # Update footer to show timeout with user-friendly message
                if embed:
                    if embed.footer and embed.footer.text:
                        embed.set_footer(text=f"{embed.footer.text} | 💤 Use the command again to interact with buttons")
                    else:
                        embed.set_footer(text="💤 Buttons have expired - use the command again to interact")
                    
                    # Edit the message with disabled view
                    await self.message.edit(embed=embed, view=self)
            except Exception as e:
                # Log the error but don't crash
                logger.warning(f"Failed to update message on timeout: {e}")
    
    async def _get_timeout_embed(self) -> Optional[discord.Embed]:
        """Get the embed to display during timeout
        
        Subclasses should override this method to provide the current embed.
        This method is called by on_timeout() to preserve the view state.
        
        Returns:
            The current embed to display, or None if no embed available
        """
        # Try common method names used by subclasses
        if hasattr(self, 'create_embed'):
            return self.create_embed()
        elif hasattr(self, 'get_embed_for_view') and hasattr(self, 'current_view'):
            return await self.get_embed_for_view(self.current_view)
        elif hasattr(self, 'get_availability_embed') and hasattr(self, 'show_availability'):
            if self.show_availability:
                return self.get_availability_embed()
            elif hasattr(self, 'critter'):
                return self.critter.to_discord_embed()
        
        # Fallback: try to get from message if available
        if hasattr(self, 'message') and self.message and self.message.embeds:
            return self.message.embeds[0]
        
        return None


class RefreshableView(discord.ui.View):
    """Base view with image refresh functionality and cooldown
    
    Provides a standardized refresh button that forces Discord to re-fetch
    images from CDN, useful when Discord's CDN fails to load images initially.
    
    The refresh has a 30-second cooldown to prevent spam and includes visual
    feedback (footer update) that auto-restores after 2 seconds.
    
    Args:
        timeout: Seconds before view times out (default 120)
        refresh_cooldown: Seconds between allowed refreshes (default 30)
    
    Note:
        Subclasses should implement a method to generate the current embed
        (e.g., create_embed() or get_embed_for_view()) for refresh to work.
    """
    
    def __init__(self, timeout: float = 120, refresh_cooldown: float = 30, *args, **kwargs):
        super().__init__(timeout=timeout, *args, **kwargs)
        self.last_refresh_time: float = 0
        self.refresh_cooldown = refresh_cooldown
    
    async def _handle_refresh(self, interaction: discord.Interaction):
        """Handle refresh button interaction with cooldown and feedback
        
        Args:
            interaction: The button interaction that triggered the refresh
        """
        try:
            # Check cooldown
            current_time = time.time()
            if current_time - self.last_refresh_time < self.refresh_cooldown:
                remaining = int(self.refresh_cooldown - (current_time - self.last_refresh_time))
                await interaction.response.send_message(
                    f"Please wait {remaining} more second(s) before refreshing again.", 
                    ephemeral=True
                )
                return
            
            # Update last refresh time
            self.last_refresh_time = current_time
            
            # Get the current embed
            embed = await self._get_refresh_embed()
            
            if not embed:
                await interaction.response.send_message("❌ No content to refresh", ephemeral=True)
                return
            
            # Add a subtle indicator that images were refreshed
            original_footer = embed.footer.text if embed.footer else ""
            if "🔄 Images refreshed" not in original_footer:
                new_footer = f"{original_footer} | 🔄 Images refreshed" if original_footer else "🔄 Images refreshed"
                embed.set_footer(text=new_footer)
            
            # Edit the message with the refreshed embed to force Discord to re-fetch images
            await interaction.response.edit_message(embed=embed, view=self)
            
            # After a short delay, restore the original footer text
            await asyncio.sleep(2)
            
            # Restore original footer
            try:
                original_embed = await self._get_refresh_embed()
                if original_embed:
                    if original_footer:
                        original_embed.set_footer(text=original_footer)
                    else:
                        original_embed.set_footer(text=discord.Embed.Empty)
                    
                    if hasattr(self, 'message') and self.message:
                        await self.message.edit(embed=original_embed, view=self)
            except:
                pass  # Ignore errors if message was deleted or interaction expired
                
        except Exception as e:
            logger.error(f"Error refreshing images: {e}")
            try:
                await interaction.response.send_message("❌ Failed to refresh images", ephemeral=True)
            except:
                pass
    
    async def _get_refresh_embed(self) -> Optional[discord.Embed]:
        """Get the embed to display during refresh
        
        Subclasses should override this method or implement common embed methods.
        This method is called by _handle_refresh() to regenerate the embed.
        
        Returns:
            The current embed to display, or None if no embed available
        """
        # Try common method names used by subclasses
        if hasattr(self, 'create_embed'):
            return self.create_embed()
        elif hasattr(self, 'get_embed_for_view') and hasattr(self, 'current_view'):
            return await self.get_embed_for_view(self.current_view)
        elif hasattr(self, 'get_availability_embed'):
            return self.get_availability_embed()
        
        # Fallback: try to get from message if available
        if hasattr(self, 'message') and self.message and self.message.embeds:
            return self.message.embeds[0]
        
        return None
