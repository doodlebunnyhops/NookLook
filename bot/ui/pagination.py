"""UI components for pagination views

This module contains views specifically for paginated browsing of items and critters.
For search result views, see search_views.py. For item variant views, see item_views.py.
"""

import discord
from discord.ext import commands
from typing import Dict, Any, Optional, Callable
import logging
from .base import UserRestrictedView, MessageTrackingMixin, TimeoutPreservingView
from .common import RefreshImagesButton

logger = logging.getLogger(__name__)


class BrowsePageSelect(discord.ui.Select):
    """Dropdown to jump directly to a specific page for browse views"""
    
    def __init__(self, total_pages: int, current_page: int):
        options = []
        
        if total_pages <= 25:
            for i in range(total_pages):
                options.append(discord.SelectOption(
                    label=f"Page {i + 1}",
                    value=str(i),
                    default=(i == current_page)
                ))
        else:
            # Show strategic pages
            pages_to_show = set()
            for i in range(min(8, total_pages)):
                pages_to_show.add(i)
            for i in range(max(0, current_page - 3), min(total_pages, current_page + 4)):
                pages_to_show.add(i)
            for i in range(max(0, total_pages - 5), total_pages):
                pages_to_show.add(i)
            
            for i in sorted(pages_to_show)[:25]:
                options.append(discord.SelectOption(
                    label=f"Page {i + 1}",
                    value=str(i),
                    default=(i == current_page)
                ))
        
        super().__init__(
            placeholder=f"Jump to page (1-{total_pages})...",
            options=options,
            custom_id="browse_page_select"
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Handle page selection"""
        view: PaginationView = self.view
        new_page = int(self.values[0])
        await view._update_page(interaction, new_page)


class PaginationView(UserRestrictedView, MessageTrackingMixin, TimeoutPreservingView):
    """Base view for paginated content with navigation buttons.
    
    Inherits:
        - UserRestrictedView: Restricts interactions to the original user
        - MessageTrackingMixin: Tracks the message instance for updates
        - TimeoutPreservingView: Shows preserved embed on timeout
    """
    
    def __init__(self, bot: commands.Bot, interaction_user: discord.Member, 
                 data: Dict[str, Any], format_func: Callable):
        super().__init__(timeout=120)  # 2-minute timeout for browsing
        self.bot = bot
        self.interaction_user = interaction_user
        self.data = data
        self.format_func = format_func
        self.current_page = data['pagination']['current_page']
        self.message: Optional[discord.Message] = None
        self._page_select: Optional[BrowsePageSelect] = None
        
        # Add components
        self._add_components()
    
    def _add_components(self):
        """Add all UI components"""
        total_pages = self.data['pagination']['total_pages']
        
        # Add page selector if multiple pages
        if total_pages > 1:
            self._page_select = BrowsePageSelect(total_pages, self.current_page)
            self.add_item(self._page_select)
        
        # Add navigation buttons
        self._add_navigation_buttons()
        
        # Add refresh button
        self.add_item(RefreshImagesButton())
    
    def _add_navigation_buttons(self):
        """Add navigation buttons with proper state"""
        pagination = self.data['pagination']
        
        first_btn = discord.ui.Button(
            label='⏪', style=discord.ButtonStyle.secondary, 
            custom_id='first_page', disabled=not pagination['has_previous']
        )
        first_btn.callback = self._first_page_callback
        self.add_item(first_btn)
        
        prev_btn = discord.ui.Button(
            label='◀️', style=discord.ButtonStyle.primary, 
            custom_id='prev_page', disabled=not pagination['has_previous']
        )
        prev_btn.callback = self._prev_page_callback
        self.add_item(prev_btn)
        
        next_btn = discord.ui.Button(
            label='▶️', style=discord.ButtonStyle.primary, 
            custom_id='next_page', disabled=not pagination['has_next']
        )
        next_btn.callback = self._next_page_callback
        self.add_item(next_btn)
        
        last_btn = discord.ui.Button(
            label='⏩', style=discord.ButtonStyle.secondary, 
            custom_id='last_page', disabled=not pagination['has_next']
        )
        last_btn.callback = self._last_page_callback
        self.add_item(last_btn)
    
    async def _first_page_callback(self, interaction: discord.Interaction):
        if self.data['pagination']['has_previous']:
            await self._update_page(interaction, 0)
    
    async def _prev_page_callback(self, interaction: discord.Interaction):
        if self.data['pagination']['has_previous']:
            await self._update_page(interaction, self.current_page - 1)
    
    async def _next_page_callback(self, interaction: discord.Interaction):
        if self.data['pagination']['has_next']:
            await self._update_page(interaction, self.current_page + 1)
    
    async def _last_page_callback(self, interaction: discord.Interaction):
        if self.data['pagination']['has_next']:
            await self._update_page(interaction, self.data['pagination']['total_pages'] - 1)
    
    def _update_buttons(self):
        """Update button enabled/disabled state based on pagination"""
        pagination = self.data['pagination']
        
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
    
    def _update_page_select(self):
        """Update the page select dropdown"""
        if self._page_select:
            for option in self._page_select.options:
                option.default = (int(option.value) == self.current_page)
    
    def create_embed(self) -> discord.Embed:
        """Create embed for current page"""
        return self.format_func(self.data)
    
    def _get_timeout_embed(self) -> discord.Embed:
        """Return embed to show when view times out"""
        return self.create_embed()
    
    async def _update_page(self, interaction: discord.Interaction, new_page: int):
        """Update to a new page - must be implemented by subclasses"""
        pass


class ItemsPaginationView(PaginationView):
    """Pagination view specifically for browsing items with filtering options."""
    
    def __init__(self, bot: commands.Bot, interaction_user: discord.Member, 
                 data: Dict[str, Any], service, category: str = None, 
                 color: str = None, price_range: str = None):
        self.service = service
        self.category = category
        self.color = color
        self.price_range = price_range
        
        # Format function for items
        super().__init__(bot, interaction_user, data, self._format_items_embed)
    
    def _format_items_embed(self, data: Dict[str, Any]) -> discord.Embed:
        """Format items data into an embed"""
        items = data['items']
        pagination = data['pagination']
        
        # Build title
        title_parts = ["Items"]
        if self.category:
            title_parts.append(f"({self.category})")
        if self.color:
            title_parts.append(f"[{self.color}]")
        if self.price_range:
            title_parts.append(f"Price: {self.price_range}")
        
        embed = discord.Embed(
            title=" ".join(title_parts),
            color=discord.Color.blue()
        )
        
        # Add items
        for item in items:
            name = item.get('name', 'Unknown')
            category = item.get('category', 'N/A')
            buy_price = item.get('buy_price', 'N/A')
            sell_price = item.get('sell_price', 'N/A')
            
            value = f"**Category:** {category}\n"
            value += f"**Buy:** {buy_price} | **Sell:** {sell_price}"
            
            embed.add_field(name=name, value=value, inline=False)
        
        # Add pagination footer
        embed.set_footer(
            text=f"Page {pagination['current_page'] + 1} of {pagination['total_pages']} | "
                 f"{pagination['total_items']} total items"
        )
        
        return embed
    
    async def _update_page(self, interaction: discord.Interaction, new_page: int):
        """Fetch and display new page of items"""
        await interaction.response.defer()
        
        try:
            # Fetch new page data
            self.data = await self.service.get_items_page(
                page=new_page,
                category=self.category,
                color=self.color,
                price_range=self.price_range
            )
            self.current_page = new_page
            
            # Update buttons, page select, and display
            self._update_buttons()
            self._update_page_select()
            embed = self.create_embed()
            await interaction.edit_original_response(embed=embed, view=self)
            
        except Exception as e:
            logger.error(f"Error updating items page: {e}")
            await interaction.followup.send("Failed to load page.", ephemeral=True)


class CrittersPaginationView(PaginationView):
    """Pagination view specifically for browsing critters with filtering options."""
    
    def __init__(self, bot: commands.Bot, interaction_user: discord.Member, 
                 data: Dict[str, Any], service, critter_type: str = None,
                 location: str = None, active_now: bool = False):
        self.service = service
        self.critter_type = critter_type
        self.location = location
        self.active_now = active_now
        
        # Format function for critters
        super().__init__(bot, interaction_user, data, self._format_critters_embed)
    
    def _format_critters_embed(self, data: Dict[str, Any]) -> discord.Embed:
        """Format critters data into an embed"""
        critters = data['critters']
        pagination = data['pagination']
        
        # Build title
        title_parts = ["Critters"]
        if self.critter_type:
            title_parts.append(f"({self.critter_type})")
        if self.location:
            title_parts.append(f"[{self.location}]")
        if self.active_now:
            title_parts.append("(Active Now)")
        
        embed = discord.Embed(
            title=" ".join(title_parts),
            color=discord.Color.green()
        )
        
        # Add critters
        for critter in critters:
            name = critter.get('name', 'Unknown')
            location_str = critter.get('location', 'N/A')
            price = critter.get('sell_price', 'N/A')
            
            value = f"**Location:** {location_str}\n"
            value += f"**Price:** {price}"
            
            # Add availability info if present
            if 'availability' in critter:
                avail = critter['availability']
                if avail.get('isAllDay'):
                    value += "\n**Time:** All day"
                elif avail.get('time'):
                    value += f"\n**Time:** {avail['time']}"
            
            embed.add_field(name=name, value=value, inline=False)
        
        # Add pagination footer
        embed.set_footer(
            text=f"Page {pagination['current_page'] + 1} of {pagination['total_pages']} | "
                 f"{pagination['total_items']} total critters"
        )
        
        return embed
    
    async def _update_page(self, interaction: discord.Interaction, new_page: int):
        """Fetch and display new page of critters"""
        await interaction.response.defer()
        
        try:
            # Fetch new page data
            self.data = await self.service.get_critters_page(
                page=new_page,
                critter_type=self.critter_type,
                location=self.location,
                active_now=self.active_now
            )
            self.current_page = new_page
            
            # Update buttons, page select, and display
            self._update_buttons()
            self._update_page_select()
            embed = self.create_embed()
            await interaction.edit_original_response(embed=embed, view=self)
            
        except Exception as e:
            logger.error(f"Error updating critters page: {e}")
            await interaction.followup.send("Failed to load page.", ephemeral=True)
