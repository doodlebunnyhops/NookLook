from dataclasses import dataclass
from typing import Optional, Dict, Any
import discord

@dataclass
class ACNHItem:
    """Represents an Animal Crossing: New Horizons item with comprehensive data from community spreadsheets"""
    
    # Basic info
    id: Optional[int]
    name: str
    name_normalized: str
    category: str = ""
    color_variant: str = ""
    hex_id: str = ""
    
    # Display and gameplay data you want to show
    sell_price: Optional[int] = None
    hha_base: Optional[int] = None
    hha_category: str = ""
    grid_width: Optional[int] = None
    grid_length: Optional[int] = None
    
    # Series and classification
    item_series: str = ""
    item_set: str = ""
    tag: str = ""
    
    # Customization
    customizable: bool = False
    custom_kits: int = 0
    custom_kit_type: str = ""
    
    # Additional metadata from CSV imports
    interact: str = ""
    outdoor: str = ""
    speaker_type: str = ""
    lighting_type: str = ""
    catalog: str = ""
    version_added: str = ""
    unlocked: str = ""
    filename: str = ""
    variant_id: str = ""
    internal_id: str = ""
    unique_entry_id: str = ""
    
    # Images
    image_filename: str = ""
    image_url: str = ""
    
    # Metadata
    notes: str = ""
    last_fetched: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ACNHItem':
        """Create an ACNHItem from a dictionary (usually from database)"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            name_normalized=data.get('name_normalized', ''),
            category=data.get('category', ''),
            color_variant=data.get('color_variant', ''),
            hex_id=data.get('hex_id', '')
        )
    
    def get_image_url(self) -> str:
        """Generate the image URL from hex_id"""
        if not self.hex_id:
            return ""
        return f"https://acnhcdn.com/latest/FtrIcon/{self.hex_id}.png"
    
    def display_name(self) -> str:
        """Get display name with color variant"""
        if self.color_variant:
            return f"{self.name} ({self.color_variant})"
        return self.name
    
    def to_embed(self) -> discord.Embed:
        """Convert item to Discord embed"""
        title = self.display_name()
        embed = discord.Embed(title=title, color=0x7FB069)
        
        if self.category:
            embed.add_field(name="Category", value=self.category, inline=True)
        
        if self.hex_id:
            embed.add_field(name="Hex ID", value=self.hex_id, inline=True)
            image_url = self.get_image_url()
            if image_url:
                embed.set_thumbnail(url=image_url)
        
        return embed