from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import discord

@dataclass
class BuyPrice:
    """Represents a buy price for an item"""
    price: int
    currency: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BuyPrice':
        return cls(
            price=data.get('price', 0),
            currency=data.get('currency', 'Bells')
        )
    
    def __str__(self) -> str:
        return f"{self.price:,} {self.currency}"

@dataclass
class AvailabilitySource:
    """Represents an availability source for an item"""
    source: str
    note: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AvailabilitySource':
        return cls(
            source=data.get('from', data.get('source', '')),
            note=data.get('note', '')
        )
    
    def __str__(self) -> str:
        if self.note:
            return f"{self.source} ({self.note})"
        return self.source

@dataclass
class ItemVariation:
    """Represents a variation of an item"""
    variation: str
    pattern: str = ""
    image_url: str = ""
    colors: List[str] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ItemVariation':
        return cls(
            variation=data.get('variation', ''),
            pattern=data.get('pattern', ''),
            image_url=data.get('image_url', ''),
            colors=data.get('colors', [])
        )
    
    def color_text(self) -> str:
        """Get colors as formatted text"""
        if not self.colors:
            return "No colors specified"
        return ", ".join(self.colors)

@dataclass
class ACNHItem:
    """Represents an Animal Crossing: New Horizons item with all related data"""
    
    # Basic info
    id: Optional[int]
    name: str
    name_normalized: str
    url: str = ""
    category: str = ""
    
    # Series and classification
    item_series: str = ""
    item_set: str = ""
    themes: List[str] = field(default_factory=list)
    hha_category: str = ""
    hha_base: Optional[int] = None
    tag: str = ""
    
    # Special properties
    lucky: bool = False
    lucky_season: str = ""
    
    # Pricing
    buy_prices: List[BuyPrice] = field(default_factory=list)
    sell_price: Optional[int] = None
    
    # Customization
    variation_total: int = 0
    pattern_total: int = 0
    customizable: bool = False
    custom_kits: int = 0
    custom_kit_type: str = ""
    custom_body_part: str = ""
    custom_pattern_part: str = ""
    
    # Physical properties
    grid_width: Optional[int] = None
    grid_length: Optional[int] = None
    
    # Images
    image_filename: str = ""
    image_url: str = ""
    height: Optional[float] = None
    door_decor: bool = False
    
    # Game properties
    version_added: str = ""
    unlocked: bool = True
    functions: List[str] = field(default_factory=list)
    
    # Availability and variations
    availability: List[AvailabilitySource] = field(default_factory=list)
    variations: List[ItemVariation] = field(default_factory=list)
    
    # Metadata
    notes: str = ""
    last_fetched: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ACNHItem':
        """Create an ACNHItem from a dictionary (usually from database)"""
        
        # Convert buy prices
        buy_prices = []
        if 'buy' in data and data['buy']:
            for buy_data in data['buy']:
                buy_prices.append(BuyPrice.from_dict(buy_data))
        
        # Convert availability sources
        availability = []
        if 'availability' in data and data['availability']:
            for avail_data in data['availability']:
                availability.append(AvailabilitySource.from_dict(avail_data))
        
        # Convert variations
        variations = []
        if 'variations' in data and data['variations']:
            for var_data in data['variations']:
                variations.append(ItemVariation.from_dict(var_data))
        
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            name_normalized=data.get('name_normalized', ''),
            url=data.get('url', ''),
            category=data.get('category', ''),
            item_series=data.get('item_series', ''),
            item_set=data.get('item_set', ''),
            themes=data.get('themes', []),
            hha_category=data.get('hha_category', ''),
            hha_base=data.get('hha_base'),
            tag=data.get('tag', ''),
            lucky=data.get('lucky', False),
            lucky_season=data.get('lucky_season', ''),
            buy_prices=buy_prices,
            sell_price=data.get('sell_price') or data.get('sell'),
            variation_total=data.get('variation_total', 0),
            pattern_total=data.get('pattern_total', 0),
            customizable=data.get('customizable', False),
            custom_kits=data.get('custom_kits', 0),
            custom_kit_type=data.get('custom_kit_type', ''),
            custom_body_part=data.get('custom_body_part', ''),
            custom_pattern_part=data.get('custom_pattern_part', ''),
            grid_width=data.get('grid_width'),
            grid_length=data.get('grid_length'),
            height=data.get('height'),
            door_decor=data.get('door_decor', False),
            version_added=data.get('version_added', ''),
            unlocked=data.get('unlocked', True),
            functions=data.get('functions', []),
            availability=availability,
            variations=variations,
            notes=data.get('notes', ''),
            image_filename=data.get('image_filename', ''),
            image_url=data.get('image_url', ''),
            last_fetched=data.get('last_fetched')
        )
    
    def primary_image_url(self) -> str:
        """Get the primary image URL for this item"""
        # First try the main item image URL
        if self.image_url:
            return self.image_url
        # Fallback to variation image if available
        if self.variations and self.variations[0].image_url:
            return self.variations[0].image_url
        return ""
    
    def size_text(self) -> str:
        """Get size as formatted text"""
        if self.grid_width and self.grid_length:
            return f"{self.grid_width}×{self.grid_length}"
        return "Unknown size"
    
    def buy_price_text(self) -> str:
        """Get buy prices as formatted text"""
        if not self.buy_prices:
            return "Not for sale"
        return "\n".join(str(price) for price in self.buy_prices)
    
    def sell_price_text(self) -> str:
        """Get sell price as formatted text"""
        if self.sell_price is None:
            return "Cannot sell"
        return f"{self.sell_price:,} Bells"
    
    def themes_text(self) -> str:
        """Get themes as formatted text"""
        if not self.themes:
            return "No themes"
        return ", ".join(self.themes)
    
    def functions_text(self) -> str:
        """Get functions as formatted text"""
        if not self.functions:
            return "Decorative"
        return ", ".join(self.functions)
    
    def availability_text(self) -> str:
        """Get availability as formatted text"""
        if not self.availability:
            return "Unknown"
        return "\n".join(str(avail) for avail in self.availability)
    
    def variation_summary(self) -> str:
        """Get variation summary text"""
        if self.variation_total == 0:
            return "No variations"
        elif self.variation_total == 1:
            return "1 variation"
        else:
            return f"{self.variation_total} variations"
    
    def customization_summary(self) -> str:
        """Get customization summary text"""
        if not self.customizable:
            return "Not customizable"
        
        parts = []
        if self.custom_body_part:
            parts.append(f"Body: {self.custom_body_part}")
        if self.custom_pattern_part:
            parts.append(f"Pattern: {self.custom_pattern_part}")
        
        if parts:
            kit_text = f" ({self.custom_kits} {self.custom_kit_type})" if self.custom_kits > 0 else ""
            return f"Customizable: {', '.join(parts)}{kit_text}"
        else:
            return "Customizable"
    
    def to_discord_embed(self, color: discord.Color = discord.Color.green()) -> discord.Embed:
        """Convert this item to a Discord embed"""
        embed = discord.Embed(
            title=self.name,
            url=self.url if self.url else None,
            description="Animal Crossing: New Horizons Item",
            color=color
        )
        
        # Set image if available
        image_url = self.primary_image_url()
        if image_url:
            embed.set_image(url=image_url)
        
        # Basic info
        if self.category:
            embed.add_field(name="Category", value=self.category, inline=True)
        
        if self.item_series:
            embed.add_field(name="Series", value=self.item_series, inline=True)
        
        embed.add_field(name="Size", value=self.size_text(), inline=True)
        
        # Pricing
        if self.buy_prices:
            embed.add_field(name="Buy Price", value=self.buy_price_text(), inline=True)
        
        if self.sell_price is not None:
            embed.add_field(name="Sell Price", value=self.sell_price_text(), inline=True)
        
        # Themes and functions
        if self.themes:
            embed.add_field(name="Themes", value=self.themes_text(), inline=False)
        
        if self.functions:
            embed.add_field(name="Function", value=self.functions_text(), inline=True)
        
        # Variations and customization
        if self.variation_total > 0:
            embed.add_field(name="Variations", value=self.variation_summary(), inline=True)
        
        if self.customizable:
            embed.add_field(name="Customization", value=self.customization_summary(), inline=False)
        
        # Special properties
        if self.lucky:
            lucky_text = f"Lucky item"
            if self.lucky_season:
                lucky_text += f" ({self.lucky_season})"
            embed.add_field(name="✨ Special", value=lucky_text, inline=True)
        
        # HHA info
        if self.hha_base is not None:
            embed.add_field(name="HHA Points", value=f"{self.hha_base:,}", inline=True)
        
        # Availability
        if self.availability:
            embed.add_field(name="Availability", value=self.availability_text(), inline=False)
        
        # Footer
        embed.set_footer(text="Data from Nookipedia API • nookipedia.com")
        
        return embed
    
    def to_detailed_embed(self) -> List[discord.Embed]:
        """Convert this item to multiple detailed Discord embeds if needed"""
        embeds = []
        
        # Main embed
        main_embed = self.to_discord_embed()
        embeds.append(main_embed)
        
        # Variations embed if there are many variations
        if len(self.variations) > 3:
            var_embed = discord.Embed(
                title=f"{self.name} - Variations",
                color=discord.Color.blue()
            )
            
            for i, variation in enumerate(self.variations[:10]):  # Limit to 10 to avoid Discord limits
                var_embed.add_field(
                    name=variation.variation,
                    value=f"Colors: {variation.color_text()}",
                    inline=True
                )
            
            if len(self.variations) > 10:
                var_embed.add_field(
                    name="...",
                    value=f"And {len(self.variations) - 10} more variations",
                    inline=False
                )
            
            embeds.append(var_embed)
        
        return embeds