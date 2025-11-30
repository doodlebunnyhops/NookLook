import discord
from discord.ext import commands
from discord import app_commands
import logging

from bot.services.acnh_service import NooklookService
from bot.ui.common import get_combined_view, LanguageSelectView
from bot.cogs.acnh.base import check_guild_ephemeral
from bot.cogs.acnh.autocomplete import fossil_name_autocomplete
from bot.repos.user_repo import UserRepository

logger = logging.getLogger(__name__)


class FossilCommands(commands.Cog):
    """ACNH fossil commands using nooklook database"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_repo = UserRepository()
    
    @property
    def service(self) -> NooklookService:
        """Get the shared NooklookService from the bot instance"""
        return self.bot.nooklook_service
    
    async def _check_new_user(self, interaction: discord.Interaction) -> bool:
        from bot.ui.common import check_new_user_language
        if await check_new_user_language(interaction, self.user_repo):
            return True
        return False


    @app_commands.command(name="fossil", description="Look up a specific ACNH fossil")
    @app_commands.describe(name="The fossil name to look up")
    @app_commands.autocomplete(name=fossil_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def fossil_command(self, interaction: discord.Interaction, name: str):
        """Look up a fossil by name"""
        user_id = getattr(interaction.user, 'id', 'unknown')
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        # Check if this is a new user - show language prompt first
        if await self._check_new_user(interaction):
            return
        
        try:
            logger.info(f"fossil command used by:\n\t{interaction.user.display_name} ({user_id})\n\tsearching for: '{name}'")
            
            # Convert name to fossil ID if it's numeric (from autocomplete)
            if name.isdigit():
                fossil_id = int(name)
                fossil = await self.service.get_fossil_by_id(fossil_id)
            else:
                # Search for fossil by name using search_all with category filter
                search_results = await self.service.search_all(name, category_filter="fossil")
                fossil = search_results[0] if search_results else None
            
            if not fossil:
                embed = discord.Embed(
                    title="❌ Fossil Not Found",
                    description=f"Sorry, I couldn't find a fossil named **{name}** 🦴\n"
                               f"Try using `/search {name}` to see if there are similar names.",
                    color=0xe74c3c
                )
                
                # Add suggestion for fossil groups
                embed.add_field(
                    name="💡 Search Tips",
                    value="• Fossils are grouped into complete skeletons\n"
                          "• Some fossils are standalone pieces\n"
                          "• Try `/search` with partial names or fossil group names",
                    inline=False
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Create the fossil embed
            embed = fossil.to_discord_embed()
            # embed = await safe_embed_images(embed, 'fossil')
            
            # Add fossil info in footer
            footer_text = f"🦴 Museum Fossil"
            if fossil.fossil_group:
                footer_text += f" • {fossil.fossil_group}"
            embed.set_footer(text=footer_text)
            
            # Add Nookipedia and refresh button
            view = get_combined_view(
                None, fossil.nookipedia_url, 
                add_refresh=True, content_type="fossil",
                stash_info={'ref_table': 'fossils', 'ref_id': fossil.id, 'display_name': fossil.name}
            )
            
            logger.info(f"found fossil: {fossil.name}")
            if view:
                view.message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            else:
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"❌ Error in /fossil command for user {user_id}, query '{name}': {e}", exc_info=True)
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the fossil.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(FossilCommands(bot))
