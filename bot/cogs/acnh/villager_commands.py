import discord
from discord.ext import commands
from discord import app_commands
import logging

from bot.services.acnh_service import NooklookService
from bot.ui.common import get_combined_view
from bot.ui.detail_views import VillagerDetailsView
from bot.cogs.acnh.base import check_guild_ephemeral
from bot.cogs.acnh.autocomplete import villager_name_autocomplete

logger = logging.getLogger(__name__)


class VillagerCommands(commands.Cog):
    """ACNH villager commands using nooklook database"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @property
    def service(self) -> NooklookService:
        """Get the shared NooklookService from the bot instance"""
        return self.bot.nooklook_service

    @app_commands.command(name="villager", description="Look up a specific ACNH villager")
    @app_commands.describe(name="The villager name to look up")
    @app_commands.autocomplete(name=villager_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def villager(self, interaction: discord.Interaction, name: str):
        """Look up villager details"""
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)

        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"villager command used by:\n\t{interaction.user.display_name} ({user_id})\n\tin {guild_name or 'Unknown Guild'}\n\tsearching for: '{name}'")
        
        try:
            # Convert name to villager ID if it's numeric (from autocomplete)
            if name.isdigit():
                villager_id = int(name)
                villager = await self.service.get_villager_by_id(villager_id)
            else:
                # Search for villager by name
                search_results = await self.service.search_all(name, category_filter="villagers")
                villagers = [r for r in search_results if hasattr(r, 'species')]  # Filter for villagers
                villager = villagers[0] if villagers else None
            
            if not villager:
                embed = discord.Embed(
                    title="❌ Villager Not Found",
                    description=f"Sorry, I couldn't find a villager named **{name}** 😿\n"
                               f"Try using `/search {name}` to see if there are similar names.",
                    color=0xe74c3c
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            logger.info(f"found villager: {villager.name} ({villager.species})")
            
            # Create the main villager embed
            embed = villager.to_discord_embed()
            
            # Create view with details buttons and Nookipedia link
            view = VillagerDetailsView(villager, interaction.user, self.service)
            get_combined_view(view, villager.nookipedia_url)  # Adds Nookipedia button in-place
            
            # Send and store message reference for timeout handling
            view.message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in villager command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the villager.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(VillagerCommands(bot))