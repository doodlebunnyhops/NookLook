import discord
from discord.ext import commands
from discord import app_commands
import logging

from bot.services.acnh_service import NooklookService
from bot.ui.detail_views import CritterAvailabilityView
from bot.ui.common import LanguageSelectView
from bot.cogs.acnh.base import check_guild_ephemeral
from bot.cogs.acnh.autocomplete import critter_name_autocomplete
from bot.repos.user_repo import UserRepository
from bot.utils.localization import get_ui, translate_critter_detail, translate_critter_detail

logger = logging.getLogger(__name__)


class CritterCommands(commands.Cog):
    """ACNH critter commands using nooklook database"""
    
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

    @app_commands.command(name="critter", description="Look up a specific ACNH critter (fish, bug, or sea creature)")
    @app_commands.describe(name="The critter name to look up")
    @app_commands.autocomplete(name=critter_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def critter(self, interaction: discord.Interaction, name: str):
        """Look up critter details"""
        # Check if this is a new user - show language prompt first (before defer for ephemeral)
        if await self._check_new_user(interaction):
            return
        
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)

        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"critter command used by:\n\t{interaction.user.display_name} ({user_id})\n\tin {guild_name or 'Unknown Guild'}\n\tsearching for: '{name}'")
        
        try:
            # Convert name to critter ID if it's numeric (from autocomplete)
            if name.isdigit():
                critter_id = int(name)
                critter = await self.service.get_critter_by_id(critter_id)
            else:
                # Search for critter by name
                search_results = await self.service.search_all(name, category_filter="critters")
                critter = search_results[0] if search_results else None
            
            if not critter:
                embed = discord.Embed(
                    title="❌ Critter Not Found",
                    description=f"Sorry, I couldn't find a critter named **{name}** 😿\n"
                               f"Try using `/search {name}` to see if there are similar names.",
                    color=0xe74c3c
                )
                
                # Add suggestion for different critter types
                embed.add_field(
                    name="💡 Search Tips",
                    value="• Fish: Found in rivers, ponds, and the sea\n"
                          "• Bugs: Found around flowers, trees, and rocks\n"
                          "• Sea Creatures: Found while diving in the ocean\n"
                          "• Try `/search` with partial names or locations",
                    inline=False
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Get user's preferred language
            language = await self.service.get_user_language(user_id)
            ui = get_ui(language)
            
            # Create the critter embed with localization
            embed = critter.to_discord_embed(language=language)
            
            # Get localized critter name if available
            localized_name = await self.service.get_localized_critter_name(
                critter.id, user_id, critter.name
            )
            if localized_name != critter.name:
                embed.title = f"{localized_name} ({critter.name})"
            
            # Add critter type info in footer (localized)
            critter_type = critter.get_type_display(language)
            
            footer_text = f"{critter_type}"
            if critter.location:
                footer_text += f" • {translate_critter_detail(critter.location, language) or critter.location}"
            embed.set_footer(text=footer_text)
            
            # Create view with buttons in correct order: Availability → Stash → Refresh → Nookipedia
            view = CritterAvailabilityView(critter, interaction.user, language=language)
            view.add_details_action_buttons(critter.nookipedia_url)
            
            logger.info(f"found critter: {critter.name}")
            
            # Send and store message reference for timeout handling
            view.message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"❌ Error in /critter command for user {user_id}, query '{name}': {e}", exc_info=True)
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the critter.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(CritterCommands(bot))
