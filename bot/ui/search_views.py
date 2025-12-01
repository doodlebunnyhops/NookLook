"""UI views for search result navigation and display

This module contains views for displaying and navigating through search results,
both detailed single-result navigation and paginated list views.
"""

import discord
import logging
from typing import List, Any
from bot.models.acnh_item import Item, Critter, Recipe, Villager, Fossil, Artwork
from .base import UserRestrictedView, MessageTrackingMixin, TimeoutPreservingView
from .common import RefreshImagesButton, AddToStashButton

logger = logging.getLogger(__name__)


class ResultPageSelect(discord.ui.Select):
    """Dropdown to jump to a page/range of results"""
    
    def __init__(self, total_results: int, current_index: int, results_per_page: int = 10, language: str = 'en'):
        from bot.utils.localization import get_ui
        ui = get_ui(language)
        
        self.results_per_page = results_per_page
        total_pages = (total_results + results_per_page - 1) // results_per_page
        current_page = current_index // results_per_page
        
        options = []
        
        # Build page options (max 25 due to Discord limit)
        pages_to_show = min(total_pages, 25)
        
        for page in range(pages_to_show):
            start = page * results_per_page + 1
            end = min((page + 1) * results_per_page, total_results)
            options.append(discord.SelectOption(
                label=ui.format_results_range(start, end),
                value=str(page),
                default=(page == current_page)
            ))
        
        super().__init__(
            placeholder=ui.jump_to_range,
            options=options,
            custom_id="result_page_select",
            row=0
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Handle page selection - jump to first result on that page"""
        view: SearchResultsView = self.view
        page = int(self.values[0])
        view.current_index = page * 10  # Jump to first result of that page
        
        # Update the view
        view.clear_items()
        view._add_components()
        
        embed = view.create_embed()
        await interaction.response.edit_message(embed=embed, view=view)


class ResultItemSelect(discord.ui.Select):
    """Dropdown to jump to a specific result within the current page"""
    
    def _get_ref_table(self, result: Any) -> str:
        """Get the database table name for a result type"""
        if isinstance(result, Item):
            return 'items'
        elif isinstance(result, Critter):
            return 'critters'
        elif isinstance(result, Recipe):
            return 'recipes'
        elif isinstance(result, Villager):
            return 'villagers'
        elif isinstance(result, Fossil):
            return 'fossils'
        elif isinstance(result, Artwork):
            return 'artwork'
        return None
    
    def __init__(self, results: List[Any], current_index: int, results_per_page: int = 10, row: int = 0, language: str = 'en', localized_names: dict = None):
        from bot.utils.localization import get_ui
        ui = get_ui(language)
        localized_names = localized_names or {}
        
        current_page = current_index // results_per_page
        page_start = current_page * results_per_page
        page_end = min(page_start + results_per_page, len(results))
        
        options = []
        for i in range(page_start, page_end):
            result = results[i]
            # Use localized name if available, otherwise original name
            # Use composite key (ref_table, id) to avoid ID collisions between content types
            item_id = getattr(result, 'id', None)
            ref_table = self._get_ref_table(result) if item_id else None
            localized_name = localized_names.get((ref_table, item_id)) if ref_table and item_id else None
            original_name = getattr(result, 'name', f'Result {i + 1}')
            name = localized_name if localized_name else original_name

            #if artwork add fake/real to name
            if isinstance(result, Artwork):
                authenticity = ui.genuine if result.genuine else ui.fake
                name = f"{name} ({authenticity})"

            if len(name) > 85:
                name = name[:82] + "..."
            
            # Add type indicator and original name if different
            type_name = ui.get_type_name(type(result).__name__)
            description = f"{type_name}"
            if localized_name and localized_name != original_name:
                description += f" • {original_name}"
            elif hasattr(result, 'category') and result.category:
                description += f" • {result.category}"
            
            options.append(discord.SelectOption(
                label=f"{i + 1}. {name}",
                value=str(i),
                description=description[:100],
                default=(i == current_index)
            ))
        
        super().__init__(
            placeholder=ui.select_result,
            options=options,
            custom_id="result_item_select",
            row=row
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Handle result selection"""
        view: SearchResultsView = self.view
        view.current_index = int(self.values[0])
        
        # Update the view
        view.clear_items()
        view._add_components()
        
        embed = view.create_embed()
        await interaction.response.edit_message(embed=embed, view=view)


class SearchResultsView(UserRestrictedView, MessageTrackingMixin, TimeoutPreservingView):
    """View for displaying search results across multiple content types with navigation
    
    This view allows users to navigate through multiple search results with
    previous/next buttons. Each result is shown as a full embed with its details.
    
    Args:
        results: List of search result objects (Item, Critter, Recipe, etc.)
        query: The search query that produced these results
        interaction_user: The Discord member who can interact with this view
        language: User's preferred language for UI labels (default: 'en')
    
    Attributes:
        current_index: Index of currently displayed result (0-based)
    """
    
    def __init__(self, results: List[Any], query: str, interaction_user: discord.Member, language: str = 'en', localized_names: dict = None):
        super().__init__(interaction_user=interaction_user, timeout=120)
        self.results = results
        self.query = query
        self.current_index = 0
        self.language = language
        self.localized_names = localized_names or {}  # item_id -> localized name mapping
        
        # Add all components
        self._add_components()
    
    def _add_components(self):
        """Add all UI components (dropdowns, buttons, refresh)
        
        Layout:
        - Row 0: Page selector (if >10 results)
        - Row 1: Item selector (or row 0 if no page selector)
        - Row 2: Navigation buttons (if multiple results)
        - Row 3: Action buttons (Stash, Refresh, Nookipedia)
        
        For single results, action buttons go on row 0.
        """
        total = len(self.results)
        
        if total > 1:
            # Add page/range selector if more than one page worth of results
            has_page_select = total > 10
            if has_page_select:
                self.add_item(ResultPageSelect(total, self.current_index, language=self.language))
            
            # Add individual result selector for current page
            # Row 1 if there's a page select, row 0 if not
            item_row = 1 if has_page_select else 0
            self.add_item(ResultItemSelect(self.results, self.current_index, row=item_row, language=self.language, localized_names=self.localized_names))
            
            # Add navigation buttons on their own row
            self.add_navigation_buttons()
        
        # Add action buttons on a dedicated row (below navigation)
        self._add_action_buttons()
    
    def _get_ref_table(self, result: Any) -> str:
        """Get the database table name for a result type"""
        if isinstance(result, Item):
            return 'items'
        elif isinstance(result, Critter):
            return 'critters'
        elif isinstance(result, Recipe):
            return 'recipes'
        elif isinstance(result, Villager):
            return 'villagers'
        elif isinstance(result, Fossil):
            return 'fossils'
        elif isinstance(result, Artwork):
            return 'artwork'
        return None
    
    def _add_action_buttons(self):
        """Add action buttons (Stash, Refresh, Nookipedia) on their own row
        
        Order: Add to Stash → Refresh Images → Nookipedia Link
        """
        total = len(self.results)
        
        # Determine which row for action buttons
        # Row 3 if >10 results (page select + item select + nav)
        # Row 2 if 2-10 results (item select + nav)
        # Row 0 if single result (no nav)
        if total > 10:
            action_row = 3
        elif total > 1:
            action_row = 2
        else:
            action_row = 0
        
        current_result = self.results[self.current_index] if self.results else None
        if not current_result:
            return
        
        # Add Stash button
        ref_table = self._get_ref_table(current_result)
        if ref_table:
            self.add_item(AddToStashButton(
                ref_table=ref_table,
                ref_id=current_result.id,
                display_name=getattr(current_result, 'name', 'Unknown'),
                row=action_row,
                language=self.language
            ))
        
        # Add Refresh Images button
        self.add_item(RefreshImagesButton(row=action_row, language=self.language))
        
        # Add Nookipedia link button (external link, always last)
        nookipedia_url = getattr(current_result, 'nookipedia_url', None)
        if nookipedia_url:
            from bot.utils.localization import get_ui
            ui = get_ui(self.language)
            self.add_item(discord.ui.Button(
                label=ui.nookipedia,
                style=discord.ButtonStyle.link,
                url=nookipedia_url,
                emoji="📖",
                row=action_row
            ))
    
    def add_navigation_buttons(self):
        """Add buttons for navigating through search results"""
        from bot.utils.localization import get_ui
        ui = get_ui(self.language)
        
        total = len(self.results)
        # Use row 2 for buttons (row 0 = page select, row 1 = item select)
        button_row = 2 if total > 10 else 1
        
        # First button
        first_btn = discord.ui.Button(
            label="⏪",
            style=discord.ButtonStyle.secondary,
            custom_id="first_result",
            disabled=(self.current_index == 0),
            row=button_row
        )
        first_btn.callback = self.first_result
        self.add_item(first_btn)
        
        # Previous button
        prev_btn = discord.ui.Button(
            label=f"◀️ {ui.prev_button}",
            style=discord.ButtonStyle.primary,
            custom_id="prev_result",
            disabled=(self.current_index == 0),
            row=button_row
        )
        prev_btn.callback = self.previous_result
        self.add_item(prev_btn)
        
        # Next button
        next_btn = discord.ui.Button(
            label=f"▶️ {ui.next_button}",
            style=discord.ButtonStyle.primary,
            custom_id="next_result",
            disabled=(self.current_index >= total - 1),
            row=button_row
        )
        next_btn.callback = self.next_result
        self.add_item(next_btn)
        
        # Last button
        last_btn = discord.ui.Button(
            label="⏩",
            style=discord.ButtonStyle.secondary,
            custom_id="last_result",
            disabled=(self.current_index >= total - 1),
            row=button_row
        )
        last_btn.callback = self.last_result
        self.add_item(last_btn)
    
    def create_embed(self) -> discord.Embed:
        """Create embed for current search result"""
        from bot.utils.localization import get_ui
        ui = get_ui(self.language)
        
        if not self.results:
            return discord.Embed(
                title=ui.search_results,
                description=f"{ui.no_results} '{self.query}'",
                color=0xe74c3c
            )
        
        result = self.results[self.current_index]
        
        # Create embed based on result type
        if isinstance(result, Item):
            # Items support language parameter
            embed = result.to_discord_embed(language=self.language)
            # Update title with localized name if available (use composite key)
            localized_name = self.localized_names.get(('items', result.id))
            if localized_name and localized_name != result.name:
                embed.title = f"{localized_name} ({result.name})"
        elif isinstance(result, Critter):
            embed = result.to_embed()
        elif isinstance(result, Recipe):
            embed = result.to_embed()
        elif isinstance(result, Villager):
            embed = result.to_embed()
        elif isinstance(result, Fossil):
            embed = result.to_embed()
        elif isinstance(result, Artwork):
            embed = result.to_embed(language=self.language)
        else:
            # Fallback generic embed
            embed = discord.Embed(
                title=getattr(result, 'name', 'Unknown'),
                color=0x95a5a6
            )
        
        # Add localized footer with result navigation
        if len(self.results) > 1:
            embed.set_footer(
                text=ui.format_result_footer(self.current_index + 1, len(self.results), self.query)
            )
        else:
            embed.set_footer(text=ui.format_single_result_footer(self.query))
        
        return embed
    
    async def _get_timeout_embed(self) -> discord.Embed:
        """Get the embed to display during timeout"""
        return self.create_embed()
    
    async def first_result(self, interaction: discord.Interaction):
        """Navigate to first search result"""
        if self.current_index > 0:
            self.current_index = 0
            await self._update_result(interaction)
    
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
    
    async def last_result(self, interaction: discord.Interaction):
        """Navigate to last search result"""
        if self.current_index < len(self.results) - 1:
            self.current_index = len(self.results) - 1
            await self._update_result(interaction)
    
    async def _update_result(self, interaction: discord.Interaction):
        """Update the display with the current result"""
        # Clear and re-add all components
        self.clear_items()
        self._add_components()
        
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)


class PageSelect(discord.ui.Select):
    """Dropdown to jump directly to a specific page"""
    
    def __init__(self, total_pages: int, current_page: int):
        # Build options for each page (Discord limits to 25 options)
        options = []
        
        if total_pages <= 25:
            # Show all pages
            for i in range(total_pages):
                options.append(discord.SelectOption(
                    label=f"Page {i + 1}",
                    value=str(i),
                    default=(i == current_page)
                ))
        else:
            # Show strategic pages: first 10, current area, last 5
            pages_to_show = set()
            
            # First 8 pages
            for i in range(min(8, total_pages)):
                pages_to_show.add(i)
            
            # Pages around current
            for i in range(max(0, current_page - 3), min(total_pages, current_page + 4)):
                pages_to_show.add(i)
            
            # Last 5 pages
            for i in range(max(0, total_pages - 5), total_pages):
                pages_to_show.add(i)
            
            # Sort and limit to 25
            sorted_pages = sorted(pages_to_show)[:25]
            
            for i in sorted_pages:
                options.append(discord.SelectOption(
                    label=f"Page {i + 1}",
                    value=str(i),
                    default=(i == current_page)
                ))
        
        super().__init__(
            placeholder=f"Jump to page (1-{total_pages})...",
            options=options,
            custom_id="page_select"
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Handle page selection"""
        view: PaginatedResultView = self.view
        view.current_page = int(self.values[0])
        
        # Update the view
        view._update_buttons()
        view._update_page_select()
        
        embed = view.create_page_embed()
        await interaction.response.edit_message(embed=embed, view=view)


class PaginatedResultView(MessageTrackingMixin, TimeoutPreservingView):
    """View for displaying paginated list of results
    
    This view shows a list of results with pagination controls (first/prev/next/last).
    Unlike SearchResultsView, this shows multiple results per page in a condensed format.
    
    Args:
        results: List of result objects to display
        embed_title: Title for the embed (default "Results")
        per_page: Number of results to show per page (default 10)
    
    Attributes:
        current_page: Current page number (0-based)
        total_pages: Total number of pages
    """
    
    def __init__(self, results: List[Any], embed_title: str = "Results", per_page: int = 10, timeout: float = 120):
        super().__init__(timeout=timeout)
        self.results = results
        self.embed_title = embed_title
        self.per_page = per_page
        self.current_page = 0
        self.total_pages = max(1, (len(results) + per_page - 1) // per_page)
        self._page_select: PageSelect = None
        
        self._add_components()
    
    def _add_components(self):
        """Add all UI components"""
        # Add page selector if multiple pages
        if self.total_pages > 1:
            self._page_select = PageSelect(self.total_pages, self.current_page)
            self.add_item(self._page_select)
        
        # Add navigation buttons
        self._add_navigation_buttons()
        
        # Add refresh button
        self.add_item(RefreshImagesButton())
    
    def _add_navigation_buttons(self):
        """Add navigation buttons with proper state"""
        # First page button
        first_btn = discord.ui.Button(
            label='⏪', 
            style=discord.ButtonStyle.secondary, 
            custom_id='first_page',
            disabled=(self.current_page == 0)
        )
        first_btn.callback = self._first_page
        self.add_item(first_btn)
        
        # Previous button
        prev_btn = discord.ui.Button(
            label='◀️', 
            style=discord.ButtonStyle.primary, 
            custom_id='prev_page',
            disabled=(self.current_page == 0)
        )
        prev_btn.callback = self._previous_page
        self.add_item(prev_btn)
        
        # Next button
        next_btn = discord.ui.Button(
            label='▶️', 
            style=discord.ButtonStyle.primary, 
            custom_id='next_page',
            disabled=(self.current_page >= self.total_pages - 1)
        )
        next_btn.callback = self._next_page
        self.add_item(next_btn)
        
        # Last page button
        last_btn = discord.ui.Button(
            label='⏩', 
            style=discord.ButtonStyle.secondary, 
            custom_id='last_page',
            disabled=(self.current_page >= self.total_pages - 1)
        )
        last_btn.callback = self._last_page
        self.add_item(last_btn)
    
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
    
    def _update_page_select(self):
        """Update the page select dropdown"""
        if self._page_select and self.total_pages > 1:
            # Update the default selection
            for option in self._page_select.options:
                option.default = (int(option.value) == self.current_page)
    
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
    
    async def _get_timeout_embed(self) -> discord.Embed:
        """Get the embed to display during timeout"""
        return self.create_page_embed()
    
    async def _first_page(self, interaction: discord.Interaction):
        """Go to first page"""
        self.current_page = 0
        self._update_buttons()
        self._update_page_select()
        embed = self.create_page_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def _previous_page(self, interaction: discord.Interaction):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self._update_buttons()
            self._update_page_select()
            embed = self.create_page_embed()
            await interaction.response.edit_message(embed=embed, view=self)
    
    async def _next_page(self, interaction: discord.Interaction):
        """Go to next page"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._update_buttons()
            self._update_page_select()
            embed = self.create_page_embed()
            await interaction.response.edit_message(embed=embed, view=self)
    
    async def _last_page(self, interaction: discord.Interaction):
        """Go to last page"""
        self.current_page = self.total_pages - 1
        self._update_buttons()
        self._update_page_select()
        embed = self.create_page_embed()
        await interaction.response.edit_message(embed=embed, view=self)
