"""UI views for stash management and display"""

import discord
import asyncio
import logging
from typing import List, Dict, Any, Optional, Union
from .base import UserRestrictedView, MessageTrackingMixin, TimeoutPreservingView
from .common import RefreshImagesButton
from bot.models.acnh_item import Item, Critter, Recipe, Villager, Fossil, Artwork, ItemVariant
from bot.repos.acnh_items_repo import NooklookRepository

logger = logging.getLogger(__name__)


class StashSelectView(UserRestrictedView, MessageTrackingMixin, TimeoutPreservingView):
    """View for selecting a stash to add an item to"""
    
    def __init__(
        self, 
        interaction_user: discord.Member,
        stashes: List[Dict[str, Any]],
        ref_table: str,
        ref_id: int,
        display_name: str,
        stash_service,
        variant_id: int = None
    ):
        super().__init__(interaction_user=interaction_user, timeout=60)
        self.stashes = stashes
        self.ref_table = ref_table
        self.ref_id = ref_id
        self.display_name = display_name
        self.stash_service = stash_service
        self.variant_id = variant_id
        
        # Add stash selector dropdown
        if stashes:
            self._add_stash_select()
        
        # Add cancel button
        cancel_btn = discord.ui.Button(
            label="Cancel",
            style=discord.ButtonStyle.secondary,
            custom_id="cancel"
        )
        cancel_btn.callback = self._cancel
        self.add_item(cancel_btn)
    
    def _add_stash_select(self):
        """Add the stash selection dropdown"""
        options = []
        for stash in self.stashes[:25]:  # Discord limit
            item_count = stash.get('item_count', 0)
            max_items = self.stash_service.max_items
            
            options.append(discord.SelectOption(
                label=stash['name'][:100],
                value=str(stash['id']),
                description=f"{item_count}/{max_items} items",
                emoji="📦"
            ))
        
        select = discord.ui.Select(
            placeholder="Choose a stash...",
            options=options,
            custom_id="stash_select"
        )
        select.callback = self._on_stash_select
        self.add_item(select)
    
    async def _on_stash_select(self, interaction: discord.Interaction):
        """Handle stash selection"""
        stash_id = int(interaction.data['values'][0])
        
        success, message = await self.stash_service.add_to_stash(
            stash_id=stash_id,
            user_id=interaction.user.id,
            ref_table=self.ref_table,
            ref_id=self.ref_id,
            display_name=self.display_name,
            variant_id=self.variant_id
        )
        
        # Find stash name
        stash_name = next((s['name'] for s in self.stashes if s['id'] == stash_id), "stash")
        
        if success:
            embed = discord.Embed(
                title="✅ Added to Stash",
                description=f"**{self.display_name}** has been added to **{stash_name}**",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="❌ Couldn't Add",
                description=message,
                color=discord.Color.red()
            )
        
        self.stop()
        await interaction.response.edit_message(embed=embed, view=None)
        
        # Auto-delete the confirmation after a short delay
        logger.info("on_stash_select confirmation will be auto-deleted after delay")
        asyncio.create_task(self._delete_after_delay(interaction, delay=10.0))
    
    async def _cancel(self, interaction: discord.Interaction):
        """Handle cancel button"""
        self.stop()
        await interaction.response.edit_message(
            content="Cancelled.",
            embed=None,
            view=None
        )
        
        # Auto-delete the cancel message after a short delay
        asyncio.create_task(self._delete_after_delay(interaction, delay=2.0))
    
    async def _delete_after_delay(self, interaction: discord.Interaction, delay: float = 3.0):
        """Delete the ephemeral message after a delay"""
        logger.info(f"Message will be auto-deleted after {delay} seconds")
        try:
            await asyncio.sleep(delay)
            await interaction.delete_original_response()
        except discord.NotFound:
            pass  # Message already deleted
        except discord.HTTPException:
            pass  # Can't delete, ignore


class StashContentsView(UserRestrictedView, MessageTrackingMixin, TimeoutPreservingView):
    """View for displaying stash contents with detailed item view navigation
    
    Similar to SearchResultsView, this allows users to navigate through stash items
    with full detail embeds for each item.
    
    Navigation (selects, prev/next buttons) is open to everyone so others can browse
    a shared stash. Only the owner can remove items.
    
    Layout:
    - Row 0: Page selector (if >10 items)
    - Row 1: Item selector
    - Row 2: Navigation buttons (First, Prev, Next, Last)
    - Row 3: Action buttons (Remove from Stash, Refresh Images, Nookipedia)
    """
    
    def __init__(
        self,
        interaction_user: discord.Member,
        stash: Dict[str, Any],
        items: List[Dict[str, Any]],
        stash_service,
        repo: NooklookRepository = None
    ):
        super().__init__(interaction_user=interaction_user, timeout=120)
        self.stash = stash
        self.items = items
        self.stash_service = stash_service
        self.repo = repo or NooklookRepository()
        self.current_index = 0
        self._current_nookipedia_url: Optional[str] = None
        self.showing_full_list = False
        
        # Cache for loaded item details
        self._item_cache: Dict[int, Union[Item, Critter, Recipe, Villager, Fossil, Artwork]] = {}
        
        # Cache for item labels (with artwork genuine/fake info)
        self._item_labels: Dict[int, str] = {}
        
        self._add_components()
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Allow anyone to navigate, but only owner can remove items
        
        This lets others browse a shared stash without being able to modify it.
        The remove button has its own owner check as a second layer of protection.
        """
        # Check if this is the remove button - only owner can use it
        if interaction.data and interaction.data.get('custom_id') == 'remove':
            if interaction.user != self.interaction_user:
                await interaction.response.send_message(
                    "❌ Only the stash owner can remove items.",
                    ephemeral=True
                )
                return False
        
        # Allow all other interactions (navigation, selects)
        return True
    
    async def initialize(self) -> discord.Embed:
        """Initialize the view by loading the first item and building components
        
        This should be called after creating the view to properly set up the
        Nookipedia button based on the first item's URL.
        
        Returns:
            The embed for the current (first) item
        """
        # Build item labels (for artwork genuine/fake)
        await self._build_item_labels()
        # Load embed first (sets _current_nookipedia_url)
        embed = await self.create_embed()
        # Rebuild components with nookipedia URL
        self._add_components()
        return embed
    
    def _add_components(self):
        """Add all UI components"""
        self.clear_items()
        
        if not self.items:
            return
        
        # Full list mode: show simplified buttons
        if self.showing_full_list:
            self._add_full_list_buttons(row=0)
            return
        
        total = len(self.items)
        
        # Row 0: Page/range selector if more than 10 items
        has_page_select = total > 10
        if has_page_select:
            self.add_item(StashItemPageSelect(total, self.current_index))
        
        # Row 1 (or 0): Item selector for quick navigation within range
        item_row = 1 if has_page_select else 0
        self.add_item(StashItemSelect(self.items, self.current_index, row=item_row, 
                                       item_labels=self._item_labels))
        
        # Navigation buttons row
        if total > 1:
            self._add_nav_buttons(row=2 if has_page_select else 1)
        
        # Action buttons row (remove from stash)
        action_row = 3 if has_page_select else (2 if total > 1 else 1)
        self._add_action_buttons(row=action_row)
    
    def _add_nav_buttons(self, row: int):
        """Add navigation buttons"""
        total = len(self.items)
        
        # First button
        first_btn = discord.ui.Button(
            label="⏪",
            style=discord.ButtonStyle.secondary,
            custom_id="first",
            disabled=(self.current_index == 0),
            row=row
        )
        first_btn.callback = self._first_item
        self.add_item(first_btn)
        
        # Previous button
        prev_btn = discord.ui.Button(
            label="◀️ Prev",
            style=discord.ButtonStyle.primary,
            custom_id="prev",
            disabled=(self.current_index == 0),
            row=row
        )
        prev_btn.callback = self._prev_item
        self.add_item(prev_btn)
        
        # Next button
        next_btn = discord.ui.Button(
            label="Next ▶️",
            style=discord.ButtonStyle.primary,
            custom_id="next",
            disabled=(self.current_index >= total - 1),
            row=row
        )
        next_btn.callback = self._next_item
        self.add_item(next_btn)
        
        # Last button
        last_btn = discord.ui.Button(
            label="⏩",
            style=discord.ButtonStyle.secondary,
            custom_id="last",
            disabled=(self.current_index >= total - 1),
            row=row
        )
        last_btn.callback = self._last_item
        self.add_item(last_btn)
    
    def _add_action_buttons(self, row: int):
        """Add action buttons in order: Remove from Stash → Full List → TI Order → Refresh Images → Nookipedia"""
        # 1. Remove from Stash button (owner only)
        remove_btn = discord.ui.Button(
            label="🗑️ Remove from Stash",
            style=discord.ButtonStyle.danger,
            custom_id="remove",
            row=row
        )
        remove_btn.callback = self._remove_current_item
        self.add_item(remove_btn)

        # 2. Full List button (shows consolidated text list)
        if self.items:
            full_list_btn = discord.ui.Button(
                label="📝 Full List",
                style=discord.ButtonStyle.secondary,
                custom_id="full_list",
                row=row
            )
            full_list_btn.callback = self._show_full_list
            self.add_item(full_list_btn)

        # 3. Convert to TI Order button (only show if items exist)
        if self.items:
            ti_order_btn = discord.ui.Button(
                label="📋 TI Order",
                style=discord.ButtonStyle.success,
                custom_id="ti_order",
                row=row
            )
            ti_order_btn.callback = self._generate_ti_order
            self.add_item(ti_order_btn)

        # 4. Refresh Images button
        self.add_item(RefreshImagesButton(row=row))

        # 5. Nookipedia link button (added dynamically based on current item)
        # This will be updated when create_embed loads the item details
        if self._current_nookipedia_url:
            self.add_item(discord.ui.Button(
                label="Nookipedia",
                style=discord.ButtonStyle.link,
                url=self._current_nookipedia_url,
                emoji="📖",
                row=row
            ))

    def _add_full_list_buttons(self, row: int):
        """Add buttons for full list view: Back → TI Order"""
        # 1. Back button to return to detail view
        back_btn = discord.ui.Button(
            label="◀️ Back to Details",
            style=discord.ButtonStyle.primary,
            custom_id="back_to_details",
            row=row
        )
        back_btn.callback = self._back_to_detail_view
        self.add_item(back_btn)

        # 2. TI Order button
        ti_order_btn = discord.ui.Button(
            label="📋 TI Order",
            style=discord.ButtonStyle.success,
            custom_id="ti_order",
            row=row
        )
        ti_order_btn.callback = self._generate_ti_order
        self.add_item(ti_order_btn)

    async def _first_item(self, interaction: discord.Interaction):
        """Navigate to first item"""
        if self.current_index > 0:
            self.current_index = 0
            await self._update_view(interaction)
    
    async def _prev_item(self, interaction: discord.Interaction):
        """Navigate to previous item"""
        if self.current_index > 0:
            self.current_index -= 1
            await self._update_view(interaction)
    
    async def _next_item(self, interaction: discord.Interaction):
        """Navigate to next item"""
        if self.current_index < len(self.items) - 1:
            self.current_index += 1
            await self._update_view(interaction)
    
    async def _last_item(self, interaction: discord.Interaction):
        """Navigate to last item"""
        if self.current_index < len(self.items) - 1:
            self.current_index = len(self.items) - 1
            await self._update_view(interaction)
    
    async def _remove_current_item(self, interaction: discord.Interaction):
        """Remove the currently displayed item from the stash (owner only)"""
        # Double-check ownership (interaction_check should have caught this, but be safe)
        if interaction.user != self.interaction_user:
            await interaction.response.send_message(
                "❌ Only the stash owner can remove items.",
                ephemeral=True
            )
            return

        if not self.items:
            return

        current_item = self.items[self.current_index]
        removed_name = current_item['display_name']

        success, message = await self.stash_service.remove_item_by_id(
            current_item['id'],
            interaction.user.id
        )

        if success:
            # Remove from local list and cache
            self.items = [i for i in self.items if i['id'] != current_item['id']]
            if current_item['id'] in self._item_cache:
                del self._item_cache[current_item['id']]

            # Adjust current index if needed
            if self.current_index >= len(self.items) and self.items:
                self.current_index = len(self.items) - 1

            # Rebuild item labels (indices changed after removal)
            await self._build_item_labels()
            # First load embed (sets _current_nookipedia_url), then rebuild components
            embed = await self.create_embed()
            self._add_components()
            embed.set_footer(text=f"✅ Removed {removed_name} • {len(self.items)}/{self.stash_service.max_items} items")
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message(f"❌ {message}", ephemeral=True)

    async def _generate_ti_order(self, interaction: discord.Interaction):
        """Generate a Treasure Island order command from all items in the stash"""
        if not self.items:
            await interaction.response.send_message(
                "❌ Stash is empty - nothing to convert!",
                ephemeral=True
            )
            return

        # Collect hex codes and item descriptions
        hex_codes = []
        item_descriptions = []
        skipped_items = []

        for stash_item in self.items:
            detail = await self._get_item_detail(stash_item)
            if not detail:
                skipped_items.append(stash_item['display_name'])
                continue

            ti_hex = None
            item_name = stash_item['display_name']

            # Handle items with variants
            if isinstance(detail, Item):
                variant_id = stash_item.get('variant_id')
                if variant_id and detail.variants:
                    # Find the specific variant
                    variant = next((v for v in detail.variants if v.id == variant_id), None)
                    if variant and variant.ti_full_hex:
                        ti_hex = variant.ti_full_hex
                elif detail.variants:
                    # Use first/default variant
                    default_variant = detail.primary_variant
                    if default_variant and default_variant.ti_full_hex:
                        ti_hex = default_variant.ti_full_hex
            # Handle critters, recipes, fossils, artwork (they have ti_full_hex directly)
            elif hasattr(detail, 'ti_full_hex') and detail.ti_full_hex:
                ti_hex = detail.ti_full_hex

            if ti_hex:
                hex_codes.append(ti_hex)
                item_descriptions.append(f"{item_name} = {ti_hex}")
            else:
                skipped_items.append(item_name)

        if not hex_codes:
            await interaction.response.send_message(
                "❌ No items in this stash have TI hex codes available.\n"
                "This might happen with villagers or items without internal IDs.",
                ephemeral=True
            )
            return

        # Build the order command
        order_command = f"$order {' '.join(hex_codes)}"

        # Send just the command in a code block for easy copying
        await interaction.response.send_message(
            f"```\n{order_command}\n```",
            ephemeral=True
        )

    async def _show_full_list(self, interaction: discord.Interaction):
        """Switch to full list view showing consolidated items with xN for duplicates"""
        if not self.items:
            await interaction.response.send_message(
                "❌ Stash is empty!",
                ephemeral=True
            )
            return

        # Create the full list embed (now async to look up artwork details)
        embed = await self._create_full_list_embed()
        
        # Switch to full list mode and update components
        self.showing_full_list = True
        self._add_components()
        
        await interaction.response.edit_message(embed=embed, view=self)

    async def _create_full_list_embed(self) -> discord.Embed:
        """Create an embed showing the consolidated item list"""
        from collections import Counter
        
        # Build display names, checking artwork for genuine/fake status and recipes for DIY
        display_names = []
        for item in self.items:
            name = item['display_name']
            
            # For artwork, look up genuine/fake status
            if item['ref_table'] == 'artwork':
                detail = await self._get_item_detail(item)
                if detail and isinstance(detail, Artwork):
                    authenticity = "Genuine" if detail.genuine else "Fake"
                    name = f"{detail.name} ({authenticity})"
            # For recipes, add DIY indicator
            elif item['ref_table'] == 'recipes':
                name = f"{name} (DIY)"
            
            display_names.append(name)
        
        item_counts = Counter(display_names)

        # Build the list with counts
        lines = []
        for item_name, count in item_counts.items():
            if count > 1:
                lines.append(f"• {item_name} x{count}")
            else:
                lines.append(f"• {item_name}")

        stash_name = self.stash['name']
        total_items = len(self.items)
        unique_items = len(item_counts)

        embed = discord.Embed(
            title=f"📋 {stash_name} — Full List",
            color=discord.Color.blue()
        )

        # Join lines and handle Discord's 4096 char description limit
        item_list = "\n".join(lines)
        if len(item_list) > 4000:
            item_list = item_list[:3950] + "\n\n*... list truncated*"
        
        embed.description = item_list
        embed.set_footer(text=f"{total_items} items ({unique_items} unique) • {total_items}/{self.stash_service.max_items} capacity")

        return embed

    async def _back_to_detail_view(self, interaction: discord.Interaction):
        """Switch back from full list view to detail view"""
        self.showing_full_list = False
        self._add_components()
        embed = await self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    async def _update_view(self, interaction: discord.Interaction):
        """Update the view after navigation"""
        # First load the embed (which sets _current_nookipedia_url)
        embed = await self.create_embed()
        # Then rebuild components (which uses _current_nookipedia_url for Nookipedia button)
        self._add_components()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def _get_item_detail(self, stash_item: Dict[str, Any]) -> Optional[Union[Item, Critter, Recipe, Villager, Fossil, Artwork]]:
        """Fetch the full item details from the database"""
        cache_key = stash_item['id']
        
        # Check cache first
        if cache_key in self._item_cache:
            return self._item_cache[cache_key]
        
        ref_table = stash_item['ref_table']
        ref_id = stash_item['ref_id']
        
        result = None
        try:
            if ref_table == 'items':
                result = await self.repo.get_item_by_id(ref_id)
            elif ref_table == 'critters':
                result = await self.repo.get_critter_by_id(ref_id)
            elif ref_table == 'recipes':
                result = await self.repo.get_recipe_by_id(ref_id)
            elif ref_table == 'villagers':
                result = await self.repo.get_villager_by_id(ref_id)
            elif ref_table == 'fossils':
                result = await self.repo.get_fossil_by_id(ref_id)
            elif ref_table == 'artwork':
                result = await self.repo.get_artwork_by_id(ref_id)
        except Exception as e:
            logger.error(f"Failed to load item detail: {e}")
        
        # Cache the result
        if result:
            self._item_cache[cache_key] = result
        
        return result
    
    async def _build_item_labels(self):
        """Build display labels for items, including artwork genuine/fake status and recipe DIY indicator
        
        This populates self._item_labels with index -> label mappings.
        """
        self._item_labels.clear()
        
        for i, item in enumerate(self.items):
            if item['ref_table'] == 'artwork':
                detail = await self._get_item_detail(item)
                if detail and isinstance(detail, Artwork):
                    authenticity = "Genuine" if detail.genuine else "Fake"
                    self._item_labels[i] = f"{detail.name} ({authenticity})"
                else:
                    self._item_labels[i] = item['display_name']
            elif item['ref_table'] == 'recipes':
                self._item_labels[i] = f"{item['display_name']} (DIY)"
            else:
                self._item_labels[i] = item['display_name']
    
    async def create_embed(self) -> discord.Embed:
        """Create embed for current stash item with full details
        
        Also updates _current_nookipedia_url for the Nookipedia button.
        """
        if not self.items:
            self._current_nookipedia_url = None
            embed = discord.Embed(
                title=f"📦 {self.stash['name']}",
                description="*This stash is empty*\n\nUse `/lookup`, `/search`, or other commands and click **Add to Stash** to save items here!",
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"0/{self.stash_service.max_items} items")
            return embed
        
        current_item = self.items[self.current_index]
        detail = await self._get_item_detail(current_item)
        
        # Update nookipedia URL for current item
        self._current_nookipedia_url = getattr(detail, 'nookipedia_url', None) if detail else None
        
        if detail:
            # Use the item's native to_embed method for full details
            embed = detail.to_embed()
            
            # If this is an item with variants and a specific variant was stashed
            variant_id = current_item.get('variant_id')
            if variant_id and isinstance(detail, Item) and detail.variants:
                # Find the specific variant
                variant = next((v for v in detail.variants if v.id == variant_id), None)
                if variant:
                    # Update thumbnail to show the specific variant
                    if variant.image_url:
                        embed.set_thumbnail(url=variant.image_url)
                    # Add variant info to title
                    variant_name = variant.display_name
                    embed.title = f"{detail.name} ({variant_name})"
            
            # For artwork, ensure the title shows genuine/fake status
            if isinstance(detail, Artwork):
                authenticity = "Genuine" if detail.genuine else "Fake"
                embed.title = f"{detail.name} ({authenticity})"
        else:
            # Fallback if we can't load details
            emoji = self.stash_service.get_type_emoji(current_item['ref_table'])
            type_name = self.stash_service.get_type_name(current_item['ref_table'])
            
            embed = discord.Embed(
                title=f"{emoji} {current_item['display_name']}",
                description=f"*Type: {type_name}*\n\n⚠️ Could not load full details for this item.",
                color=discord.Color.orange()
            )
        
        # Override footer with stash navigation info
        footer_parts = [f"📦 {self.stash['name']}"]
        footer_parts.append(f"Item {self.current_index + 1} of {len(self.items)}")
        footer_parts.append(f"{len(self.items)}/{self.stash_service.max_items} items")
        embed.set_footer(text=" • ".join(footer_parts))
        
        return embed
    
    async def _get_timeout_embed(self) -> discord.Embed:
        return await self.create_embed()


class StashItemPageSelect(discord.ui.Select):
    """Dropdown to jump to a page range of stash items"""
    
    def __init__(self, total_items: int, current_index: int):
        # Group items into pages of 10
        page_size = 10
        total_pages = (total_items + page_size - 1) // page_size
        current_page = current_index // page_size
        
        options = []
        
        if total_pages <= 25:
            for i in range(total_pages):
                start = i * page_size + 1
                end = min((i + 1) * page_size, total_items)
                options.append(discord.SelectOption(
                    label=f"Items {start}-{end}",
                    value=str(i * page_size),
                    default=(i == current_page)
                ))
        else:
            # Strategic page selection
            pages_to_show = set()
            for i in range(min(8, total_pages)):
                pages_to_show.add(i)
            for i in range(max(0, current_page - 3), min(total_pages, current_page + 4)):
                pages_to_show.add(i)
            for i in range(max(0, total_pages - 5), total_pages):
                pages_to_show.add(i)
            
            for i in sorted(pages_to_show)[:25]:
                start = i * page_size + 1
                end = min((i + 1) * page_size, total_items)
                options.append(discord.SelectOption(
                    label=f"Items {start}-{end}",
                    value=str(i * page_size),
                    default=(i == current_page)
                ))
        
        super().__init__(
            placeholder="Jump to items...",
            options=options,
            custom_id="page_select",
            row=0
        )
    
    async def callback(self, interaction: discord.Interaction):
        view: StashContentsView = self.view
        view.current_index = int(self.values[0])
        # Load embed first (sets _current_nookipedia_url), then rebuild components
        embed = await view.create_embed()
        view._add_components()
        await interaction.response.edit_message(embed=embed, view=view)


class StashItemSelect(discord.ui.Select):
    """Dropdown to select a specific stash item to view"""
    
    def __init__(self, items: List[Dict[str, Any]], current_index: int, row: int = 0, 
                 item_labels: Dict[int, str] = None):
        """
        Args:
            items: List of stash items
            current_index: Currently selected item index
            row: Discord UI row
            item_labels: Optional dict mapping item index to display label (for artwork genuine/fake)
        """
        # Show items around current position (10 items max due to Discord limits)
        page_size = 10
        page_start = (current_index // page_size) * page_size
        page_end = min(page_start + page_size, len(items))
        
        page_items = items[page_start:page_end]
        
        options = []
        for i, item in enumerate(page_items):
            global_index = page_start + i
            # Get emoji from stash_service type mapping
            emoji_map = {
                'items': '🪑',
                'critters': '🦋', 
                'recipes': '📋',
                'villagers': '🏠',
                'fossils': '🦴',
                'artwork': '🖼️'
            }
            emoji = emoji_map.get(item['ref_table'], '📦')
            
            # Use pre-built label if available (for artwork genuine/fake), else default
            label = item_labels.get(global_index, item['display_name']) if item_labels else item['display_name']
            
            options.append(discord.SelectOption(
                label=label[:95],
                value=str(global_index),
                emoji=emoji,
                default=(global_index == current_index)
            ))
        
        super().__init__(
            placeholder="Select an item to view...",
            options=options,
            custom_id="item_select",
            row=row
        )
    
    async def callback(self, interaction: discord.Interaction):
        view: StashContentsView = self.view
        view.current_index = int(self.values[0])
        # Load embed first (sets _current_nookipedia_url), then rebuild components
        embed = await view.create_embed()
        view._add_components()
        await interaction.response.edit_message(embed=embed, view=view)


class StashListView(UserRestrictedView, MessageTrackingMixin, TimeoutPreservingView):
    """View for listing all user stashes with selection"""
    
    def __init__(
        self,
        interaction_user: discord.Member,
        stashes: List[Dict[str, Any]],
        stash_service
    ):
        super().__init__(interaction_user=interaction_user, timeout=120)
        self.stashes = stashes
        self.stash_service = stash_service
        
        if stashes:
            self._add_stash_select()
    
    def _add_stash_select(self):
        """Add stash selection dropdown"""
        options = []
        for stash in self.stashes[:25]:
            item_count = stash.get('item_count', 0)
            max_items = self.stash_service.max_items
            
            options.append(discord.SelectOption(
                label=stash['name'][:100],
                value=str(stash['id']),
                description=f"{item_count}/{max_items} items",
                emoji="📦"
            ))
        
        select = discord.ui.Select(
            placeholder="Select a stash to view...",
            options=options,
            custom_id="stash_view_select"
        )
        select.callback = self._on_stash_select
        self.add_item(select)
    
    async def _on_stash_select(self, interaction: discord.Interaction):
        """Handle stash selection - show contents"""
        stash_id = int(interaction.data['values'][0])
        
        # Get stash and items
        stash = await self.stash_service.get_stash(stash_id, interaction.user.id)
        if not stash:
            await interaction.response.send_message("❌ Stash not found", ephemeral=True)
            return
        
        items = await self.stash_service.get_stash_items(stash_id, interaction.user.id)
        
        # Create contents view
        self.stop()
        view = StashContentsView(
            interaction_user=interaction.user,
            stash=stash,
            items=items,
            stash_service=self.stash_service
        )
        
        embed = await view.create_embed()
        await interaction.response.edit_message(embed=embed, view=view)
        view.message = await interaction.original_response()
    
    def create_embed(self) -> discord.Embed:
        """Create the stash list embed"""
        embed = discord.Embed(
            title="📦 Your Stashes",
            color=discord.Color.blue()
        )
        
        if not self.stashes:
            embed.description = "*You don't have any stashes yet*\n\nUse `/stash create <name>` to create your first stash!"
            embed.set_footer(text=f"0/{self.stash_service.max_stashes} stashes")
            return embed
        
        lines = []
        for stash in self.stashes:
            item_count = stash.get('item_count', 0)
            max_items = self.stash_service.max_items
            lines.append(f"📦 **{stash['name']}** — {item_count}/{max_items} items")
        
        embed.description = "\n".join(lines)
        embed.set_footer(text=f"{len(self.stashes)}/{self.stash_service.max_stashes} stashes • Select one to view")
        
        return embed
    
    async def _get_timeout_embed(self) -> discord.Embed:
        return self.create_embed()


class ConfirmDeleteView(UserRestrictedView, MessageTrackingMixin):
    """Confirmation view for deleting a stash"""
    
    def __init__(self, interaction_user: discord.Member, stash: Dict[str, Any], stash_service):
        super().__init__(interaction_user=interaction_user, timeout=30)
        self.stash = stash
        self.stash_service = stash_service
        self.confirmed = False
        
        # Confirm button
        confirm_btn = discord.ui.Button(
            label="Delete",
            style=discord.ButtonStyle.danger,
            custom_id="confirm"
        )
        confirm_btn.callback = self._confirm
        self.add_item(confirm_btn)
        
        # Cancel button
        cancel_btn = discord.ui.Button(
            label="Cancel",
            style=discord.ButtonStyle.secondary,
            custom_id="cancel"
        )
        cancel_btn.callback = self._cancel
        self.add_item(cancel_btn)
    
    async def _confirm(self, interaction: discord.Interaction):
        """Confirm deletion"""
        success, message = await self.stash_service.delete_stash(
            self.stash['id'], 
            interaction.user.id
        )
        
        self.confirmed = True
        self.stop()
        
        if success:
            embed = discord.Embed(
                title="🗑️ Stash Deleted",
                description=f"**{self.stash['name']}** has been deleted.",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="❌ Error",
                description=message,
                color=discord.Color.red()
            )
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    async def _cancel(self, interaction: discord.Interaction):
        """Cancel deletion"""
        self.stop()
        await interaction.response.edit_message(
            content="Deletion cancelled.",
            embed=None,
            view=None
        )


class RemoveItemsView(UserRestrictedView, MessageTrackingMixin):
    """View for selecting multiple items to remove from a stash"""
    
    def __init__(self, interaction_user: discord.Member, stash: Dict[str, Any], 
                 items: List[Dict[str, Any]], stash_service):
        super().__init__(interaction_user=interaction_user, timeout=120)
        self.stash = stash
        self.items = items
        self.stash_service = stash_service
        self.selected_item_ids: set = set()
        self.current_page = 0
        self.items_per_page = 25  # Discord select limit
        
        self._add_components()
    
    @property
    def total_pages(self) -> int:
        return max(1, (len(self.items) + self.items_per_page - 1) // self.items_per_page)
    
    def _add_components(self):
        """Add select menu and buttons"""
        self.clear_items()
        
        if not self.items:
            return
        
        # Row 0: Multi-select for items on current page
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.items))
        page_items = self.items[start_idx:end_idx]
        
        options = []
        for item in page_items:
            # Get emoji for item type
            emoji_map = {
                'items': '🪑',
                'critters': '🦋',
                'recipes': '📋',
                'villagers': '🏠',
                'fossils': '🦴',
                'artwork': '🖼️'
            }
            emoji = emoji_map.get(item['ref_table'], '📦')
            
            options.append(discord.SelectOption(
                label=item['display_name'][:100],
                value=str(item['id']),
                emoji=emoji,
                default=(item['id'] in self.selected_item_ids)
            ))
        
        select = discord.ui.Select(
            placeholder=f"Select items to remove (page {self.current_page + 1}/{self.total_pages})...",
            options=options,
            min_values=0,
            max_values=len(options),
            custom_id="item_select",
            row=0
        )
        select.callback = self._on_select
        self.add_item(select)
        
        # Row 1: Page navigation (if needed)
        if self.total_pages > 1:
            prev_btn = discord.ui.Button(
                label="◀️ Prev Page",
                style=discord.ButtonStyle.secondary,
                custom_id="prev_page",
                disabled=(self.current_page == 0),
                row=1
            )
            prev_btn.callback = self._prev_page
            self.add_item(prev_btn)
            
            next_btn = discord.ui.Button(
                label="Next Page ▶️",
                style=discord.ButtonStyle.secondary,
                custom_id="next_page",
                disabled=(self.current_page >= self.total_pages - 1),
                row=1
            )
            next_btn.callback = self._next_page
            self.add_item(next_btn)
        
        # Row 2: Action buttons
        action_row = 2 if self.total_pages > 1 else 1
        
        remove_btn = discord.ui.Button(
            label=f"🗑️ Remove Selected ({len(self.selected_item_ids)})",
            style=discord.ButtonStyle.danger,
            custom_id="remove",
            disabled=(len(self.selected_item_ids) == 0),
            row=action_row
        )
        remove_btn.callback = self._remove_selected
        self.add_item(remove_btn)
        
        select_all_btn = discord.ui.Button(
            label="Select All",
            style=discord.ButtonStyle.secondary,
            custom_id="select_all",
            row=action_row
        )
        select_all_btn.callback = self._select_all
        self.add_item(select_all_btn)
        
        clear_btn = discord.ui.Button(
            label="Clear Selection",
            style=discord.ButtonStyle.secondary,
            custom_id="clear",
            disabled=(len(self.selected_item_ids) == 0),
            row=action_row
        )
        clear_btn.callback = self._clear_selection
        self.add_item(clear_btn)
        
        cancel_btn = discord.ui.Button(
            label="Cancel",
            style=discord.ButtonStyle.secondary,
            custom_id="cancel",
            row=action_row
        )
        cancel_btn.callback = self._cancel
        self.add_item(cancel_btn)
    
    async def _on_select(self, interaction: discord.Interaction):
        """Handle item selection"""
        # Get current page items to know which IDs are being toggled
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.items))
        page_items = self.items[start_idx:end_idx]
        page_item_ids = {item['id'] for item in page_items}
        
        # Remove all page items from selection first
        self.selected_item_ids -= page_item_ids
        
        # Add newly selected items
        for value in interaction.data['values']:
            self.selected_item_ids.add(int(value))
        
        self._add_components()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def _prev_page(self, interaction: discord.Interaction):
        """Go to previous page"""
        self.current_page = max(0, self.current_page - 1)
        self._add_components()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def _next_page(self, interaction: discord.Interaction):
        """Go to next page"""
        self.current_page = min(self.total_pages - 1, self.current_page + 1)
        self._add_components()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def _select_all(self, interaction: discord.Interaction):
        """Select all items"""
        self.selected_item_ids = {item['id'] for item in self.items}
        self._add_components()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def _clear_selection(self, interaction: discord.Interaction):
        """Clear all selections"""
        self.selected_item_ids.clear()
        self._add_components()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def _remove_selected(self, interaction: discord.Interaction):
        """Remove all selected items"""
        if not self.selected_item_ids:
            await interaction.response.send_message("No items selected.", ephemeral=True)
            return
        
        # Remove each selected item
        removed_count = 0
        for item_id in self.selected_item_ids:
            success, _ = await self.stash_service.remove_item_by_id(item_id, interaction.user.id)
            if success:
                removed_count += 1
        
        self.stop()
        
        embed = discord.Embed(
            title="🗑️ Items Removed",
            description=f"Removed **{removed_count}** item(s) from **{self.stash['name']}**",
            color=discord.Color.green()
        )
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    async def _cancel(self, interaction: discord.Interaction):
        """Cancel the operation"""
        self.stop()
        await interaction.response.edit_message(
            content="Cancelled.",
            embed=None,
            view=None
        )
    
    def create_embed(self) -> discord.Embed:
        """Create the embed showing selection state"""
        embed = discord.Embed(
            title=f"🗑️ Remove Items from {self.stash['name']}",
            color=discord.Color.orange()
        )
        
        # Show selected items summary
        if self.selected_item_ids:
            # Get names of selected items
            selected_names = []
            for item in self.items:
                if item['id'] in self.selected_item_ids:
                    selected_names.append(item['display_name'])
            
            # Show up to 10 selected items
            if len(selected_names) <= 10:
                items_list = "\n".join(f"• {name}" for name in selected_names)
            else:
                items_list = "\n".join(f"• {name}" for name in selected_names[:10])
                items_list += f"\n*...and {len(selected_names) - 10} more*"
            
            embed.description = f"**Selected ({len(self.selected_item_ids)}):**\n{items_list}"
        else:
            embed.description = "*No items selected*\n\nSelect items from the dropdown below to remove them."
        
        embed.set_footer(text=f"Page {self.current_page + 1}/{self.total_pages} • {len(self.items)} items total")
        
        return embed
