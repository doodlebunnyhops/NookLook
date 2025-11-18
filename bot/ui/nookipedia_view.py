"""
Discord views for Nookipedia link buttons
"""
import discord
from typing import Optional

class NookipediaView(discord.ui.View):
    """A view with a button linking to Nookipedia"""
    
    def __init__(self, nookipedia_url: str):
        super().__init__(timeout=300)  # 5 minute timeout
        self.nookipedia_url = nookipedia_url
        
        # Create the Nookipedia link button
        if nookipedia_url:
            self.add_item(discord.ui.Button(
                label="Nookipedia",
                style=discord.ButtonStyle.link,
                url=nookipedia_url,
                emoji="📖"
            ))

def get_nookipedia_view(nookipedia_url: Optional[str]) -> Optional[NookipediaView]:
    """Get a Nookipedia view if URL is available, otherwise None"""
    if nookipedia_url:
        return NookipediaView(nookipedia_url)
    return None