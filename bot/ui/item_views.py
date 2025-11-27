"""UI views for item variant selection and display

This module contains views and select components for browsing and selecting
different variants of ACNH items (color, pattern, etc.).
"""

import discord
import logging
from typing import List
from bot.models.acnh_item import Item
from .base import UserRestrictedView, MessageTrackingMixin, TimeoutPreservingView
from .common import RefreshImagesButton, AddToStashButton

logger = logging.getLogger(__name__)


class VariantSelectView(UserRestrictedView, MessageTrackingMixin, TimeoutPreservingView):
    """View for selecting variants of an item
    
    This view allows users to browse and select different variants (colors, patterns)
    of an ACNH item. It automatically handles items with many variants by splitting
    them across multiple dropdowns.
    
    Args:
        item: The ACNH item with variants
        interaction_user: The Discord member who can interact with this view
    
    Attributes:
        selected_variant: Currently selected variant to display
        initial_variant: The original/default variant (tracked for display logic)
        user_selected_different_variant: Whether user chose a non-default variant
    """
    
    def __init__(self, item: Item, interaction_user: discord.Member, timeout: float = 120):
        super().__init__(interaction_user=interaction_user, timeout=timeout)
        self.item = item
        self.selected_variant = item.variants[0] if item.variants else None
        self.initial_variant = self.selected_variant  # Track the initial/default variant
        self.user_selected_different_variant = False  # Track if user selected a DIFFERENT variant
        self.nookipedia_url = None  # Set via add_action_buttons()
        
        # Add variant selector if item has multiple variants (row 0)
        if len(item.variants) > 1:
            self.add_variant_selector()
        
        # Note: Action buttons (Stash, Refresh, Nookipedia) are added separately
        # via add_action_buttons() to ensure correct order after variant selector
    
    def _get_variant_name(self, variant) -> str:
        """Get a display name for a variant"""
        if not variant:
            return None
        # Use display_name, color, or body_title
        if variant.display_name:
            return variant.display_name
        if variant.color1:
            if variant.color2 and variant.color2 != variant.color1:
                return f"{variant.color1} / {variant.color2}"
            return variant.color1
        if variant.body_title:
            return variant.body_title
        return None
    
    def add_action_buttons(self, nookipedia_url: str = None):
        """Add action buttons in correct order: Stash → Refresh → Nookipedia
        
        Args:
            nookipedia_url: Optional URL for Nookipedia link button
        """
        self.nookipedia_url = nookipedia_url
        
        # Determine row - row 1 if we have variant selectors, row 0 otherwise
        action_row = 1 if len(self.item.variants) > 1 else 0
        
        # 1. Add to Stash button
        variant_id = self.selected_variant.id if self.selected_variant else None
        variant_name = self._get_variant_name(self.selected_variant)
        
        self.add_item(AddToStashButton(
            ref_table='items',
            ref_id=self.item.id,
            display_name=self.item.name,
            variant_id=variant_id,
            variant_name=variant_name,
            row=action_row
        ))
        
        # 2. Refresh Images button
        self.add_item(RefreshImagesButton(row=action_row))
        
        # 3. Nookipedia link button (external, rightmost)
        if nookipedia_url:
            self.add_item(discord.ui.Button(
                label="Nookipedia",
                style=discord.ButtonStyle.link,
                url=nookipedia_url,
                emoji="📖",
                row=action_row
            ))
    
    def _rebuild_action_buttons(self):
        """Rebuild action buttons after variant change to maintain order"""
        # Remove existing action buttons (Stash, Refresh, Nookipedia link)
        buttons_to_remove = []
        for item in self.children:
            if isinstance(item, AddToStashButton):
                buttons_to_remove.append(item)
            elif isinstance(item, RefreshImagesButton):
                buttons_to_remove.append(item)
            elif isinstance(item, discord.ui.Button) and item.style == discord.ButtonStyle.link:
                buttons_to_remove.append(item)
        
        for item in buttons_to_remove:
            self.remove_item(item)
        
        # Re-add action buttons in correct order
        self.add_action_buttons(self.nookipedia_url)
    
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
                
                # Mark the default/initial variant
                if variant == self.initial_variant:
                    label += " (Default)"
                
                # Ensure we don't exceed Discord's character limit
                label = label[:100]
                
                options.append(discord.SelectOption(
                    label=label,
                    value=str(variant.id),
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
                    
                    options.append(discord.SelectOption(
                        label=label,
                        value=str(variant.id),
                    ))
                
                # Create select with page indicator
                select = VariantSelect(options, self.item, page=page+1, total_pages=total_pages)
                self.add_item(select)
    
    def create_embed(self) -> discord.Embed:
        """Create embed for the selected variant"""
        variant = self.selected_variant
        if not variant:
            return discord.Embed(title="❌ No variant selected", color=0xe74c3c)
        
        # Only show variant view if user selected a DIFFERENT variant than the initial one
        is_variant_view = self.user_selected_different_variant
        embed = self.item.to_discord_embed(variant, is_variant_view=is_variant_view)
        
        # Add footer with variant count in ACNH style
        if len(self.item.variants) > 1:
            # Remove the parentheses from the variation_pattern_summary for footer
            variant_summary = self.item.variation_pattern_summary.strip("()")
            embed.set_footer(text=f"This item has {variant_summary}")
        
        return embed
    
    async def _get_timeout_embed(self) -> discord.Embed:
        """Get the embed to display during timeout"""
        return self.create_embed()


class VariantSelect(discord.ui.Select):
    """Dropdown for selecting item variants
    
    This select component allows users to choose from different variants of an item.
    For items with many variants, multiple VariantSelect instances can be created
    to split them across pages.
    
    Args:
        options: List of variant options to display
        item: The ACNH item these variants belong to
        page: Current page number (for multi-page selects)
        total_pages: Total number of pages (for multi-page selects)
    """
    
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
            
            # Rebuild action buttons to update stash with new variant info
            self.view._rebuild_action_buttons()
            
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
    """Dropdown for selecting item color variants
    
    This select component filters variants by color. It's used in views that
    support combined filtering (e.g., color + pattern).
    
    Args:
        options: List of color options to display
        item: The ACNH item these colors belong to
    """
    
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
    """Dropdown for selecting item pattern variants
    
    This select component filters variants by pattern. It's used in views that
    support combined filtering (e.g., color + pattern).
    
    Args:
        options: List of pattern options to display
        item: The ACNH item these patterns belong to
    """
    
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
