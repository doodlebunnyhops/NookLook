from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import discord

from bot.utils.localization import get_ui, translate_critter_detail, translate_fossil_detail

@dataclass(slots=True)
class ItemVariant:
    """Represents a color/pattern variant of an item"""
    
    id: int
    item_id: int
    source_unique_id: Optional[str]
    variant_id_raw: Optional[str]
    primary_index: Optional[int]
    secondary_index: Optional[int]
    variation_label: Optional[str]
    body_title: Optional[str]
    pattern_label: Optional[str]
    pattern_title: Optional[str]
    color1: Optional[str]
    color2: Optional[str]
    body_customizable: bool
    pattern_customizable: bool
    cyrus_customizable: bool
    pattern_options: Optional[str]
    internal_id: Optional[int]
    item_hex: Optional[str]
    ti_primary: Optional[int]
    ti_secondary: Optional[int]
    ti_customize_str: Optional[str]
    ti_full_hex: Optional[str]
    image_url: Optional[str]
    image_url_alt: Optional[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ItemVariant':
        return cls(
            id=data['id'],
            item_id=data['item_id'],
            source_unique_id=data.get('source_unique_id'),
            variant_id_raw=data.get('variant_id_raw'),
            primary_index=data.get('primary_index'),
            secondary_index=data.get('secondary_index'),
            variation_label=data.get('variation_label'),
            body_title=data.get('body_title'),
            pattern_label=data.get('pattern_label'),
            pattern_title=data.get('pattern_title'),
            color1=data.get('color1'),
            color2=data.get('color2'),
            body_customizable=bool(data.get('body_customizable', 0)),
            pattern_customizable=bool(data.get('pattern_customizable', 0)),
            cyrus_customizable=bool(data.get('cyrus_customizable', 0)),
            pattern_options=data.get('pattern_options'),
            internal_id=data.get('internal_id'),
            item_hex=data.get('item_hex'),
            ti_primary=data.get('ti_primary'),
            ti_secondary=data.get('ti_secondary'),
            ti_customize_str=data.get('ti_customize_str'),
            ti_full_hex=data.get('ti_full_hex'),
            image_url=data.get('image_url'),
            image_url_alt=data.get('image_url_alt')
        )
    
    @property
    def display_name(self) -> str:
        """Get display name for this variant"""
        parts = []
        if self.variation_label:
            parts.append(self.variation_label)
        if self.pattern_label:
            parts.append(self.pattern_label)
        return " / ".join(parts) if parts else "Default"
    
    @property
    def colors(self) -> List[str]:
        """Get list of colors for this variant"""
        colors = []
        if self.color1:
            colors.append(self.color1)
        if self.color2:
            colors.append(self.color2)
        return colors

@dataclass(slots=True)
class Item:
    """Represents a base item from the items table"""
    
    id: int
    name: str
    category: str
    source_unique_id: Optional[str]
    internal_group_id: Optional[int]
    is_diy: bool
    buy_price: Optional[int]
    sell_price: Optional[int]
    hha_base: Optional[int]
    source: Optional[str]
    catalog: Optional[str]
    version_added: Optional[str]
    tag: Optional[str]
    style1: Optional[str]
    style2: Optional[str]
    label_themes: Optional[str]
    filename: Optional[str]
    image_url: Optional[str]
    nookipedia_url: Optional[str]
    extra_json: Optional[str]
    variants: List[ItemVariant] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        return cls(
            id=data['id'],
            name=data['name'],
            category=data['category'],
            source_unique_id=data.get('source_unique_id'),
            internal_group_id=data.get('internal_group_id'),
            is_diy=bool(data.get('is_diy', 0)),
            buy_price=data.get('buy_price'),
            sell_price=data.get('sell_price'),
            hha_base=data.get('hha_base'),
            source=data.get('source'),
            catalog=data.get('catalog'),
            version_added=data.get('version_added'),
            tag=data.get('tag'),
            style1=data.get('style1'),
            style2=data.get('style2'),
            label_themes=data.get('label_themes'),
            filename=data.get('filename'),
            image_url=data.get('image_url'),
            nookipedia_url=data.get('nookipedia_url'),
            extra_json=data.get('extra_json'),
            variants=[]
        )
    
    @property
    def variant_count(self) -> int:
        """Get number of variants for this item"""
        return len(self.variants)
    
    @property
    def has_variants(self) -> bool:
        """Check if item has multiple variants"""
        return self.variant_count > 1
    
    @property
    def variation_pattern_summary(self) -> str:
        """Get ACNH-style variation and pattern count summary"""
        if not self.variants or len(self.variants) <= 1:
            return ""
        
        # Count unique variations and patterns based on ACNH data structure
        variations = set()
        patterns = set()
        
        for variant in self.variants:
            # Variations are the color/style options (variation_label)
            if variant.variation_label and variant.variation_label.strip():
                variations.add(variant.variation_label)
                
            # Patterns are the design/screen options (pattern_label)  
            if variant.pattern_label and variant.pattern_label.strip():
                patterns.add(variant.pattern_label)
        
        # Remove empty values
        variations.discard(None)
        variations.discard('')
        patterns.discard(None)
        patterns.discard('')
        
        # Format like Animal Crossing
        parts = []
        if len(variations) > 1:
            parts.append(f"{len(variations)} variations")
        if len(patterns) > 1:
            parts.append(f"{len(patterns)} patterns")
        
        if parts:
            return f" {' and '.join(parts)}"
        else:
            # Fallback to total variant count if we can't determine variations/patterns
            return f" {len(self.variants)} variants"
    
    def get_variation_footer(self, ui) -> str:
        """Get localized variation/pattern footer text.
        
        Args:
            ui: LocalizedUI instance for the target language
        
        Returns:
            Localized footer like "This item has 7 variations and 4 patterns"
        """
        if not self.variants or len(self.variants) <= 1:
            return ""
        
        # Count unique variations and patterns
        variations = set()
        patterns = set()
        
        for variant in self.variants:
            if variant.variation_label and variant.variation_label.strip():
                variations.add(variant.variation_label)
            if variant.pattern_label and variant.pattern_label.strip():
                patterns.add(variant.pattern_label)
        
        variations.discard(None)
        variations.discard('')
        patterns.discard(None)
        patterns.discard('')
        
        return ui.format_variation_footer(
            variation_count=len(variations),
            pattern_count=len(patterns),
            total_variants=len(self.variants)
        )
    
    def get_variants_available_text(self, ui) -> str:
        """Get localized 'X variations available' text for embed field.
        
        Args:
            ui: LocalizedUI instance for the target language
        
        Returns:
            Localized text like "8 variations available" or "7 variations and 4 patterns"
        """
        if not self.variants or len(self.variants) <= 1:
            return ""
        
        # Count unique variations and patterns
        variations = set()
        patterns = set()
        
        for variant in self.variants:
            if variant.variation_label and variant.variation_label.strip():
                variations.add(variant.variation_label)
            if variant.pattern_label and variant.pattern_label.strip():
                patterns.add(variant.pattern_label)
        
        variations.discard(None)
        variations.discard('')
        patterns.discard(None)
        patterns.discard('')
        
        return ui.format_variants_available(
            variation_count=len(variations),
            pattern_count=len(patterns),
            total_variants=len(self.variants)
        )
    
    @property
    def primary_variant(self) -> Optional[ItemVariant]:
        """Get the primary/default variant"""
        if not self.variants:
            return None
        # Return first variant or one with primary_index=0
        for variant in self.variants:
            if variant.primary_index == 0:
                return variant
        return self.variants[0]
    
    @property
    def display_image_url(self) -> Optional[str]:
        """Get the best image URL for display"""
        primary = self.primary_variant
        if primary and primary.image_url:
            return primary.image_url
        return self.image_url
    
    def to_discord_embed(self, variant: Optional[ItemVariant] = None, is_variant_view: bool = False, language: str = 'en') -> discord.Embed:
        """Create Discord embed for this item
        
        Args:
            variant: Optional specific variant to display
            is_variant_view: Whether this is a variant-specific view
            language: User's preferred language for UI labels (default: 'en')
        """
        selected_variant = variant or self.primary_variant
        ui = get_ui(language)
        
        # Build title
        if self.name:
            title = self.name
        
        embed = discord.Embed(
            title=title,
            color=discord.Color.green()
        )
        
        # Add basic info with localized labels
        info_lines = []
        
        if self.category:
            translated_category = ui.translate_category(self.category)
            info_lines.append(f"{ui.category}: {translated_category}")
        
        if self.sell_price:
            info_lines.append(f"{ui.sell_price}: {self.sell_price:,} {ui.bells}")
        
        if self.buy_price:
            info_lines.append(f"{ui.buy_price}: {self.buy_price:,} {ui.bells}")
            
        if self.source:
            translated_source = ui.translate_source(self.source)
            info_lines.append(f"{ui.source}: {translated_source}")
        
        embed.description = "\n".join(info_lines)
        
        if is_variant_view and variant:
            # Variant view format - cleaner with emoji sections
            variant_info = []
            variant_info.append(ui.details)
            
            # Show variant name
            default_parts = []
            if variant.variation_label:
                default_parts.append(variant.variation_label)
            if variant.pattern_label:
                default_parts.append(variant.pattern_label)
            
            if default_parts:
                variant_info.append(f"{ui.variant}: {', '.join(default_parts)}")
            
            # Show hex code
            if variant.item_hex:
                variant_info.append(f"{ui.hex}: {variant.item_hex}")
            
            # Show customize command with $ prefix
            if variant.item_hex and variant.ti_customize_str:
                variant_info.append(f"TI Customize: $customize {variant.item_hex} {variant.ti_customize_str}")
            
            if len(variant_info) > 1:  # More than just the title
                embed.add_field(name="", value="\n".join(variant_info), inline=False)
        else:
            # Base item view format - more detailed
            if selected_variant:
                variant_info = []
                
                # Show default variant details in clean format
                default_parts = []
                if selected_variant.variation_label:
                    default_parts.append(selected_variant.variation_label)
                if selected_variant.pattern_label:
                    default_parts.append(selected_variant.pattern_label)
                
                if default_parts:
                    variant_info.append(f"{ui.default}: {', '.join(default_parts)}")
                
                # Show only item hex (not all TI codes)
                if selected_variant.item_hex:
                    variant_info.append(f"{ui.item_hex}: {selected_variant.item_hex}")
                
                if variant_info:
                    embed.add_field(name=ui.details, value="\n".join(variant_info), inline=False)
            
            # Add variant count if multiple (base view only)
            if self.has_variants:
                # Get localized variants available text
                variant_text = self.get_variants_available_text(ui)
                embed.add_field(name=ui.variants, value=variant_text, inline=True)
            
            # Add HHA info if available (base view only)
            if self.hha_base or (selected_variant and (selected_variant.body_customizable or selected_variant.pattern_customizable)):
                hha_info = []
                if self.hha_base:
                    hha_info.append(f"{ui.hha_points}: {self.hha_base:,}")
                
                if selected_variant:
                    customization = []
                    if selected_variant.body_customizable:
                        customization.append("Body")
                    if selected_variant.pattern_customizable:
                        customization.append("Pattern")
                    if selected_variant.cyrus_customizable:
                        customization.append("Cyrus")
                    
                    if customization:
                        hha_info.append(f"{ui.customizable}: {', '.join(customization)}")
                
                if hha_info:
                    embed.add_field(name=ui.hha_info, value="\n".join(hha_info), inline=True)
        
        # Set image with fallback handling
        thumbnail_image_url = selected_variant.image_url_alt if selected_variant else self.display_image_url
        set_image_url = selected_variant.image_url if selected_variant else self.display_image_url
        # Note: This will be handled by the calling code since we can't use async here
        if thumbnail_image_url:
            embed.set_thumbnail(url=thumbnail_image_url)
        elif set_image_url:
            embed.set_thumbnail(url=set_image_url)

        #if embed.thumbnail.url != set_image_url:

        # if not embed.thumbnail or embed.thumbnail.url != set_image_url:
        #     embed.set_thumbnail(url=set_image_url)

        # if set_image_url and set_image_url != thumbnail_image_url:
        #     embed.set_image(url=set_image_url)

        return embed
    
    def to_embed(self) -> discord.Embed:
        """Convert this item to a Discord embed (compatibility method)"""
        return self.to_discord_embed()

@dataclass(slots=True)
class Critter:
    """Represents a critter (fish, insect, sea creature)"""
    
    id: int
    name: str
    kind: str  # 'fish', 'insect', 'sea'
    internal_id: Optional[int]
    source_unique_id: Optional[str]
    sell_price: Optional[int]
    item_hex: Optional[str]
    ti_primary: Optional[int]
    ti_secondary: Optional[int]
    ti_customize_str: Optional[str]
    ti_full_hex: Optional[str]
    location: Optional[str]
    shadow_size: Optional[str]
    movement_speed: Optional[str]
    catch_difficulty: Optional[str]
    vision: Optional[str]
    total_catches_to_unlock: Optional[str]
    spawn_rates: Optional[str]
    # Monthly availability (NH = Northern Hemisphere, SH = Southern Hemisphere)
    nh_jan: Optional[str]
    nh_feb: Optional[str]
    nh_mar: Optional[str]
    nh_apr: Optional[str]
    nh_may: Optional[str]
    nh_jun: Optional[str]
    nh_jul: Optional[str]
    nh_aug: Optional[str]
    nh_sep: Optional[str]
    nh_oct: Optional[str]
    nh_nov: Optional[str]
    nh_dec: Optional[str]
    sh_jan: Optional[str]
    sh_feb: Optional[str]
    sh_mar: Optional[str]
    sh_apr: Optional[str]
    sh_may: Optional[str]
    sh_jun: Optional[str]
    sh_jul: Optional[str]
    sh_aug: Optional[str]
    sh_sep: Optional[str]
    sh_oct: Optional[str]
    sh_nov: Optional[str]
    sh_dec: Optional[str]
    time_of_day: Optional[str]
    weather: Optional[str]
    rarity: Optional[str]
    description: Optional[str]
    catch_phrase: Optional[str]
    hha_base_points: Optional[int]
    hha_category: Optional[str]
    color1: Optional[str]
    color2: Optional[str]
    size: Optional[str]
    surface: Optional[str]
    icon_url: Optional[str]
    critterpedia_url: Optional[str]
    furniture_url: Optional[str]
    nookipedia_url: Optional[str]
    source: Optional[str]
    version_added: Optional[str]
    extra_json: Optional[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Critter':
        return cls(
            id=data['id'],
            name=data['name'],
            kind=data['kind'],
            internal_id=data.get('internal_id'),
            source_unique_id=data.get('source_unique_id'),
            sell_price=data.get('sell_price'),
            item_hex=data.get('item_hex'),
            ti_primary=data.get('ti_primary'),
            ti_secondary=data.get('ti_secondary'),
            ti_customize_str=data.get('ti_customize_str'),
            ti_full_hex=data.get('ti_full_hex'),
            location=data.get('location'),
            shadow_size=data.get('shadow_size'),
            movement_speed=data.get('movement_speed'),
            catch_difficulty=data.get('catch_difficulty'),
            vision=data.get('vision'),
            total_catches_to_unlock=data.get('total_catches_to_unlock'),
            spawn_rates=data.get('spawn_rates'),
            nh_jan=data.get('nh_jan'),
            nh_feb=data.get('nh_feb'),
            nh_mar=data.get('nh_mar'),
            nh_apr=data.get('nh_apr'),
            nh_may=data.get('nh_may'),
            nh_jun=data.get('nh_jun'),
            nh_jul=data.get('nh_jul'),
            nh_aug=data.get('nh_aug'),
            nh_sep=data.get('nh_sep'),
            nh_oct=data.get('nh_oct'),
            nh_nov=data.get('nh_nov'),
            nh_dec=data.get('nh_dec'),
            sh_jan=data.get('sh_jan'),
            sh_feb=data.get('sh_feb'),
            sh_mar=data.get('sh_mar'),
            sh_apr=data.get('sh_apr'),
            sh_may=data.get('sh_may'),
            sh_jun=data.get('sh_jun'),
            sh_jul=data.get('sh_jul'),
            sh_aug=data.get('sh_aug'),
            sh_sep=data.get('sh_sep'),
            sh_oct=data.get('sh_oct'),
            sh_nov=data.get('sh_nov'),
            sh_dec=data.get('sh_dec'),
            time_of_day=data.get('time_of_day'),
            weather=data.get('weather'),
            rarity=data.get('rarity'),
            description=data.get('description'),
            catch_phrase=data.get('catch_phrase'),
            hha_base_points=data.get('hha_base_points'),
            hha_category=data.get('hha_category'),
            color1=data.get('color1'),
            color2=data.get('color2'),
            size=data.get('size'),
            surface=data.get('surface'),
            icon_url=data.get('icon_url'),
            critterpedia_url=data.get('critterpedia_url'),
            furniture_url=data.get('furniture_url'),
            nookipedia_url=data.get('nookipedia_url'),
            source=data.get('source'),
            version_added=data.get('version_added'),
            extra_json=data.get('extra_json')
        )
    
    @property
    def type_display(self) -> str:
        """Get user-friendly type display (English default)"""
        return {
            'fish': 'Fish',
            'insect': 'Bug',
            'sea': 'Sea Creature'
        }.get(self.kind, self.kind.title())
    
    def get_type_display(self, language: str = 'en') -> str:
        """Get user-friendly type display in the specified language"""
        ui = get_ui(language)
        return {
            'fish': ui.type_fish,
            'insect': ui.type_bug,
            'sea': ui.type_sea_creature
        }.get(self.kind, self.kind.title())
    
    def to_discord_embed(self, language: str = 'en') -> discord.Embed:
        """Create Discord embed for this critter"""
        ui = get_ui(language)
        
        embed = discord.Embed(
            title=f"{self.name}",
            color=discord.Color.blue()
        )
        
        # Basic info
        info_lines = []
        if self.sell_price:
            info_lines.append(f"**{ui.sell_price}:** {self.sell_price:,} {ui.bells}")
        
        if self.location:
            info_lines.append(f"**{ui.location}:** {translate_critter_detail(self.location, language)}")
            
        if self.shadow_size:
            info_lines.append(f"**{ui.shadow_size}:** {translate_critter_detail(self.shadow_size, language)}")
            
        if self.time_of_day:
            info_lines.append(f"**{ui.time_label}:** {translate_critter_detail(self.time_of_day, language)}")
        
        embed.description = "\n".join(info_lines)
        
        # Add item hex if available
        if self.item_hex:
            embed.add_field(name=ui.item_hex, value=f"`{self.item_hex}`", inline=True)
        
        # Add catch info if available  
        if self.catch_difficulty or self.vision or self.movement_speed:
            catch_info = []
            if self.catch_difficulty:
                catch_info.append(f"**{ui.difficulty}:** {translate_critter_detail(self.catch_difficulty, language)}")
            if self.vision:
                catch_info.append(f"**{ui.vision}:** {translate_critter_detail(self.vision, language)}")
            if self.movement_speed:
                catch_info.append(f"**{ui.movement}:** {translate_critter_detail(self.movement_speed, language)}")
            
            embed.add_field(name=ui.catch_info, value="\n".join(catch_info), inline=True)
        
        # Set image with fallback handling
        if self.icon_url:
            embed.set_thumbnail(url=self.icon_url)
        elif self.critterpedia_url:
            embed.set_thumbnail(url=self.critterpedia_url)
        
        return embed
    
    def to_embed(self, language: str = 'en') -> discord.Embed:
        """Convert this critter to a Discord embed (compatibility method)"""
        return self.to_discord_embed(language)

@dataclass(slots=True)
class Recipe:
    """Represents a DIY recipe"""
    
    id: int
    name: str
    source_unique_id: Optional[str]
    internal_id: Optional[int]
    product_item_id: Optional[int]
    category: Optional[str]
    source: Optional[str]
    source_notes: Optional[str]
    is_diy: bool
    buy_price: Optional[int]
    sell_price: Optional[int]
    hha_base: Optional[int]
    version_added: Optional[str]
    item_hex: Optional[str]
    ti_primary: Optional[int]
    ti_secondary: Optional[int]
    ti_customize_str: Optional[str]
    ti_full_hex: Optional[str]
    image_url: Optional[str]
    image_url_alt: Optional[str]
    nookipedia_url: Optional[str]
    extra_json: Optional[str]
    ingredients: List[tuple] = field(default_factory=list)  # List of (ingredient_name, quantity)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Recipe':
        return cls(
            id=data['id'],
            name=data['name'],
            source_unique_id=data.get('source_unique_id'),
            internal_id=data.get('internal_id'),
            product_item_id=data.get('product_item_id'),
            category=data.get('category'),
            source=data.get('source'),
            source_notes=data.get('source_notes'),
            is_diy=bool(data.get('is_diy', 1)),
            buy_price=data.get('buy_price'),
            sell_price=data.get('sell_price'),
            hha_base=data.get('hha_base'),
            version_added=data.get('version_added'),
            item_hex=data.get('item_hex'),
            ti_primary=data.get('ti_primary'),
            ti_secondary=data.get('ti_secondary'),
            ti_customize_str=data.get('ti_customize_str'),
            ti_full_hex=data.get('ti_full_hex'),
            image_url=data.get('image_url'),
            image_url_alt=data.get('image_url_alt'),
            nookipedia_url=data.get('nookipedia_url'),
            extra_json=data.get('extra_json'),
            ingredients=[]
        )
    
    def is_food(self) -> bool:
        """Check if this recipe is for food based on category"""
        if not self.category:
            return False
        return self.category.lower() in ['savory', 'sweet']
    
    def to_discord_embed(self, language: str = 'en', ingredient_translations: Dict[str, str] = None) -> discord.Embed:
        """Create Discord embed for this recipe
        
        Args:
            language: User's preferred language for UI labels (default: 'en')
            ingredient_translations: Optional dict mapping English ingredient names to translated names
        """
        ui = get_ui(language)
        
        # Choose emoji and color based on recipe type
        if self.is_food():
            emoji = "🍳" if self.category and "savory" in self.category.lower() else "🧁"
            color = discord.Color.from_rgb(255, 193, 7)  # Food yellow
            recipe_type = ui.food_recipe
        else:
            emoji = "🛠️"
            color = discord.Color.orange()
            recipe_type = ui.diy_recipe
        
        embed = discord.Embed(
            title=f"{self.name}",
            color=color
        )
        
        # Translate category
        category_display = ui.translate_category(self.category) if self.category else ui.unknown_category
        embed.set_footer(text=f"{emoji} {recipe_type} • {category_display}")
        
        # Basic info
        info_lines = []

        if recipe_type:
            info_lines.append(f"**{ui.category}:** {recipe_type}")

        if self.category:
            info_lines.append(f"**{ui.category}:** {category_display}")
        
        if self.sell_price:
            info_lines.append(f"**{ui.sell_price}:** {self.sell_price:,} {ui.bells}")
        
        if self.source:
            source_text = ui.translate_source(self.source)
            if self.source_notes:
                source_text += f" ({self.source_notes})"
            info_lines.append(f"**{ui.source}:** {source_text}")
        
        embed.description = "\n".join(info_lines)
        
        # Add ingredients if available
        if self.ingredients:
            ingredient_lines = []
            for ingredient_name, quantity in self.ingredients:
                # Use translated name if available, otherwise use original
                display_name = ingredient_name
                if ingredient_translations and ingredient_name in ingredient_translations:
                    display_name = ingredient_translations[ingredient_name]
                ingredient_lines.append(f"• {quantity}x {display_name}")
            
            embed.add_field(
                name=ui.ingredients, 
                value="\n".join(ingredient_lines), 
                inline=False
            )
        
        # Add item hex if available
        if self.item_hex:
            embed.add_field(name=ui.item_hex, value=f"`{self.item_hex}`", inline=True)
        
        # Set image with fallback handling
        if self.image_url:
            embed.set_thumbnail(url=self.image_url)
        
        return embed
    
    def to_embed(self, language: str = 'en') -> discord.Embed:
        """Convert this recipe to a Discord embed (compatibility method)"""
        return self.to_discord_embed(language=language)

@dataclass(slots=True)
class Villager:
    """Represents a villager"""
    id: int
    name: str
    species: Optional[str]
    gender: Optional[str]
    personality: Optional[str]
    subtype: Optional[str]
    hobby: Optional[str]
    birthday: Optional[str]
    catchphrase: Optional[str]
    favorite_song: Optional[str]
    favorite_saying: Optional[str]
    style1: Optional[str]
    style2: Optional[str]
    color1: Optional[str]
    color2: Optional[str]
    default_clothing: Optional[str]
    default_umbrella: Optional[str]
    wallpaper: Optional[str]
    flooring: Optional[str]
    furniture_list: Optional[str]
    furniture_name_list: Optional[str]
    diy_workbench: Optional[str]
    kitchen_equipment: Optional[str]
    version_added: Optional[str]
    name_color: Optional[str]
    bubble_color: Optional[str]
    filename: Optional[str]
    source_unique_id: Optional[str]
    icon_image: Optional[str]
    photo_image: Optional[str]
    house_image: Optional[str]
    house_interior_image: Optional[str]
    nookipedia_url: Optional[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Villager':
        return cls(
            id=data['id'],
            name=data['name'],
            species=data.get('species'),
            gender=data.get('gender'),
            personality=data.get('personality'),
            subtype=data.get('subtype'),
            hobby=data.get('hobby'),
            birthday=data.get('birthday'),
            catchphrase=data.get('catchphrase'),
            favorite_song=data.get('favorite_song'),
            favorite_saying=data.get('favorite_saying'),
            style1=data.get('style1'),
            style2=data.get('style2'),
            color1=data.get('color1'),
            color2=data.get('color2'),
            default_clothing=data.get('default_clothing'),
            default_umbrella=data.get('default_umbrella'),
            wallpaper=data.get('wallpaper'),
            flooring=data.get('flooring'),
            furniture_list=data.get('furniture_list'),
            furniture_name_list=data.get('furniture_name_list'),
            diy_workbench=data.get('diy_workbench'),
            kitchen_equipment=data.get('kitchen_equipment'),
            version_added=data.get('version_added'),
            name_color=data.get('name_color'),
            bubble_color=data.get('bubble_color'),
            filename=data.get('filename'),
            source_unique_id=data.get('source_unique_id'),
            icon_image=data.get('icon_image'),
            photo_image=data.get('photo_image'),
            house_image=data.get('house_image'),
            house_interior_image=data.get('house_interior_image'),
            nookipedia_url=data.get('nookipedia_url')
        )
    
    @property
    def display_name(self) -> str:
        """Get display name with gender emoji"""
        emoji = "♂️" if self.gender == "Male" else "♀️" if self.gender == "Female" else ""
        return f"{emoji} {self.name}".strip()
    
    def to_discord_embed(self, language: str = 'en') -> discord.Embed:
        """Create Discord embed for this villager"""
        from bot.utils.localization import LocalizedUI, translate_villager_detail
        ui = LocalizedUI(language)
        
        embed = discord.Embed(
            title=f"🏘️ {self.display_name}",
            color=discord.Color.purple()
        )
        
        # Basic info in simple format (no bold)
        info_lines = []
        if self.species:
            info_lines.append(f"{ui.species}: {translate_villager_detail(self.species, language)}")
        
        if self.personality:
            info_lines.append(f"{ui.personality}: {translate_villager_detail(self.personality, language)}")
        
        if self.hobby:
            info_lines.append(f"{ui.hobby}: {translate_villager_detail(self.hobby, language)}")
        
        if self.birthday:
            info_lines.append(f"{ui.birthday}: {self.birthday}")
        
        if self.catchphrase:
            info_lines.append(f"{ui.catchphrase}: \"{self.catchphrase}\"")
        
        embed.description = "\n".join(info_lines)
        
        # Add style/color preferences
        if self.style1 or self.style2 or self.color1 or self.color2:
            prefs = []
            if self.style1:
                style_text = translate_villager_detail(self.style1, language)
                if self.style2:
                    style_text += f", {translate_villager_detail(self.style2, language)}"
                prefs.append(f"{ui.style}: {style_text}")
            
            if self.color1:
                color_text = translate_villager_detail(self.color1, language)
                if self.color2:
                    color_text += f", {translate_villager_detail(self.color2, language)}"
                prefs.append(f"{ui.colors}: {color_text}")
            
            embed.add_field(name=ui.preferences, value="\n".join(prefs), inline=True)
        
        # Add favorite things
        if self.favorite_song or self.favorite_saying:
            favorites = []
            if self.favorite_song:
                favorites.append(f"{ui.song}: {self.favorite_song}")
            if self.favorite_saying:
                favorites.append(f"{ui.saying}: \"{self.favorite_saying}\"")
            
            embed.add_field(name=ui.favorites, value="\n".join(favorites), inline=True)
        
        # Set image with fallback handling
        if self.icon_image:
            embed.set_thumbnail(url=self.icon_image)
        
        return embed
    
    def to_embed(self, language: str = 'en') -> discord.Embed:
        """Convert this villager to a Discord embed (compatibility method)"""
        return self.to_discord_embed(language)

@dataclass(slots=True)
class Artwork:
    """Represents a piece of artwork"""
    id: int
    name: str
    image_url: Optional[str]
    image_url_alt: Optional[str]
    genuine: bool
    art_category: Optional[str]
    buy_price: Optional[int]
    sell_price: Optional[int]
    color1: Optional[str]
    color2: Optional[str]
    size: Optional[str]
    real_artwork_title: Optional[str]
    artist: Optional[str]
    description: Optional[str]
    source: Optional[str]
    source_notes: Optional[str]
    hha_base_points: Optional[int]
    hha_concept1: Optional[str]
    hha_concept2: Optional[str]
    hha_series: Optional[str]
    hha_set: Optional[str]
    interact: Optional[str]
    tag: Optional[str]
    speaker_type: Optional[str]
    lighting_type: Optional[str]
    catalog: Optional[str]
    version_added: Optional[str]
    unlocked: Optional[str]
    filename: Optional[str]
    internal_id: Optional[int]
    source_unique_id: Optional[str]
    item_hex: Optional[str]
    ti_primary: Optional[int]
    ti_secondary: Optional[int]
    ti_customize_str: Optional[str]
    ti_full_hex: Optional[str]
    nookipedia_url: Optional[str]
    extra_json: Optional[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Artwork':
        return cls(
            id=data['id'],
            name=data['name'],
            image_url=data.get('image_url'),
            image_url_alt=data.get('image_url_alt'),
            genuine=bool(data.get('genuine', 0)),
            art_category=data.get('art_category'),
            buy_price=data.get('buy_price'),
            sell_price=data.get('sell_price'),
            color1=data.get('color1'),
            color2=data.get('color2'),
            size=data.get('size'),
            real_artwork_title=data.get('real_artwork_title'),
            artist=data.get('artist'),
            description=data.get('description'),
            source=data.get('source'),
            source_notes=data.get('source_notes'),
            hha_base_points=data.get('hha_base_points'),
            hha_concept1=data.get('hha_concept1'),
            hha_concept2=data.get('hha_concept2'),
            hha_series=data.get('hha_series'),
            hha_set=data.get('hha_set'),
            interact=data.get('interact'),
            tag=data.get('tag'),
            speaker_type=data.get('speaker_type'),
            lighting_type=data.get('lighting_type'),
            catalog=data.get('catalog'),
            version_added=data.get('version_added'),
            unlocked=data.get('unlocked'),
            filename=data.get('filename'),
            internal_id=data.get('internal_id'),
            source_unique_id=data.get('source_unique_id'),
            item_hex=data.get('item_hex'),
            ti_primary=data.get('ti_primary'),
            ti_secondary=data.get('ti_secondary'),
            ti_customize_str=data.get('ti_customize_str'),
            ti_full_hex=data.get('ti_full_hex'),
            nookipedia_url=data.get('nookipedia_url'),
            extra_json=data.get('extra_json')
        )
    
    def to_discord_embed(self, language: str = 'en') -> discord.Embed:
        """Create Discord embed for this artwork
        
        Args:
            language: User's preferred language for UI labels (default: 'en')
        """
        ui = get_ui(language)
        
        # Choose color and emoji based on authenticity
        if self.genuine:
            color = discord.Color.from_rgb(52, 152, 219)  # Blue for genuine
            authenticity = ui.genuine
        else:
            color = discord.Color.from_rgb(231, 76, 60)  # Red for fake
            authenticity = ui.fake
        
        embed = discord.Embed(
            title=f"{self.name} ({authenticity})",
            color=color
        )
        
        # Basic info
        info_lines = []
        if self.art_category:
            translated_category = ui.translate_category(self.art_category)
            info_lines.append(f"{ui.category}: {translated_category}")
        
        if self.buy_price:
            info_lines.append(f"{ui.buy_price}: {self.buy_price:,} {ui.bells}")
        
        if self.sell_price:
            info_lines.append(f"{ui.sell_price}: {self.sell_price:,} {ui.bells}")
        
        if self.source:
            translated_source = ui.translate_source(self.source)
            source_text = translated_source
            if self.source_notes:
                source_text += f" ({self.source_notes})"
            info_lines.append(f"{ui.source}: {source_text}")
        
        embed.description = "\n".join(info_lines)
        
        # Add real artwork info if available
        if self.real_artwork_title or self.artist:
            real_info = []
            if self.real_artwork_title:
                real_info.append(f"{ui.artwork_title}: {self.real_artwork_title}")
            if self.artist:
                real_info.append(f"{ui.artwork_artist}: {self.artist}")
            
            embed.add_field(
                name=ui.real_artwork_info,
                value="\n".join(real_info),
                inline=False
            )
        
        # Add item hex if available (no TI codes as requested)
        if self.item_hex:
            embed.add_field(name=ui.item_hex, value=f"`{self.item_hex}`", inline=True)
        
        # Set image with fallback handling
        if self.image_url:
            embed.set_thumbnail(url=self.image_url)
        
        return embed
    
    def to_embed(self, language: str = 'en') -> discord.Embed:
        """Convert this artwork to a Discord embed (compatibility method)"""
        return self.to_discord_embed(language=language)

@dataclass(slots=True)
class Fossil:
    """Represents a fossil"""
    id: int
    name: str
    source_unique_id: Optional[str]
    image_url: Optional[str]
    image_url_alt: Optional[str]
    buy_price: Optional[int]
    sell_price: Optional[int]
    fossil_group: Optional[str]
    description: Optional[str]
    hha_base_points: Optional[int]
    color1: Optional[str]
    color2: Optional[str]
    size: Optional[str]
    source: Optional[str]
    museum: Optional[str]
    interact: Optional[str]
    catalog: Optional[str]
    filename: Optional[str]
    internal_id: Optional[int]
    item_hex: Optional[str]
    ti_primary: Optional[int]
    ti_secondary: Optional[int]
    ti_customize_str: Optional[str]
    ti_full_hex: Optional[str]
    nookipedia_url: Optional[str]
    extra_json: Optional[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Fossil':
        return cls(
            id=data['id'],
            name=data['name'],
            source_unique_id=data.get('source_unique_id'),
            image_url=data.get('image_url'),
            image_url_alt=data.get('image_url_alt'),
            buy_price=data.get('buy_price'),
            sell_price=data.get('sell_price'),
            fossil_group=data.get('fossil_group'),
            description=data.get('description'),
            hha_base_points=data.get('hha_base_points'),
            color1=data.get('color1'),
            color2=data.get('color2'),
            size=data.get('size'),
            source=data.get('source'),
            museum=data.get('museum'),
            interact=data.get('interact'),
            catalog=data.get('catalog'),
            filename=data.get('filename'),
            internal_id=data.get('internal_id'),
            item_hex=data.get('item_hex'),
            ti_primary=data.get('ti_primary'),
            ti_secondary=data.get('ti_secondary'),
            ti_customize_str=data.get('ti_customize_str'),
            ti_full_hex=data.get('ti_full_hex'),
            nookipedia_url=data.get('nookipedia_url'),
            extra_json=data.get('extra_json')
        )
    
    def to_discord_embed(self, language: str = 'en') -> discord.Embed:
        """Create Discord embed for this fossil"""
        ui = get_ui(language)
        
        embed = discord.Embed(
            title=f"{self.name}",
            color=discord.Color.from_rgb(139, 69, 19)  # Brown for fossils
        )
        
        # Basic info
        info_lines = []
        if self.sell_price:
            info_lines.append(f"**{ui.sell_price}:** {self.sell_price:,} {ui.bells}")
        
        if self.fossil_group:
            info_lines.append(f"**{ui.fossil_group}:** {self.fossil_group}")
        
        if self.size:
            info_lines.append(f"**{ui.size}:** {self.size}")
        
        if self.source:
            info_lines.append(f"**{ui.source}:** {translate_fossil_detail(self.source, language)}")
        
        embed.description = "\n".join(info_lines)
        
        # Add museum info if available (with translations for room and interaction)
        museum_info = []
        if self.museum:
            museum_info.append(f"**{ui.museum}:** {translate_fossil_detail(self.museum, language)}")
        if self.interact:
            museum_info.append(f"**{ui.interaction}:** {translate_fossil_detail(self.interact, language)}")
        
        if museum_info:
            embed.add_field(
                name=f"🏛️ {ui.museum_info}",
                value="\n".join(museum_info),
                inline=True
            )
        
        # Add HHA info if available
        if self.hha_base_points:
            embed.add_field(
                name=f"🏠 {ui.hha_points}",
                value=f"{self.hha_base_points:,} {ui.points}",
                inline=True
            )
        
        # Add item hex if available
        if self.item_hex:
            embed.add_field(name=ui.item_hex, value=f"`{self.item_hex}`", inline=True)
        
        # Set image with fallback handling
        if self.image_url:
            embed.set_thumbnail(url=self.image_url)
        
        return embed
    
    def to_embed(self, language: str = 'en') -> discord.Embed:
        """Convert this fossil to a Discord embed (compatibility method)"""
        return self.to_discord_embed(language=language)
