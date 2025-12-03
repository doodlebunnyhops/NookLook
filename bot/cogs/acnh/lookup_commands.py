import discord
from discord.ext import commands
from discord import app_commands
import logging

from bot.services.acnh_service import NooklookService
from bot.ui.item_views import VariantSelectView
from bot.ui.search_views import PaginatedResultView
from bot.ui.common import get_combined_view
from bot.cogs.acnh.base import check_guild_ephemeral
from bot.cogs.acnh.autocomplete import item_name_autocomplete
from bot.repos.user_repo import UserRepository
from bot.ui.common import check_new_user_language

logger = logging.getLogger(__name__)


class LookupCommands(commands.Cog):
    """ACNH lookup commands using nooklook database"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_repo = UserRepository()
    
    @property
    def service(self) -> NooklookService:
        """Get the shared NooklookService from the bot instance"""
        return self.bot.nooklook_service
    
    async def _check_new_user(self, interaction: discord.Interaction) -> bool:
        """Check if user is new and show language selection prompt.
        
        Returns True if prompt was shown (caller should return early),
        False if user has settings (continue normally).
        """
        return await check_new_user_language(interaction, self.user_repo)
    
    @app_commands.command(name="lookup", description="Look up a specific ACNH item")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
    @app_commands.describe(item="Item name to look up")
    @app_commands.autocomplete(item=item_name_autocomplete)
    async def lookup(self, interaction: discord.Interaction, item: str):
        """Look up a specific item with autocomplete"""
        # Check if this is a new user - show language prompt first (before defer for ephemeral)
        if await self._check_new_user(interaction):
            return  # Language prompt shown, user can run command again after selecting
        
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)

        user_id = interaction.user.id
        
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"lookup command used by:\n\t{interaction.user.display_name} ({user_id})\n\tin {guild_name or 'Unknown Guild'}\n\tsearching for: '{item}'")
        
        # Get user's preferred language
        user_language = await self.service.get_user_language(user_id)
        
        try:
            # Check if item is an ID (from autocomplete) or name (typed manually)
            if item.isdigit():
                # Direct lookup by ID from autocomplete selection
                result = await self.service.get_item_by_id(int(item))
                if result:
                    results = [result]
                else:
                    results = []
            else:
                # Fallback to search by name for manually typed entries
                # Use translation-aware search
                results = await self.service.search_all(
                    item, 
                    category_filter="items",
                    user_id=interaction.user.id
                )
            
            if not results:
                embed = discord.Embed(
                    title="🔍 No Results",
                    description=f"No items found matching '{item}'",
                    color=0xe74c3c
                )
                logger.info(f"Lookup: no results found for '{item}'")
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # If exactly one result, show detailed view with variant selector
            if len(results) == 1:
                result = results[0]
                logger.info(f"Lookup: found 1 result for '{result.name if hasattr(result, 'name') else item}'")
                
                # Get localized name for the title
                localized_name = await self.service.get_localized_item_name(
                    result.id, user_id, result.name
                )
                
                if hasattr(result, 'variants') and result.variants:
                    # Multiple variants - show selector (shorter timeout for direct lookup)
                    # Pass localized_name to view so it persists on refresh/timeout
                    view = VariantSelectView(result, interaction.user, timeout=60, language=user_language, localized_name=localized_name)
                    embed = view.create_embed()  # Use view's create_embed to get consistent title
                    # Add action buttons in correct order: Stash → Refresh → Nookipedia
                    view.add_action_buttons(result.nookipedia_url)
                    
                    # Send and store message reference for timeout handling
                    view.message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
                else:
                    # Single item - show directly
                    embed = result.to_discord_embed(language=user_language)
                    # Update title with localized name
                    if localized_name != result.name:
                        embed.title = f"{localized_name} ({result.name})"
                    view = get_combined_view(
                        None, result.nookipedia_url, add_refresh=True, content_type="item",
                        stash_info={"ref_table": "items", "ref_id": result.id, "display_name": result.name},
                        language=user_language
                    )
                    if view:
                        view.message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
                    else:
                        await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Multiple results - show search-style list with pagination
            embed = discord.Embed(
                title=f"🔍 Lookup Results for '{item}'",
                color=0x3498db
            )
            
            # Create paginated view for multiple results (shorter timeout for direct lookup)
            paginated_view = PaginatedResultView(results, embed_title=f"🔍 Lookup Results for '{item}'", timeout=60)
            embed = paginated_view.create_page_embed()
            
            # Send the message and store it in the view for timeout handling
            message = await interaction.followup.send(embed=embed, view=paginated_view, ephemeral=ephemeral)
            
            # Store the message in the paginated view for timeout handling
            paginated_view.message = message
            
        except Exception as e:
            logger.error(f"Error in lookup command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the item.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(LookupCommands(bot))
