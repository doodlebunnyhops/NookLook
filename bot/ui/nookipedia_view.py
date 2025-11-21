"""
Discord views for Nookipedia link buttons
"""
import discord
from typing import Optional

class NookipediaView(discord.ui.View):
    """A view with a button linking to Nookipedia"""
    
    def __init__(self, nookipedia_url: str):
        super().__init__(timeout=120)  # 2 minute timeout
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
        """Disable interactive items when view times out after 2 minutes, but keep link buttons enabled"""
        # Disable all buttons and selects except link buttons
        # Note: NookipediaView typically only has link buttons, so this may not disable anything
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                # Keep link buttons enabled (they don't need interaction handling)
                if item.style != discord.ButtonStyle.link:
                    item.disabled = True
            elif isinstance(item, discord.ui.Select):
                item.disabled = True

def get_nookipedia_view(nookipedia_url: Optional[str]) -> Optional[NookipediaView]:
    """Get a Nookipedia view if URL is available, otherwise None"""
    if nookipedia_url:
        return NookipediaView(nookipedia_url)
    return None