import discord
from discord.ext import commands
from discord import app_commands
import logging

from bot.services.acnh_service import NooklookService
from bot.ui.common import get_combined_view
from bot.cogs.acnh.base import check_guild_ephemeral
from bot.cogs.acnh.autocomplete import artwork_name_autocomplete

logger = logging.getLogger(__name__)


class ArtworkCommands(commands.Cog):
    """ACNH artwork commands using nooklook database"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @property
    def service(self) -> NooklookService:
        """Get the shared NooklookService from the bot instance"""
        return self.bot.nooklook_service


    @app_commands.command(name="artwork", description="Look up a specific ACNH artwork")
    @app_commands.describe(name="The artwork name to look up")
    @app_commands.autocomplete(name=artwork_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def artwork(self, interaction: discord.Interaction, name: str):
        """Look up artwork details"""
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        logger.info(f"artwork command used by:\n\t{interaction.user.display_name} ({interaction.user.id})\n\tsearching for: '{name}'")
        
        try:
            # Convert name to artwork ID if it's numeric (from autocomplete)
            if name.isdigit():
                artwork_id = int(name)
                artwork = await self.service.get_artwork_by_id(artwork_id)
            else:
                # Search for artwork by name
                search_results = await self.service.search_all(name, category_filter="artwork")
                artwork = search_results[0] if search_results else None
            
            if not artwork:
                embed = discord.Embed(
                    title="❌ Artwork Not Found",
                    description=f"Sorry, I couldn't find artwork named **{name}** 😿\n"
                               f"Try using `/search {name}` to see if there are similar names.",
                    color=0xe74c3c
                )
                
                # Add suggestion for genuine vs fake
                embed.add_field(
                    name="💡 Search Tips",
                    value="• Artwork comes in genuine and fake versions\n"
                          "• Use the artwork name without 'genuine' or 'fake'\n"
                          "• Try `/search` with partial names or artist names",
                    inline=False
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            logger.info(f"found artwork: {artwork.name}")
            
            # Create the artwork embed
            embed = artwork.to_discord_embed()
            # embed = await safe_embed_images(embed, 'artwork')
            
            # Add artwork category info in footer
            authenticity = "Genuine" if artwork.genuine else "Fake"
            category_text = f"🎨 {authenticity} Artwork"
            if artwork.art_category:
                category_text += f" • {artwork.art_category}"
            embed.set_footer(text=category_text)
            
            # Add Nookipedia and refresh button
            view = get_combined_view(None, artwork.nookipedia_url, add_refresh=True, content_type="artwork")
            
            if view:
                view.message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            else:
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in artwork command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the artwork.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(ArtworkCommands(bot))
