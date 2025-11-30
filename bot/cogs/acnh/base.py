"""Base ACNH cog with shared utilities"""
import discord
from discord.ext import commands
import logging

from bot.services.acnh_service import NooklookService
from bot.utils.autocomplete_cache import autocomplete_cache

logger = logging.getLogger(__name__)

async def check_guild_ephemeral(interaction: discord.Interaction) -> bool:
    """Check if the guild has ephemeral responses enabled
    
    Logic:
    - DM (no guild): NOT ephemeral (False) - public responses in DMs
    - Guild without bot installed: ephemeral (True) - private for safety
    - Guild with bot installed: use settings
    - Default/error: ephemeral (True) - safe fallback
    """
    # DM - always public responses
    if interaction.guild is None:
        return False  # NOT ephemeral - public responses in DMs
    
    try:
        # Access the server repository from the bot instance
        server_repo = getattr(interaction.client, 'server_repo', None)
        if not server_repo:
            # No server repo available - bot not properly installed
            logger.debug("ServerRepository not available, defaulting to ephemeral responses")
            return True  # Ephemeral for safety
        
        # Check if guild settings exist (don't create if they don't exist)
        settings = await server_repo.get_guild_settings_if_exists(interaction.guild.id)
        if settings is None:
            # No settings exist - bot not properly installed in this guild
            logger.debug(f"No guild settings found for guild {interaction.guild.id}, defaulting to ephemeral responses")
            return True  # Ephemeral - bot not installed
        
        # Guild has bot installed - use the configured setting
        ephemeral_setting = settings.get('ephemeral_responses', False)
        logger.debug(f"Guild {interaction.guild.id} ephemeral setting: {ephemeral_setting}")
        return ephemeral_setting
        
    except Exception as e:
        logger.error(f"Error checking guild ephemeral setting for guild {interaction.guild.id}: {e}")
        return True  # Default to ephemeral on error for safety

class ACNHBaseCog(commands.Cog):
    """Base class for ACNH commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.service = NooklookService()
        bot.nooklook_service = self.service
    
    async def cog_load(self):
        try:
            await self.service.init_database()
            logger.info("ACNH database validated and ready")
        except FileNotFoundError as e:
            logger.error(f"Database not found: {e}")
            raise
        except RuntimeError as e:
            logger.error(f"Database validation failed: {e}")
            raise
    
    async def cog_unload(self):
        """Cleanup when cog unloads"""
        # Log detailed cache statistics before clearing
        stats = autocomplete_cache.get_cache_stats()
        logger.info(f"Final Cache Stats - Size: {stats['cache_size']}, Hits: {stats['total_hits']}, Rate: {stats['hit_rate']}")
        if stats['popular_queries']:
            top_query = stats['popular_queries'][0]
            logger.info(f"Most popular query: '{top_query[0]}' ({top_query[1]} hits)")
        autocomplete_cache.clear()
        
        # Remove service reference from bot
        if hasattr(self.bot, 'nooklook_service'):
            delattr(self.bot, 'nooklook_service')
            logger.info("NooklookService reference removed from bot")


async def setup(bot: commands.Bot):
    """Setup function for the cog - LOAD THIS FIRST"""
    await bot.add_cog(ACNHBaseCog(bot))