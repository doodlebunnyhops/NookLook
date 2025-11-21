"""Modern ACNH Discord commands using the new nooklook database"""

import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, List
import logging

from bot.services.acnh_service import NooklookService
from bot.ui.pagination import (
    ItemsPaginationView, 
    CrittersPaginationView, 
    VariantSelectView,
    SearchResultsView,
    PaginatedResultView
)
from bot.ui.nookipedia_view import get_nookipedia_view
# from bot.utils.image_fallback import safe_set_image, safe_set_thumbnail
import asyncio
from functools import lru_cache
import time

logger = logging.getLogger(__name__)

# async def safe_embed_images(embed: discord.Embed, content_type: str = 'general') -> discord.Embed:
#     """Not actually for safe checking, but helps cdn load times to discord to prevent images not loading."""
#     from bot.utils.image_fallback import is_valid_url
    
#     # Check if embed has an image and make it safe
#     if embed.image and embed.image.url:
#         original_url = embed.image.url
#         if is_valid_url(original_url):
#             embed = await safe_set_image(embed, original_url, content_type)
#         else:
#             # Remove invalid image URL to prevent Discord API error
#             embed.set_image(url=discord.Embed.Empty)
#             logger.warning(f"Removed invalid image URL from embed: {original_url}")
    
#     # Check if embed has a thumbnail and make it safe
#     if embed.thumbnail and embed.thumbnail.url:
#         original_url = embed.thumbnail.url
#         if is_valid_url(original_url):
#             embed = await safe_set_thumbnail(embed, original_url, content_type)
#         else:
#             # Remove invalid thumbnail URL to prevent Discord API error
#             embed.set_thumbnail(url=discord.Embed.Empty)
#             logger.warning(f"Removed invalid thumbnail URL from embed: {original_url}")
        
#     return embed

class AutocompleteCache:
    """Efficient cache for autocomplete results with smart optimizations"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 300, random_ttl: int = 60):  # 1 minute random TTL
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
        self.random_ttl = random_ttl  # Shorter TTL for random results
        self.access_times = {}
        self.random_pools = {}  # Store multiple random result sets
        self.random_rotation_times = {}  # Track when to rotate random sets
        
        # Enhanced caching features
        self.prefix_cache = {}  # Cache for prefix-based lookups
        self.hit_counts = {}    # Track cache hit frequency
        self.query_patterns = {}  # Track common query patterns
    
    def _cleanup_expired(self):
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self.access_times.items()
            if current_time - timestamp > self._get_ttl_for_key(key)
        ]
        if expired_keys:
            logger.debug(f"Cache cleanup: removing {len(expired_keys)} expired entries")
        for key in expired_keys:
            self.cache.pop(key, None)
            self.access_times.pop(key, None)
            # Clean up random pool tracking
            if key in self.random_rotation_times:
                self.random_rotation_times.pop(key, None)
    
    def _get_ttl_for_key(self, key: str) -> int:
        """Get TTL based on key type"""
        return self.random_ttl if ':random' in key else self.ttl
    
    def _make_room(self):
        """Remove oldest entries if cache is full"""
        if len(self.cache) >= self.max_size:
            # Remove 20% of oldest entries
            to_remove = max(1, len(self.cache) // 5)
            oldest_keys = sorted(self.access_times.items(), key=lambda x: x[1])[:to_remove]
            logger.info(f"Cache full ({len(self.cache)} entries), evicting {to_remove} oldest entries")
            for key, _ in oldest_keys:
                self.cache.pop(key, None)
                self.access_times.pop(key, None)
    
    def get(self, key: str):
        """Get cached value if not expired with smart optimizations"""
        self._cleanup_expired()
        
        # Normalize key for consistent caching
        normalized_key = self._normalize_key(key)
        
        # Special handling for random keys
        if ':random' in normalized_key:
            return self._get_random_result(normalized_key)
        
        # Try exact match first
        if normalized_key in self.cache:
            self.access_times[normalized_key] = time.time()
            self.hit_counts[normalized_key] = self.hit_counts.get(normalized_key, 0) + 1
            logger.info(f"Cache HIT for key: {normalized_key} (hits: {self.hit_counts[normalized_key]})")
            return self.cache[normalized_key]
        
        # Try prefix matching for progressive typing
        prefix_result = self._try_prefix_match(normalized_key)
        if prefix_result:
            return prefix_result
            
        logger.debug(f"Cache MISS for key: {normalized_key}")
        return None
    
    def _normalize_key(self, key: str) -> str:
        """Normalize cache keys for consistency"""
        if ':' in key:
            prefix, query = key.split(':', 1)
            # Normalize the query part - trim whitespace, lowercase
            normalized_query = query.strip().lower()
            return f"{prefix}:{normalized_query}"
        return key.strip().lower()
    
    def _try_prefix_match(self, key: str) -> any:
        """Try to find results from cached longer queries"""
        if ':' not in key:
            return None
            
        prefix, query = key.split(':', 1)
        
        # Look for cached results from longer queries that start with this query
        for cached_key, cached_result in self.cache.items():
            if not cached_key.startswith(f"{prefix}:"):
                continue
                
            _, cached_query = cached_key.split(':', 1)
            
            # If cached query starts with our query and is longer
            if cached_query.startswith(query) and len(cached_query) > len(query):
                # Filter the cached results to match our shorter query
                filtered_results = self._filter_results_for_query(cached_result, query)
                if filtered_results:
                    logger.info(f"Cache PREFIX HIT: '{key}' found via '{cached_key}' ({len(filtered_results)} results)")
                    # Cache this result for future use
                    self.cache[key] = filtered_results
                    self.access_times[key] = time.time()
                    return filtered_results
        
        return None
    
    def _filter_results_for_query(self, results, query: str):
        """Filter autocomplete results to match a shorter query"""
        if not results or not query:
            return results
            
        # Filter choices that contain the query
        filtered = []
        for choice in results:
            if hasattr(choice, 'name') and query.lower() in choice.name.lower():
                filtered.append(choice)
            elif isinstance(choice, dict) and 'name' in choice and query.lower() in choice['name'].lower():
                filtered.append(choice)
                
        return filtered[:25]  # Maintain Discord's 25-item limit
    
    def _get_random_result(self, key: str):
        """Handle random result caching with rotation"""
        current_time = time.time()
        
        # Check if we have a fresh random result
        if key in self.cache and key in self.access_times:
            age = current_time - self.access_times[key]
            if age < self.random_ttl:
                logger.info(f"Cache HIT for random key: {key} (age: {age:.1f}s)")
                return self.cache[key]
            else:
                logger.debug(f"Random cache EXPIRED for key: {key} (age: {age:.1f}s)")
        
        logger.debug(f"Random cache MISS for key: {key}")
        return None
    
    def set(self, key: str, value):
        """Cache a value with normalization"""
        self._cleanup_expired()
        self._make_room()
        
        # Normalize the key
        normalized_key = self._normalize_key(key)
        
        self.cache[normalized_key] = value
        self.access_times[normalized_key] = time.time()
        self.hit_counts[normalized_key] = 0  # Initialize hit counter
        
        # Track query patterns for analytics
        if ':' in normalized_key:
            prefix, query = normalized_key.split(':', 1)
            if len(query) >= 2:  # Only track meaningful queries
                self.query_patterns[prefix] = self.query_patterns.get(prefix, 0) + 1
        
        ttl_type = "random" if ':random' in normalized_key else "regular"
        ttl_value = self._get_ttl_for_key(normalized_key)
        logger.debug(f"Cache SET for key: {normalized_key} ({ttl_type} TTL: {ttl_value}s, cache size: {len(self.cache)})")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.access_times.clear()
        self.random_pools.clear()
        self.random_rotation_times.clear()
        self.prefix_cache.clear()
        self.hit_counts.clear()
        self.query_patterns.clear()
    
    def get_cache_stats(self) -> dict:
        """Get comprehensive cache statistics"""
        total_hits = sum(self.hit_counts.values())
        cache_size = len(self.cache)
        
        # Find most popular queries
        popular_queries = sorted(self.hit_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Query pattern stats
        pattern_stats = dict(sorted(self.query_patterns.items(), key=lambda x: x[1], reverse=True))
        
        return {
            'cache_size': cache_size,
            'total_hits': total_hits,
            'hit_rate': f"{(total_hits / max(cache_size, 1)) * 100:.1f}%",
            'popular_queries': popular_queries,
            'query_patterns': pattern_stats,
            'max_size': self.max_size,
            'utilization': f"{(cache_size / self.max_size) * 100:.1f}%"
        }

# Global cache instance with 1-minute random TTL for freshness
_autocomplete_cache = AutocompleteCache(max_size=1000, ttl=300, random_ttl=60)

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
    

def is_dm(interaction: discord.Interaction) -> bool:
    """Check if interaction is in a DM or Group DM (both have guild=None)"""
    return interaction.guild is None

async def villager_name_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for villager names with caching"""
    user_id = getattr(interaction.user, 'id', 'unknown')
    logger.debug(f"Villager autocomplete called by user {user_id} with query: '{current}'")
    
    try:
        # Normalize query for consistent caching
        query = current.lower().strip()
        cache_key = f"villager:{query}"
        
        # Check cache first
        cached_result = _autocomplete_cache.get(cache_key)
        if cached_result:
            logger.debug(f"Villager autocomplete: returning {len(cached_result)} cached results for '{query}'")
            return cached_result
            
        # Get service from bot instance
        service = getattr(interaction.client, 'nooklook_service', None)
        if not service:
            logger.error("Villager autocomplete: NooklookService not found on bot instance")
            return []
        
        # Get villager suggestions
        logger.debug(f"Villager autocomplete: searching database for '{current}'")
        suggestions = await service.get_villager_suggestions(current)
        choices = [
            app_commands.Choice(name=name, value=str(villager_id))
            for name, villager_id in suggestions[:25]
        ]
        
        logger.info(f"Villager autocomplete: found {len(choices)} results for '{current}', caching...")
        # Cache the result
        _autocomplete_cache.set(cache_key, choices)
        return choices
        
    except Exception as e:
        logger.error(f"Error in villager autocomplete for user {user_id}, query '{current}': {e}", exc_info=True)
        return []

async def recipe_name_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for recipe names with caching"""
    user_id = getattr(interaction.user, 'id', 'unknown')
    logger.debug(f"Recipe autocomplete called by user {user_id} with query: '{current}'")
    
    try:
        # Normalize query for consistent caching
        query = current.lower().strip()
        cache_key = f"recipe:{query}"
        
        # Check cache first
        cached_result = _autocomplete_cache.get(cache_key)
        if cached_result:
            logger.debug(f"Recipe autocomplete: returning {len(cached_result)} cached results for '{query}'")
            return cached_result
            
        # Get service from bot instance
        service = getattr(interaction.client, 'nooklook_service', None)
        if not service:
            logger.error("Recipe autocomplete: NooklookService not found on bot instance")
            return []
        
        # Get recipe suggestions
        if not query or len(query) <= 2:
            cache_key = "recipe:random"
            cached_result = _autocomplete_cache.get(cache_key)
            if cached_result:
                logger.debug(f"Recipe autocomplete: returning {len(cached_result)} cached random results")
                return cached_result
            logger.info("Recipe autocomplete: generating fresh random suggestions (1min cache)")
            suggestions = await service.get_random_recipe_suggestions(25)
        else:
            logger.debug(f"Recipe autocomplete: searching database for '{current}'")
            suggestions = await service.get_recipe_suggestions(current)
        
        # Convert to choices
        choices = [
            app_commands.Choice(name=name, value=str(recipe_id))
            for name, recipe_id in suggestions[:25]
        ]
        
        logger.info(f"Recipe autocomplete: found {len(choices)} results for '{current}', caching...")
        # Cache the result
        _autocomplete_cache.set(cache_key, choices)
        return choices

    except Exception as e:
        logger.error(f"Error in recipe autocomplete for user {user_id}, query '{current}': {e}", exc_info=True)
        return []

async def artwork_name_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for artwork names with caching"""
    user_id = getattr(interaction.user, 'id', 'unknown')
    logger.debug(f"Artwork autocomplete called by user {user_id} with query: '{current}'")
    
    try:
        # Normalize query for consistent caching
        query = current.lower().strip()
        cache_key = f"artwork:{query}"
        
        # Check cache first
        cached_result = _autocomplete_cache.get(cache_key)
        if cached_result:
            logger.debug(f"Artwork autocomplete: returning {len(cached_result)} cached results for '{query}'")
            return cached_result
            
        # Get service from bot instance
        service = getattr(interaction.client, 'nooklook_service', None)
        if not service:
            logger.error("Artwork autocomplete: NooklookService not found on bot instance")
            return []
        
        # Get artwork suggestions
        if not query or len(query) <= 2:
            cache_key = "artwork:random"
            cached_result = _autocomplete_cache.get(cache_key)
            if cached_result:
                logger.debug(f"Artwork autocomplete: returning {len(cached_result)} cached random results")
                return cached_result
            logger.info("Artwork autocomplete: generating fresh random suggestions (1min cache)")
            suggestions = await service.get_random_artwork_suggestions(25)
        else:
            logger.debug(f"Artwork autocomplete: searching database for '{current}'")
            suggestions = await service.get_artwork_suggestions(current)
        
        # Convert to choices
        choices = [
            app_commands.Choice(name=name, value=str(artwork_id))
            for name, artwork_id in suggestions[:25]
        ]
        
        logger.info(f"Artwork autocomplete: found {len(choices)} results for '{current}', caching...")
        # Cache the result
        _autocomplete_cache.set(cache_key, choices)
        return choices

    except Exception as e:
        logger.error(f"Error in artwork autocomplete for user {user_id}, query '{current}': {e}", exc_info=True)
        return []

async def critter_name_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for critter names with caching"""
    user_id = getattr(interaction.user, 'id', 'unknown')
    logger.debug(f"Critter autocomplete called by user {user_id} with query: '{current}'")
    
    try:
        # Normalize query for consistent caching
        query = current.lower().strip()
        cache_key = f"critter:{query}"
        
        # Check cache first
        cached_result = _autocomplete_cache.get(cache_key)
        if cached_result:
            logger.debug(f"Critter autocomplete: returning {len(cached_result)} cached results for '{query}'")
            return cached_result
        
        # Get service from bot instance
        service = getattr(interaction.client, 'nooklook_service', None)
        if not service:
            logger.error("Critter autocomplete: NooklookService not found on bot instance")
            return []
        
        # Get critter suggestions
        if not query or len(query) <= 2:
            # Use a consistent cache key for random suggestions
            cache_key = "critter:random"
            cached_result = _autocomplete_cache.get(cache_key)
            if cached_result:
                logger.debug(f"Critter autocomplete: returning {len(cached_result)} cached random results")
                return cached_result
            logger.info("Critter autocomplete: generating fresh random suggestions (1min cache)")
            suggestions = await service.get_random_critter_suggestions(25)
        else:
            logger.debug(f"Critter autocomplete: searching database for '{current}'")
            suggestions = await service.get_critter_suggestions(current)
        
        # Convert to choices
        choices = [
            app_commands.Choice(name=name, value=str(critter_id))
            for name, critter_id in suggestions[:25]
        ]
        
        logger.info(f"Critter autocomplete: found {len(choices)} results for '{current}', caching...")
        # Cache the result
        _autocomplete_cache.set(cache_key, choices)
        return choices
        
    except Exception as e:
        logger.error(f"Error in critter autocomplete for user {user_id}, query '{current}': {e}", exc_info=True)
        return []

async def fossil_name_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for fossil names with caching"""
    user_id = getattr(interaction.user, 'id', 'unknown')
    logger.debug(f"Fossil autocomplete called by user {user_id} with query: '{current}'")
    
    try:
        # Use cache with fossil-specific key
        cache_key = f"fossil_autocomplete:{current.lower()}"
        cached_results = _autocomplete_cache.get(cache_key)
        
        if cached_results is not None:
            logger.debug(f"Fossil autocomplete cache hit for user {user_id}, query '{current}' - returning {len(cached_results)} results")
            return cached_results[:25]  # Discord limit
        
        # Get service from bot
        if not hasattr(interaction.client, 'nooklook_service'):
            logger.warning("Nooklook service not available for fossil autocomplete")
            return []
        
        service = interaction.client.nooklook_service
        
        # Search fossils specifically using category filter
        results = await service.search_all(current, category_filter="fossil")
        
        # Create choices with fossil ID for exact lookup
        choices = []
        for fossil in results[:25]:  # Discord autocomplete limit
            choice_name = fossil.name
            if fossil.fossil_group and fossil.fossil_group != fossil.name:
                choice_name += f" ({fossil.fossil_group})"
            
            # Truncate if too long for Discord
            if len(choice_name) > 100:
                choice_name = choice_name[:97] + "..."
            
            choices.append(app_commands.Choice(
                name=choice_name,
                value=str(fossil.id)
            ))
        
        # Cache the results
        _autocomplete_cache.set(cache_key, choices)
        
        logger.debug(f"Fossil autocomplete for user {user_id}, query '{current}' - found {len(choices)} results")
        return choices
        
    except Exception as e:
        logger.error(f"Error in fossil autocomplete for user {user_id}, query '{current}': {e}", exc_info=True)
        return []

class SimpleRefreshView(discord.ui.View):
    """Simple view with just a refresh images button for static content"""
    
    def __init__(self, content_type: str = "content"):
        super().__init__(timeout=10)
        self.content_type = content_type
        self.message = None
        self.last_refresh_time = 0  # Track last refresh to prevent spam
        
    @discord.ui.button(label="🔄 Refresh Images", style=discord.ButtonStyle.secondary)
    async def refresh_images(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Refresh images by re-editing the message"""
        try:
            # Check cooldown (3 seconds minimum between refreshes)
            import time
            current_time = time.time()
            if current_time - self.last_refresh_time < 10:
                remaining = int(10 - (current_time - self.last_refresh_time))
                await interaction.response.send_message(f"Please wait {remaining} more second(s) before refreshing again.", ephemeral=True)
                return
            
            # Update last refresh time
            self.last_refresh_time = current_time
            
            # Get the current embed
            if not interaction.message.embeds:
                await interaction.response.send_message("❌ No content to refresh", ephemeral=True)
                return
                
            embed = interaction.message.embeds[0]
            
            # Add refresh indicator temporarily
            original_footer = embed.footer.text if embed.footer else ""
            if "🔄 Images refreshed" not in original_footer:
                new_footer = f"{original_footer} | 🔄 Images refreshed" if original_footer else "🔄 Images refreshed"
                embed.set_footer(text=new_footer)
            
            # Edit the message to force Discord to re-fetch images
            await interaction.response.edit_message(embed=embed, view=self)
            
            # After a delay, restore the original footer
            import asyncio
            await asyncio.sleep(2)
            
            try:
                if original_footer:
                    embed.set_footer(text=original_footer)
                else:
                    embed.set_footer(text=discord.Embed.Empty)
                
                if self.message:
                    await self.message.edit(embed=embed, view=self)
            except:
                pass  # Ignore errors if message was deleted
                
        except Exception as e:
            logger.error(f"Error refreshing {self.content_type} images: {e}")
            try:
                await interaction.response.send_message("❌ Failed to refresh images", ephemeral=True)
            except:
                pass
    
    async def on_timeout(self):
        """Disable buttons when view times out"""
        for item in self.children:
            if isinstance(item, discord.ui.Button) and item.style != discord.ButtonStyle.link:
                item.disabled = True
        
        if self.message:
            try:
                await self.message.edit(view=self)
            except:
                pass

def get_combined_view(existing_view: Optional[discord.ui.View], nookipedia_url: Optional[str], add_refresh: bool = False, content_type: str = "content") -> Optional[discord.ui.View]:
    """Combine an existing view with Nookipedia button if URL is available"""
    nookipedia_view = get_nookipedia_view(nookipedia_url)
    
    # If we need to add refresh but have no existing view, create a simple one
    if add_refresh and not existing_view:
        existing_view = SimpleRefreshView(content_type)
    
    if existing_view and nookipedia_view:
        # Add Nookipedia button to existing view
        for item in nookipedia_view.children:
            existing_view.add_item(item)
        return existing_view
    elif nookipedia_view and not add_refresh:
        # Only Nookipedia button and no refresh needed
        return nookipedia_view
    elif nookipedia_view and add_refresh:
        # Create view with both nookipedia and refresh
        refresh_view = SimpleRefreshView(content_type)
        for item in nookipedia_view.children:
            refresh_view.add_item(item)
        return refresh_view
    else:
        # Return existing view or None
        return existing_view

class ACNHCommands(commands.Cog):
    """ACNH lookup commands using nooklook database"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.service = NooklookService()
        
        # Store service in bot for easy access from autocomplete functions
        bot.nooklook_service = self.service
        
    async def cog_load(self):
        """Initialize the database when cog loads"""
        try:
            await self.service.init_database()
            logger.info("ACNH database initialized successfully")
            logger.info(f"Autocomplete cache initialized (max_size: {_autocomplete_cache.max_size}, regular_ttl: {_autocomplete_cache.ttl}s, random_ttl: {_autocomplete_cache.random_ttl}s)")
        except Exception as e:
            logger.error(f"Failed to initialize ACNH database: {e}", exc_info=True)
    
    async def cog_unload(self):
        """Cleanup when cog unloads"""
        # Log detailed cache statistics before clearing
        stats = _autocomplete_cache.get_cache_stats()
        logger.info(f"Final Cache Stats - Size: {stats['cache_size']}, Hits: {stats['total_hits']}, Rate: {stats['hit_rate']}")
        if stats['popular_queries']:
            top_query = stats['popular_queries'][0]
            logger.info(f"Most popular query: '{top_query[0]}' ({top_query[1]} hits)")
        
        _autocomplete_cache.clear()
        
        # Remove service reference from bot
        if hasattr(self.bot, 'nooklook_service'):
            delattr(self.bot, 'nooklook_service')
            logger.info("NooklookService reference removed from bot")
    
    @app_commands.command(name="search", description="Search across all ACNH content")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
    @app_commands.describe(
        query="What to search for (exact phrase matching)",
        category="Limit search to specific content type"
    )
    @app_commands.choices(category=[
        app_commands.Choice(name="Items", value="items"),
        app_commands.Choice(name="Critters", value="critters"),
        app_commands.Choice(name="Fossils", value="fossils"),
        app_commands.Choice(name="Food Recipes", value="food_recipes"),
        app_commands.Choice(name="DIY Recipes", value="diy_recipes"),
        app_commands.Choice(name="Ceiling Decor", value="ceiling-decor"),
        app_commands.Choice(name="Wall Mounted", value="wall-mounted"),
        app_commands.Choice(name="Villagers", value="villagers")
    ])
    async def search(self, interaction: discord.Interaction, 
                    query: str, category: Optional[str] = None):
        """Search across all ACNH content using FTS5"""
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)

        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        category_str = f" in {category}" if category else ""
        logger.info(f"🔍 /search command used by {interaction.user.display_name} ({user_id}) in {guild_name or 'Unknown Guild'} - query: '{query}'{category_str}")
        
        try:
            # Map Discord choice values to database category values
            category_mapping = {
                "items": "item",           # Discord "items" -> DB "item"
                "critters": "critter",     # Discord "critters" -> DB "critter"  
                "food_recipes": "recipe",  # Discord "food_recipes" -> DB "recipe"
                "diy_recipes": "recipe",   # Discord "diy_recipes" -> DB "recipe"
                "villagers": "villager",   # Discord "villagers" -> DB "villager"
                "artwork": "artwork",      # Discord "artwork" -> DB "artwork"
                "fossils": "fossil",       # Discord "fossils" -> DB "fossil"
                "ceiling-decor": "item",   # Discord "ceiling-decor" -> DB "item" (subcategory)
                "wall-mounted": "item"     # Discord "wall-mounted" -> DB "item" (subcategory)
            }
            
            # Convert category to database format
            db_category = category_mapping.get(category) if category else None
            
            # Handle subcategories for different content types
            recipe_subtype = None
            item_subcategory = None
            
            # Recipe subcategories
            if category == "food_recipes":
                recipe_subtype = "food"
            elif category == "diy_recipes":
                recipe_subtype = "diy"
            
            # Item subcategories
            elif category == "ceiling-decor":
                item_subcategory = "ceiling-decor"
            elif category == "wall-mounted":
                item_subcategory = "wall-mounted"
            
            logger.debug(f"Search: executing search_all with query='{query}', category_filter='{db_category}', recipe_subtype='{recipe_subtype}', item_subcategory='{item_subcategory}' (Discord: '{category}')")
            
            results = await self.service.search_all(query, category_filter=db_category, recipe_subtype=recipe_subtype, item_subcategory=item_subcategory)
            logger.debug(f"Search: found {len(results) if results else 0} results with category filter")
            
            if not results:
                embed = discord.Embed(
                    title="🔍 No Results Found",
                    description=f"No results found for '{query}'",
                    color=0xe74c3c
                )
                if category:
                    embed.description += f" in {category}"
                    logger.info(f"Search: no results for '{query}' in category '{category}'")
                
                embed.add_field(
                    name="💡 Search Tips",
                    value="• Use exact phrases for better results\n" +
                          "• Try different keywords\n" +
                          "• Check your spelling",
                    inline=False
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Single result - show detailed view
            if len(results) == 1:
                result = results[0]
                
                # If it's an item with variants, show variant selector
                if hasattr(result, 'variants') and len(result.variants) > 1:
                    variant_view = VariantSelectView(result, interaction.user)
                    embed = variant_view.create_embed()
                    # Add Nookipedia button to variant view
                    nookipedia_url = getattr(result, 'nookipedia_url', None)
                    view = get_combined_view(variant_view, nookipedia_url)
                    
                    # Send the message and store it in the view for timeout handling
                    message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
                    
                    # Store the message in the variant view for timeout handling
                    variant_view.message = message
                else:
                    # Show regular embed
                    embed = result.to_embed() if hasattr(result, 'to_embed') else discord.Embed(
                        title=getattr(result, 'name', 'Unknown'),
                        color=0x95a5a6
                    )
                    embed.title = f"🔍 {embed.title}"
                    embed.set_footer(text=f"Search result for '{query}'")
                    category_info = f" in {category}" if category else ""
                    logger.info(f"✅ /search command completed for user {user_id} - found 1 result for '{query}'{category_info}: {getattr(result, 'name', 'Unknown')}")
                    
                    # Add Nookipedia button if available
                    nookipedia_url = getattr(result, 'nookipedia_url', None)
                    view = get_combined_view(None, nookipedia_url)
                    await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
            # Multiple results - show navigation view
            else:
                view = SearchResultsView(results, query, interaction.user)
                embed = view.create_embed()
                category_info = f" in {category}" if category else ""
                logger.info(f"✅ /search command completed for user {user_id} - found {len(results)} results for '{query}'{category_info}")
                
                # Send the message and store it in the view for timeout handling
                message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
                
                # Store the message in the search view for timeout handling
                view.message = message
            
        except Exception as e:
            logger.error(f"Error in search: {e}")
            embed = discord.Embed(
                title="❌ Search Error",
                description="An error occurred while searching.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    async def item_name_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete for item names (base items only, no variants)"""
        user_id = getattr(interaction.user, 'id', 'unknown')
        logger.debug(f"Item autocomplete called by user {user_id} with query: '{current}'")

        try:
            if not current or len(current) <= 2:
                logger.debug(f"Item autocomplete: generating random items for user {user_id} (no cache for items)")
                # Show 25 random items when query is too short - no caching for true randomness
                base_items = await self.service.get_random_item_suggestions(25)
            else:
                logger.debug(f"Item autocomplete: searching database for '{current}' (user {user_id})")
                # Get base item names and IDs using the service
                base_items = await self.service.get_base_item_suggestions(current)
            
            # Return up to 25 choices for autocomplete using item IDs as values
            choices = [
                app_commands.Choice(name=item_name, value=str(item_id))
                for item_name, item_id in base_items[:25]
            ]
            logger.debug(f"Item autocomplete: found {len(choices)} results for '{current}' (user {user_id})")
            return choices

        except Exception as e:
            logger.error(f"Error in item_name_autocomplete for user {user_id}, query '{current}': {e}", exc_info=True)
            return []

    @app_commands.command(name="lookup", description="Look up a specific ACNH item")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
    @app_commands.describe(item="Item name to look up")
    @app_commands.autocomplete(item=item_name_autocomplete)
    async def lookup(self, interaction: discord.Interaction, item: str):
        """Look up a specific item with autocomplete"""
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)

        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"🔍 /lookup command used by {interaction.user.display_name} ({user_id}) in {guild_name or 'Unknown Guild'} - searching for: '{item}'")
        
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
                results = await self.service.search_all(item, category_filter="items")
            
            if not results:
                embed = discord.Embed(
                    title="🔍 No Results",
                    description=f"No items found matching '{item}'",
                    color=0xe74c3c
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # If exactly one result, show detailed view with variant selector
            if len(results) == 1:
                result = results[0]
                if hasattr(result, 'variants') and result.variants:
                    # Multiple variants - show selector
                    embed = result.to_discord_embed()
                    # embed = await safe_embed_images(embed, 'item')
                    variant_view = VariantSelectView(result, interaction.user)
                    # Add Nookipedia button to variant view
                    nookipedia_url = getattr(result, 'nookipedia_url', None)
                    view = get_combined_view(variant_view, nookipedia_url)
                    
                    # Send the message and store it in the view for timeout handling
                    message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
                    
                    # Store the message in the variant view for timeout handling
                    variant_view.message = message
                else:
                    # Single item - show directly
                    embed = result.to_discord_embed()
                    # embed = await safe_embed_images(embed, 'item')
                    # Add Nookipedia and refresh button if available
                    nookipedia_url = getattr(result, 'nookipedia_url', None)
                    view = get_combined_view(None, nookipedia_url, add_refresh=True, content_type="item")
                    message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
                    if view:
                        view.message = message
                return
            
            # Multiple results - show search-style list with pagination
            embed = discord.Embed(
                title=f"🔍 Lookup Results for '{item}'",
                color=0x3498db
            )
            
            # Create paginated view for multiple results
            paginated_view = PaginatedResultView(results, embed_title=f"🔍 Lookup Results for '{item}'")
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
        logger.info(f"👥 /villager command used by {interaction.user.display_name} ({user_id}) in {guild_name or 'Unknown Guild'} - searching for: '{name}'")
        
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
            
            # Create the main villager embed with extra details button
            embed = villager.to_discord_embed()
            # embed = await safe_embed_images(embed, 'villager')
            
            # Create a view with buttons for additional details and add Nookipedia button
            details_view = VillagerDetailsView(villager, interaction.user, self.service)
            nookipedia_url = getattr(villager, 'nookipedia_url', None)
            view = get_combined_view(details_view, nookipedia_url)
            
            # Send the message and store it in the view for timeout handling
            message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
            # Store the message in the details view for timeout handling
            details_view.message = message
            
        except Exception as e:
            logger.error(f"Error in villager command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the villager.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    @app_commands.command(name="recipe", description="Look up a specific ACNH recipe")
    @app_commands.describe(name="The recipe name to look up")
    @app_commands.autocomplete(name=recipe_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def recipe(self, interaction: discord.Interaction, name: str):
        """Look up recipe details"""
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)

        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"🍳 /recipe command used by {interaction.user.display_name} ({user_id}) in {guild_name or 'Unknown Guild'} - searching for: '{name}'")
        
        try:
            # Convert name to recipe ID if it's numeric (from autocomplete)
            if name.isdigit():
                recipe_id = int(name)
                recipe = await self.service.get_recipe_by_id(recipe_id)
            else:
                # Search for recipe by name
                search_results = await self.service.search_all(name, category_filter="recipes")
                recipe = search_results[0] if search_results else None
            
            if not recipe:
                embed = discord.Embed(
                    title="❌ Recipe Not Found",
                    description=f"Sorry, I couldn't find a recipe named **{name}** 😿\n"
                               f"Try using `/search {name}` to see if there are similar names.",
                    color=0xe74c3c
                )
                
                # Add suggestion for food vs DIY search
                embed.add_field(
                    name="💡 Search Tips",
                    value="• Food recipes: savory dishes, desserts, and drinks\n"
                          "• DIY recipes: furniture, tools, and decorations\n"
                          "• Try `/search` with partial names or ingredients",
                    inline=False
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Create the recipe embed
            embed = recipe.to_discord_embed()
            # embed = await safe_embed_images(embed, 'recipe')
            
            # Add recipe type info in footer
            recipe_type = "Food Recipe" if recipe.is_food() else "DIY Recipe"
            # embed.set_footer(text=f"{recipe_type} • {recipe.category or 'Unknown Category'}")
            
            # Add Nookipedia and refresh button if available
            nookipedia_url = getattr(recipe, 'nookipedia_url', None)
            view = get_combined_view(None, nookipedia_url, add_refresh=True, content_type="recipe")
            
            logger.info(f"✅ /recipe command completed successfully for user {user_id} - found: {recipe.name} ({recipe_type})")
            message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            if view:
                view.message = message
            
        except Exception as e:
            logger.error(f"❌ Error in /recipe command for user {user_id}, query '{name}': {e}", exc_info=True)
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the recipe.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    @app_commands.command(name="artwork", description="Look up a specific ACNH artwork")
    @app_commands.describe(name="The artwork name to look up")
    @app_commands.autocomplete(name=artwork_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def artwork(self, interaction: discord.Interaction, name: str):
        """Look up artwork details"""
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
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
            
            # Create the artwork embed
            embed = artwork.to_discord_embed()
            # embed = await safe_embed_images(embed, 'artwork')
            
            # Add artwork category info in footer
            authenticity = "Genuine" if artwork.genuine else "Fake"
            category_text = f"🎨 {authenticity} Artwork"
            if artwork.art_category:
                category_text += f" • {artwork.art_category}"
            embed.set_footer(text=category_text)
            
            # Add Nookipedia and refresh button if available
            nookipedia_url = getattr(artwork, 'nookipedia_url', None)
            view = get_combined_view(None, nookipedia_url, add_refresh=True, content_type="artwork")
            
            message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            if view:
                view.message = message
            
        except Exception as e:
            logger.error(f"Error in artwork command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the artwork.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)

    @app_commands.command(name="fossil", description="Look up a specific ACNH fossil")
    @app_commands.describe(name="The fossil name to look up")
    @app_commands.autocomplete(name=fossil_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def fossil_command(self, interaction: discord.Interaction, name: str):
        """Look up a fossil by name"""
        user_id = getattr(interaction.user, 'id', 'unknown')
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        try:
            logger.info(f"🔍 /fossil command called by user {user_id} with query: '{name}'")
            
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
            
            # Add Nookipedia and refresh button if available
            nookipedia_url = getattr(fossil, 'nookipedia_url', None)
            view = get_combined_view(None, nookipedia_url, add_refresh=True, content_type="fossil")
            
            logger.info(f"✅ /fossil command completed successfully for user {user_id} - found: {fossil.name}")
            message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            if view:
                view.message = message
            
        except Exception as e:
            logger.error(f"❌ Error in /fossil command for user {user_id}, query '{name}': {e}", exc_info=True)
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the fossil.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    @app_commands.command(name="critter", description="Look up a specific ACNH critter (fish, bug, or sea creature)")
    @app_commands.describe(name="The critter name to look up")
    @app_commands.autocomplete(name=critter_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def critter(self, interaction: discord.Interaction, name: str):
        """Look up critter details"""
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)

        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"🔍 /critter command used by {interaction.user.display_name} ({user_id}) in {guild_name or 'Unknown Guild'} - searching for: '{name}'")
        
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
            
            # Create the critter embed
            embed = critter.to_discord_embed()
            # embed = await safe_embed_images(embed, 'critter')
            
            # Add critter type info in footer
            critter_type = {
                'fish': 'Fish',
                'insect': 'Bug', 
                'sea': 'Sea Creature'
            }.get(critter.kind, critter.kind.title())
            
            footer_text = f"{critter_type}"
            if critter.location:
                footer_text += f" • {critter.location}"
            embed.set_footer(text=footer_text)
            
            # Create a view with availability button and add Nookipedia button
            availability_view = CritterAvailabilityView(critter, interaction.user)
            nookipedia_url = getattr(critter, 'nookipedia_url', None)
            view = get_combined_view(availability_view, nookipedia_url)
            
            logger.info(f"✅ /critter command completed successfully for user {user_id} - found: {critter.name}")
            
            # Send the message and store it in the view for timeout handling
            message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
            # Store the message in the availability view for timeout handling
            availability_view.message = message
            
        except Exception as e:
            logger.error(f"❌ Error in /critter command for user {user_id}, query '{name}': {e}", exc_info=True)
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the critter.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    # @app_commands.command(name="service-status", description="Check image service status (Cloudflare, CDNs, etc.)")
    # @app_commands.allowed_contexts(private_channels=True, guilds=True, dms=True)
    # async def service_status(self, interaction: discord.Interaction):
    #     """Check the status of image services"""
    #     ephemeral = True  # Always ephemeral for debug info
    #     await interaction.response.defer(ephemeral=ephemeral)
        
    #     try:
    #         from bot.utils.image_fallback import get_service_status_summary, get_service_monitoring_config
            
    #         status_summary = get_service_status_summary()
    #         config = get_service_monitoring_config()
            
    #         embed = discord.Embed(
    #             title="Image Service Status",
    #             color=discord.Color.green()
    #         )
            
    #         # Show monitoring status
    #         monitoring_status = "Active" if config['background_task_running'] else "Stopped"
    #         embed.add_field(
    #             name="Background Monitoring",
    #             value=f"{monitoring_status} (every {config['check_interval_minutes']} minutes)",
    #             inline=True
    #         )
            
    #         # Show monitored URLs
    #         # if config['monitor_urls']:
    #         #     urls_text = "\n".join([f"• `{url.split('/')[-1]}`" for url in config['monitor_urls'][:3]])
    #         #     embed.add_field(
    #         #         name="Sample URLs Monitored", 
    #         #         value=urls_text,
    #         #         inline=True
    #         #     )
            
    #         # Show active mocks
    #         if config.get('manual_overrides'):
    #             mock_count = len(config['manual_overrides'])
    #             mock_text = f"{mock_count} service{'s' if mock_count != 1 else ''} mocked"
    #             embed.add_field(
    #                 name="Testing Overrides",
    #                 value=mock_text,
    #                 inline=True
    #             )
            
    #         if not status_summary:
    #             embed.add_field(
    #                 name="Current Status",
    #                 value="*No checks completed yet - monitoring will begin shortly*",
    #                 inline=False
    #             )
    #             embed.color = discord.Color.orange()
    #         else:
    #             # Show status of each service
    #             status_lines = []
    #             all_good = True
                
    #             for domain, info in status_summary.items():
    #                 is_available = info.get('available', True)
    #                 reason = info.get('reason', 'No issues detected')
                    
    #                 if is_available:
    #                     status_lines.append(f"✅ **{domain}**: Healthy")
    #                 else:
    #                     status_lines.append(f"❌ **{domain}**: {reason}")
    #                     all_good = False
                
    #             embed.add_field(
    #                 name="Service Health",
    #                 value="\n".join(status_lines) if status_lines else "*No services checked*",
    #                 inline=False
    #             )
    #             embed.color = discord.Color.green() if all_good else discord.Color.red()
                
    #             if not all_good:
    #                 embed.add_field(
    #                     name="User Impact", 
    #                     value="Users will see helpful messages when image service issues are detected.",
    #                     inline=False
    #                 )
            
    #         embed.set_footer(text="Automatic monitoring helps detect image service outages before users report them")
    #         await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
    #     except Exception as e:
    #         logger.error(f"Error in service_status command: {e}", exc_info=True)
    #         embed = discord.Embed(
    #             title="❌ Error",
    #             description="An error occurred while checking service status.",
    #             color=0xe74c3c
    #         )
    #         await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    # @app_commands.command(name="cache-stats", description="Show autocomplete cache statistics (debug)")

    # @app_commands.allowed_contexts(private_channels=True, guilds=True, dms=True)
    # async def cache_stats(self, interaction: discord.Interaction):
    #     """Show cache performance statistics"""
    #     ephemeral = True  # Always ephemeral for debug info
    #     await interaction.response.defer(ephemeral=ephemeral)
        
    #     try:
    #         stats = _autocomplete_cache.get_cache_stats()
            
    #         embed = discord.Embed(
    #             title="Autocomplete Cache Statistics",
    #             color=0x3498db
    #         )
            
    #         # Basic stats
    #         embed.add_field(
    #             name="Performance",
    #             value=f"**Size:** {stats['cache_size']}/{stats['max_size']} ({stats['utilization']})\n"
    #                   f"**Total Hits:** {stats['total_hits']:,}\n"
    #                   f"**Hit Rate:** {stats['hit_rate']}",
    #             inline=True
    #         )
            
    #         # Popular queries
    #         if stats['popular_queries']:
    #             popular = "\n".join([
    #                 f"• `{key}`: {hits} hits" 
    #                 for key, hits in stats['popular_queries'][:5]
    #             ])
    #             embed.add_field(
    #                 name="Popular Queries",
    #                 value=popular,
    #                 inline=True
    #             )
            
    #         # Query patterns
    #         if stats['query_patterns']:
    #             patterns = "\n".join([
    #                 f"• **{pattern}**: {count:,} queries"
    #                 for pattern, count in list(stats['query_patterns'].items())[:5]
    #             ])
    #             embed.add_field(
    #                 name="Query Patterns",
    #                 value=patterns,
    #                 inline=False
    #             )
            
    #         embed.set_footer(text="Cache helps reduce database load and improve response times")
    #         await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
    #     except Exception as e:
    #         logger.error(f"Error in cache_stats command: {e}", exc_info=True)
    #         embed = discord.Embed(
    #             title="❌ Error",
    #             description="An error occurred while fetching cache statistics.",
    #             color=0xe74c3c
    #         )
    #         await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    # @app_commands.command(name="mock-cdn", description="Mock CDN service status for testing (admin only)")
    # @app_commands.allowed_contexts(private_channels=True, guilds=True, dms=True)
    # @app_commands.describe(
    #     action="Action to perform",
    #     domain="Domain to mock (e.g., 'dodo.ac', 'cdn.discordapp.com')",
    #     reason="Optional reason for the status change"
    # )
    # @app_commands.choices(action=[
    #     app_commands.Choice(name="Mock Service Down", value="down"),
    #     app_commands.Choice(name="Mock Service Up", value="up"),
    #     app_commands.Choice(name="Clear Mock for Domain", value="clear"),
    #     app_commands.Choice(name="Clear All Mocks", value="clear_all"),
    #     app_commands.Choice(name="Show Active Mocks", value="show")
    # ])
    # async def mock_cdn(self, interaction: discord.Interaction, action: str, domain: str = None, reason: str = None):
    #     """Mock CDN service status for testing purposes"""
    #     ephemeral = True
    #     await interaction.response.defer(ephemeral=ephemeral)
        
    #     # Basic permission check
    #     if not (interaction.user.guild_permissions.administrator if interaction.guild else True):
    #         embed = discord.Embed(
    #             title="❌ Permission Denied",
    #             description="This command requires administrator permissions.",
    #             color=discord.Color.red()
    #         )
    #         await interaction.followup.send(embed=embed, ephemeral=ephemeral)
    #         return
        
    #     try:
    #         from bot.utils.image_fallback import (
    #             mock_service_down, mock_service_up, clear_service_mock, 
    #             clear_all_service_mocks, get_active_mocks
    #         )
            
    #         if action == "show":
    #             # Show current mocks
    #             mocks = get_active_mocks()
    #             embed = discord.Embed(
    #                 title="🔧 Active CDN Service Mocks",
    #                 color=discord.Color.blue()
    #             )
                
    #             if not mocks:
    #                 embed.description = "No active service mocks. All services using real status."
    #             else:
    #                 mock_lines = []
    #                 for domain, info in mocks.items():
    #                     status = "🔴 Down" if not info['available'] else "🟢 Up"
    #                     timestamp = info['timestamp'].strftime("%H:%M:%S")
    #                     mock_lines.append(f"{status} **{domain}** - {info['reason']} *(set {timestamp})*")
                    
    #                 embed.description = "\n".join(mock_lines)
                
    #             embed.add_field(
    #                 name="💡 Testing Tips",
    #                 value="• Use `/lookup bell` to test warning messages\n"
    #                       "• Mock `dodo.ac` to test Nookipedia images\n"
    #                       "• Mock `cdn.discordapp.com` to test Discord CDN",
    #                 inline=False
    #             )
                
    #             await interaction.followup.send(embed=embed, ephemeral=ephemeral)
    #             return
            
    #         elif action == "clear_all":
    #             clear_all_service_mocks()
    #             embed = discord.Embed(
    #                 title="✅ All Mocks Cleared",
    #                 description="All CDN service mocks have been cleared. Services will now use real status.",
    #                 color=discord.Color.green()
    #             )
                
    #         elif action in ["down", "up", "clear"]:
    #             if not domain:
    #                 embed = discord.Embed(
    #                     title="❌ Domain Required",
    #                     description="Please specify a domain to mock (e.g., 'dodo.ac' or 'cdn.discordapp.com')",
    #                     color=discord.Color.red()
    #                 )
    #                 await interaction.followup.send(embed=embed, ephemeral=ephemeral)
    #                 return
                
    #             if action == "down":
    #                 mock_service_down(domain, reason or f"Test outage for {domain}")
    #                 embed = discord.Embed(
    #                     title="🔴 Service Mocked as Down",
    #                     description=f"**Domain:** {domain}\n**Reason:** {reason or f'Test outage for {domain}'}",
    #                     color=discord.Color.red()
    #                 )
    #                 embed.add_field(
    #                     name="Testing", 
    #                     value="Try `/lookup bell` or `/villager isabelle` to see warning messages!",
    #                     inline=False
    #                 )
                    
    #             elif action == "up":
    #                 mock_service_up(domain, reason or f"Test recovery for {domain}")
    #                 embed = discord.Embed(
    #                     title="🟢 Service Mocked as Up",
    #                     description=f"**Domain:** {domain}\n**Reason:** {reason or f'Test recovery for {domain}'}",
    #                     color=discord.Color.green()
    #                 )
                    
    #             elif action == "clear":
    #                 clear_service_mock(domain)
    #                 embed = discord.Embed(
    #                     title="Mock Cleared",
    #                     description=f"Cleared mock status for **{domain}**. Service will now use real status.",
    #                     color=discord.Color.blue()
    #                 )
            
    #         embed.add_field(
    #             name="Note",
    #             value="Mocks override real service checks and persist until cleared or bot restart.",
    #             inline=False
    #         )
            
    #         logger.info(f"CDN mock action '{action}' performed by {interaction.user.display_name}" + (f" on {domain}" if domain else ""))
    #         await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
    #     except Exception as e:
    #         logger.error(f"Error in mock_cdn command: {e}", exc_info=True)
    #         embed = discord.Embed(
    #             title="❌ Error",
    #             description="An error occurred while managing CDN mocks.",
    #             color=discord.Color.red()
    #         )
    #         await interaction.followup.send(embed=embed, ephemeral=ephemeral)

class VillagerDetailsView(discord.ui.View):
    """View for showing additional villager details with navigation"""
    
    def __init__(self, villager, interaction_user: discord.Member, service, current_view: str = "main"):
        super().__init__(timeout=10)  # 2 minute timeout
        self.villager = villager
        self.interaction_user = interaction_user
        self.service = service
        self.current_view = current_view
        self.message = None  # Will be set after the message is sent
        self.last_refresh_time = 0  # Track last refresh to prevent spam
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow the original user to interact"""
        return interaction.user == self.interaction_user
    
    async def resolve_clothing_name(self, clothing_id_str: str) -> str:
        """Resolve clothing ID to name"""
        try:
            # If it's already a name (contains spaces or letters), return as-is
            if not clothing_id_str.isdigit():
                return clothing_id_str
            
            # Try to convert to int and resolve name by internal IDs
            clothing_id = int(clothing_id_str)
            
            # Try internal_id/internal_group_id first (more likely for villager references)
            clothing_name = await self.service.get_item_name_by_internal_id(clothing_id)
            
            # If that didn't work, try regular table ID as fallback
            if not clothing_name:
                clothing_name = await self.service.get_item_name_by_id(clothing_id)
            
            # Debug log to see what's happening
            logger.debug(f"Resolving ID {clothing_id}: found name '{clothing_name}'")
            
            return clothing_name if clothing_name else f"Unknown Item ({clothing_id})"
        except (ValueError, TypeError) as e:
            logger.error(f"Error resolving clothing ID {clothing_id_str}: {e}")
            return clothing_id_str

    async def resolve_equipment_name(self, equipment_str: str) -> str:
        """Resolve equipment ID,variant to item name with variant (e.g., '3943,2_0' -> 'ironwood DIY workbench, Walnut')"""
        try:
            if not equipment_str:
                return "None"
                
            # Parse internal_group_id,variant format
            if ',' in equipment_str:
                internal_id_str, variant_str = equipment_str.split(',', 1)
                internal_id = int(internal_id_str)
                
                # Parse variant indices (e.g., "2_0" -> primary=2, secondary=0)
                if '_' in variant_str:
                    primary_str, secondary_str = variant_str.split('_', 1)
                    primary_index = int(primary_str)
                    secondary_index = int(secondary_str) if secondary_str else None
                else:
                    primary_index = int(variant_str)
                    secondary_index = None
            else:
                internal_id = int(equipment_str)
                primary_index = 0
                secondary_index = None
            
            # Get item name and variant display name
            result = await self.service.get_item_variant_by_internal_group_and_indices(
                internal_id, primary_index, secondary_index
            )
            
            if result:
                item_name, variant_display = result
                if variant_display and variant_display != "Default":
                    return f"{item_name}, {variant_display}"
                else:
                    return item_name
            else:
                return f"Unknown Item ({equipment_str})"
                
        except (ValueError, Exception) as e:
            logger.error(f"Error resolving equipment name for '{equipment_str}': {e}")
            return f"Error ({equipment_str})"
    
    async def get_embed_for_view(self, view_type: str) -> discord.Embed:
        """Get the appropriate embed based on view type"""
        if view_type == "house":
            embed = discord.Embed(
                title=f"🏠 {self.villager.name}'s House",
                color=discord.Color.blue()
            )
            
            # Add wallpaper as its own field
            if self.villager.wallpaper:
                embed.add_field(
                    name="Wallpaper",
                    value=self.villager.wallpaper.title(),
                    inline=True
                )
            
            # Add flooring as its own field
            if self.villager.flooring:
                embed.add_field(
                    name="Flooring", 
                    value=self.villager.flooring.title(),
                    inline=True
                )
            
            # Add music as its own field (if available)
            if hasattr(self.villager, 'favorite_song') and self.villager.favorite_song:
                embed.add_field(
                    name="Music",
                    value=self.villager.favorite_song,
                    inline=True
                )
            
            # Format furniture list nicely
            if self.villager.furniture_name_list:
                # Split furniture items and format them
                furniture_items = [item.strip().lower() for item in self.villager.furniture_name_list.split(';') if item.strip()]
                
                if furniture_items:
                    # Group similar items and format nicely
                    formatted_furniture = []
                    item_counts = {}
                    
                    # Count occurrences of each item (case-insensitive)
                    for item in furniture_items:
                        # Normalize the item name for counting
                        normalized_item = item.strip().lower()
                        item_counts[normalized_item] = item_counts.get(normalized_item, 0) + 1
                    
                    # Format with counts, sorted alphabetically
                    for item, count in sorted(item_counts.items()):
                        if count > 1:
                            formatted_furniture.append(f"• {item.title()} ×{count}")
                        else:
                            formatted_furniture.append(f"• {item.title()}")
                    
                    # Split furniture into manageable chunks (max 8 items per field)
                    chunk_size = 6
                    furniture_chunks = [formatted_furniture[i:i + chunk_size] for i in range(0, len(formatted_furniture), chunk_size)]
                    
                    embed.add_field(
                        name="Furniture",
                        value="",  # Placeholder, actual fields added below",
                        inline=False
                    )

                    # Add furniture fields (max 2 columns per row, chunk size 6)
                    for i, chunk in enumerate(furniture_chunks):
                        chunk_text = "\n".join(chunk)
                        
                        if len(furniture_chunks) == 1:
                            # Single field if small list
                            inline_field = False
                        else:
                            # Two columns for multiple chunks (max 2 columns per row)
                            inline_field = True
                        
                        embed.add_field(
                            name="",  # No field names since "Furniture" is already added above
                            value=chunk_text,
                            inline=inline_field
                        )
                        
                        # Force new row after every 2 inline fields by adding empty non-inline field
                        if inline_field and (i + 1) % 2 == 0 and (i + 1) < len(furniture_chunks):
                            embed.add_field(name="", value="", inline=False)
            
            # Set description if no house details
            if not any([self.villager.wallpaper, self.villager.flooring, self.villager.furniture_name_list]):
                embed.description = "No house details available."
            
            # Set house images if available
            if hasattr(self.villager, 'house_interior_image') and self.villager.house_interior_image:
                embed.set_image(url=self.villager.house_interior_image)
            
            if self.villager.house_image:
                embed.set_thumbnail(url=self.villager.house_image)
                
        elif view_type == "clothing":
            embed = discord.Embed(
                title=f"👕 {self.villager.name}'s Style",
                color=discord.Color.green()
            )
            
            clothing_info = []
            if self.villager.default_clothing:
                clothing_name = await self.resolve_clothing_name(self.villager.default_clothing)
                clothing_info.append(f"**Default Clothing:** {clothing_name}")
            if self.villager.default_umbrella:
                umbrella_name = await self.resolve_clothing_name(self.villager.default_umbrella)
                clothing_info.append(f"**Default Umbrella:** {umbrella_name}")
            
            if clothing_info:
                embed.description = "\n".join(clothing_info)
            else:
                embed.description = "No clothing details available."
            
            # Set villager images for clothing view
            if hasattr(self.villager, 'photo_image') and self.villager.photo_image:
                embed.set_image(url=self.villager.photo_image)
            
            if hasattr(self.villager, 'icon_image') and self.villager.icon_image:
                embed.set_thumbnail(url=self.villager.icon_image)
                
        elif view_type == "other":
            embed = discord.Embed(
                title=f"🔧 {self.villager.name}'s Other Details",
                color=discord.Color.orange()
            )

            if hasattr(self.villager, 'icon_image') and self.villager.icon_image:
                embed.set_thumbnail(url=self.villager.icon_image)
            
            other_info = []
            if self.villager.diy_workbench:
                workbench_name = await self.resolve_equipment_name(self.villager.diy_workbench)
                other_info.append(f"**DIY Workbench:** {workbench_name}")
            if self.villager.kitchen_equipment:
                kitchen_name = await self.resolve_equipment_name(self.villager.kitchen_equipment)
                other_info.append(f"**Kitchen Equipment:** {kitchen_name}")
            if self.villager.version_added:
                other_info.append(f"**Version Added:** {self.villager.version_added}")
            if self.villager.subtype:
                other_info.append(f"**Subtype:** {self.villager.subtype}")
            
            if other_info:
                embed.description = "\n".join(other_info)
            else:
                embed.description = "No additional details available."
                
        else:  # main view
            embed = self.villager.to_discord_embed()
        
        return embed
    
    @discord.ui.button(label="🏘️ About", style=discord.ButtonStyle.primary)
    async def about_villager(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show main villager info"""
        self.current_view = "main"
        embed = await self.get_embed_for_view("main")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🏠 House", style=discord.ButtonStyle.secondary)
    async def house_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show house details"""
        self.current_view = "house"
        embed = await self.get_embed_for_view("house")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="👕 Clothing", style=discord.ButtonStyle.secondary)
    async def clothing_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show clothing details"""
        self.current_view = "clothing"
        embed = await self.get_embed_for_view("clothing")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🔧 Other", style=discord.ButtonStyle.secondary)
    async def other_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show other details"""
        self.current_view = "other"
        embed = await self.get_embed_for_view("other")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🔄 Refresh Images", style=discord.ButtonStyle.secondary, row=1)
    async def refresh_images(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Refresh images in case Discord CDN fails to load them"""
        try:
            # Check cooldown (3 seconds minimum between refreshes)
            import time
            current_time = time.time()
            if current_time - self.last_refresh_time < 10:
                remaining = int(10 - (current_time - self.last_refresh_time))
                await interaction.response.send_message(f"Please wait {remaining} more second(s) before refreshing again.", ephemeral=True)
                return
            
            # Update last refresh time
            self.last_refresh_time = current_time
            
            # Get the current embed for the current view
            embed = await self.get_embed_for_view(self.current_view)
            
            # Add a subtle indicator that images were refreshed
            if embed.footer and embed.footer.text:
                footer_text = embed.footer.text
                if "🔄 Images refreshed" not in footer_text:
                    embed.set_footer(text=f"{footer_text} | 🔄 Images refreshed")
            else:
                embed.set_footer(text="🔄 Images refreshed")
            
            # Edit the message with the refreshed embed to force Discord to re-fetch images
            await interaction.response.edit_message(embed=embed, view=self)
            
            # After a short delay, restore the original footer text
            import asyncio
            await asyncio.sleep(2)
            
            # Restore original footer
            try:
                original_embed = await self.get_embed_for_view(self.current_view)
                if self.message:
                    await self.message.edit(embed=original_embed, view=self)
            except:
                pass  # Ignore errors if message was deleted or interaction expired
                
        except Exception as e:
            logger.error(f"Error refreshing villager images: {e}")
            try:
                await interaction.response.send_message("❌ Failed to refresh images", ephemeral=True)
            except:
                pass
    
    async def on_timeout(self):
        """Disable interactive buttons when view times out after 2 minutes, but keep link buttons enabled"""
        # Disable all buttons and selects except link buttons (like Nookipedia)
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                # Keep link buttons enabled (they don't need interaction handling)
                if item.style != discord.ButtonStyle.link:
                    item.disabled = True
            elif isinstance(item, discord.ui.Select):
                item.disabled = True
        
        # Try to update the message to show disabled buttons
        if self.message:
            try:
                # Generate the embed for the current view (maintain user's last selected view)
                embed = await self.get_embed_for_view(self.current_view)
                
                # Update footer to show timeout with user-friendly message
                if embed.footer and embed.footer.text:
                    embed.set_footer(text=f"{embed.footer.text} | 💤 Use the command again to interact with buttons")
                else:
                    embed.set_footer(text="💤 Buttons have expired - use the command again to interact")
                
                # Edit the message with disabled view, keeping the current view
                await self.message.edit(embed=embed, view=self)
            except Exception as e:
                # Log the error but don't crash
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to update villager message on timeout: {e}")

class CritterAvailabilityView(discord.ui.View):
    """View for showing critter availability with hemisphere and month selection"""
    
    def __init__(self, critter, interaction_user: discord.Member, show_availability: bool = False):
        super().__init__(timeout=10)  # 2 minute timeout
        self.critter = critter
        self.interaction_user = interaction_user
        self.current_hemisphere = "NH"  # Default to Northern Hemisphere
        self.current_month = "jan"  # Default to January
        self.show_availability = show_availability
        self.message = None  # Will be set after the message is sent
        self.last_refresh_time = 0  # Track last refresh to prevent spam
        

        
        # Add appropriate buttons based on mode
        if show_availability:
            self.add_availability_controls()
            self.add_back_button()
        else:
            self.add_view_availability_button()
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow the original user to interact"""
        return interaction.user == self.interaction_user
    
    def get_availability_embed(self) -> discord.Embed:
        """Create embed showing availability for selected hemisphere and month"""
        embed = discord.Embed(
            title=f"🗓️ {self.critter.name} Availability",
            color=discord.Color.green()
        )

        if self.critter.icon_url:
            embed.set_thumbnail(url=self.critter.icon_url)
        
        # Get hemisphere display name
        hemisphere_name = "Northern Hemisphere" if self.current_hemisphere == "NH" else "Southern Hemisphere"
        
        # Get month display name
        month_names = {
            "jan": "January", "feb": "February", "mar": "March", "apr": "April",
            "may": "May", "jun": "June", "jul": "July", "aug": "August",
            "sep": "September", "oct": "October", "nov": "November", "dec": "December"
        }
        month_name = month_names.get(self.current_month, self.current_month.title())
        
        embed.description = f"**Hemisphere:** {hemisphere_name}\n**Month:** {month_name}"
        
        # Get availability for current selection
        field_name = f"{self.current_hemisphere.lower()}_{self.current_month}"
        availability = getattr(self.critter, field_name, None)
        
        if availability and availability.lower() not in ['none', 'null', '']:
            # Available - show the time information
            embed.add_field(
                name="✅ Available", 
                value=f"{self.critter.name} is available in {month_name}!\n**Time:** {availability}", 
                inline=False
            )
            embed.color = discord.Color.green()
        elif availability and availability.lower() in ['none', 'null']:
            # Not available
            embed.add_field(
                name="❌ Not Available", 
                value=f"{self.critter.name} is not available in {month_name}.", 
                inline=False
            )
            embed.color = discord.Color.red()
        else:
            embed.add_field(name="❓ Unknown", value="Availability data not found.", inline=False)
            embed.color = discord.Color.orange()
        
        # Add full year overview
        year_data = []
        for month in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]:
            field = f"{self.current_hemisphere.lower()}_{month}"
            month_avail = getattr(self.critter, field, None)
            if month_avail and month_avail.lower() not in ['none', 'null', '']:
                year_data.append(f"✅ {month_names[month][:3]}")
            else:
                year_data.append(f"❌ {month_names[month][:3]}")
        
        # Split into quarters for better formatting
        quarters = [year_data[i:i+3] for i in range(0, 12, 3)]
        year_overview = "\n".join([" ".join(quarter) for quarter in quarters])
        
        embed.add_field(
            name=f"📅 Full Year Overview ({hemisphere_name})",
            value=f"```\n{year_overview}\n```",
            inline=False
        )
        
        # Add additional info if available
        info_lines = []
        if self.critter.time_of_day:
            info_lines.append(f"**Time:** {self.critter.time_of_day}")
        if self.critter.location:
            info_lines.append(f"**Location:** {self.critter.location}")
        if self.critter.weather:
            info_lines.append(f"**Weather:** {self.critter.weather}")
        
        if info_lines:
            embed.add_field(name="ℹ️ Additional Info", value="\n".join(info_lines), inline=False)
        
        return embed
    
    def add_availability_controls(self):
        """Add hemisphere and month selects for availability view"""
        hemisphere_select = discord.ui.Select(
            placeholder="Choose hemisphere...",
            options=[
                discord.SelectOption(label="Northern Hemisphere", value="NH", emoji="🌎"),
                discord.SelectOption(label="Southern Hemisphere", value="SH", emoji="🌏")
            ],
            row=0
        )
        hemisphere_select.callback = self.hemisphere_callback
        
        month_select = discord.ui.Select(
            placeholder="Choose month...",
            options=[
                discord.SelectOption(label="January", value="jan"),
                discord.SelectOption(label="February", value="feb"),
                discord.SelectOption(label="March", value="mar"),
                discord.SelectOption(label="April", value="apr"),
                discord.SelectOption(label="May", value="may"),
                discord.SelectOption(label="June", value="jun"),
                discord.SelectOption(label="July", value="jul"),
                discord.SelectOption(label="August", value="aug"),
                discord.SelectOption(label="September", value="sep"),
                discord.SelectOption(label="October", value="oct"),
                discord.SelectOption(label="November", value="nov"),
                discord.SelectOption(label="December", value="dec")
            ],
            row=1
        )
        month_select.callback = self.month_callback
        
        self.add_item(hemisphere_select)
        self.add_item(month_select)
        
        # Add refresh images button
        refresh_button = discord.ui.Button(
            label="🔄 Refresh Images", 
            style=discord.ButtonStyle.secondary, 
            row=2
        )
        refresh_button.callback = self.refresh_images_callback
        self.add_item(refresh_button)
    
    async def hemisphere_callback(self, interaction: discord.Interaction):
        """Handle hemisphere selection"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
            

        self.current_hemisphere = interaction.data['values'][0]
        embed = self.get_availability_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def month_callback(self, interaction: discord.Interaction):
        """Handle month selection"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
            

        self.current_month = interaction.data['values'][0]
        embed = self.get_availability_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def refresh_images_callback(self, interaction: discord.Interaction):
        """Refresh images in case Discord CDN fails to load them"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
        
        # Check cooldown (3 seconds minimum between refreshes)
        import time
        current_time = time.time()
        if current_time - self.last_refresh_time < 10:
            remaining = int(10 - (current_time - self.last_refresh_time))
            await interaction.response.send_message(f"Please wait {remaining} more second(s) before refreshing again.", ephemeral=True)
            return
        
        # Update last refresh time
        self.last_refresh_time = current_time
            
        try:
            # Get the current embed
            embed = self.get_availability_embed()
            
            # Add a subtle indicator that images were refreshed
            if embed.footer and embed.footer.text:
                footer_text = embed.footer.text
                if "🔄 Images refreshed" not in footer_text:
                    embed.set_footer(text=f"{footer_text} | 🔄 Images refreshed")
            else:
                embed.set_footer(text="🔄 Images refreshed")
            
            # Edit the message with the refreshed embed to force Discord to re-fetch images
            await interaction.response.edit_message(embed=embed, view=self)
            
            # After a short delay, restore the original footer text
            import asyncio
            await asyncio.sleep(2)
            
            # Restore original footer
            try:
                original_embed = self.get_availability_embed()
                if self.message:
                    await self.message.edit(embed=original_embed, view=self)
            except:
                pass  # Ignore errors if message was deleted or interaction expired
                
        except Exception as e:
            logger.error(f"Error refreshing critter images: {e}")
            try:
                await interaction.response.send_message("❌ Failed to refresh images", ephemeral=True)
            except:
                pass
    
    async def refresh_main_images_callback(self, interaction: discord.Interaction):
        """Refresh images for main critter view in case Discord CDN fails to load them"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
        
        # Check cooldown (3 seconds minimum between refreshes)
        import time
        current_time = time.time()
        if current_time - self.last_refresh_time < 3:
            remaining = int(3 - (current_time - self.last_refresh_time))
            await interaction.response.send_message(f"Please wait {remaining} more second(s) before refreshing again.", ephemeral=True)
            return
        
        # Update last refresh time
        self.last_refresh_time = current_time
            
        try:
            # Get the main critter embed
            embed = self.critter.to_discord_embed()
            
            # Add critter type info in footer
            critter_type = {
                'fish': 'Fish',
                'insect': 'Bug', 
                'sea': 'Sea Creature'
            }.get(self.critter.kind, self.critter.kind.title())
            
            footer_text = f"{critter_type}"
            if self.critter.location:
                footer_text += f" • {self.critter.location}"
            
            # Add refresh indicator
            footer_text += " | 🔄 Images refreshed"
            embed.set_footer(text=footer_text)
            
            # Edit the message with the refreshed embed to force Discord to re-fetch images
            await interaction.response.edit_message(embed=embed, view=self)
            
            # After a short delay, restore the original footer text
            import asyncio
            await asyncio.sleep(2)
            
            # Restore original footer
            try:
                original_embed = self.critter.to_discord_embed()
                original_footer = f"{critter_type}"
                if self.critter.location:
                    original_footer += f" • {self.critter.location}"
                original_embed.set_footer(text=original_footer)
                
                if self.message:
                    await self.message.edit(embed=original_embed, view=self)
            except:
                pass  # Ignore errors if message was deleted or interaction expired
                
        except Exception as e:
            logger.error(f"Error refreshing main critter images: {e}")
            try:
                await interaction.response.send_message("❌ Failed to refresh images", ephemeral=True)
            except:
                pass
    
    def add_back_button(self):
        """Add only the back to details button"""
        back_button = discord.ui.Button(label="📋 Back to Details", style=discord.ButtonStyle.secondary, row=2)
        back_button.callback = self.back_callback
        self.add_item(back_button)
        

    
    def add_view_availability_button(self):
        """Add only the view availability button"""
        availability_button = discord.ui.Button(label="🗓️ View Availability", style=discord.ButtonStyle.primary)
        availability_button.callback = self.availability_callback
        self.add_item(availability_button)
        
        # Add refresh images button for main critter view
        refresh_button = discord.ui.Button(
            label="🔄 Refresh Images", 
            style=discord.ButtonStyle.secondary
        )
        refresh_button.callback = self.refresh_main_images_callback
        self.add_item(refresh_button)
    
    async def back_callback(self, interaction: discord.Interaction):
        """Go back to the main critter details"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
            
        # Stop the current view's timeout since we're replacing it
        # logger.info(f"Stopping CritterAvailabilityView: id={id(self)}, show_availability={self.show_availability}")
        self.stop()
        
        embed = self.critter.to_discord_embed()
        
        # Add critter type info in footer
        critter_type = {
            'fish': 'Fish',
            'insect': 'Bug', 
            'sea': 'Sea Creature'
        }.get(self.critter.kind, self.critter.kind.title())
        
        footer_text = f"{critter_type}"
        if self.critter.location:
            footer_text += f" • {self.critter.location}"
        embed.set_footer(text=footer_text)
        
        # Create a new view with only the availability button (no selects)
        view = CritterAvailabilityView(self.critter, self.interaction_user, show_availability=False)
        view.clear_items()
        view.add_view_availability_button()
        
        # Transfer the message reference to the new view for timeout handling
        view.message = self.message

        
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def availability_callback(self, interaction: discord.Interaction):
        """Show availability interface"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
            
        # Stop the current view's timeout since we're replacing it
        logger.info(f"Stopping CritterAvailabilityView: id={id(self)}, show_availability={self.show_availability}")
        self.stop()
        
        # Create new view with availability controls
        view = CritterAvailabilityView(self.critter, self.interaction_user, show_availability=True)
        
        # Transfer the message reference to the new view for timeout handling
        view.message = self.message

        
        embed = view.get_availability_embed()
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def on_timeout(self):
        """Disable interactive buttons when view times out after 2 minutes, but keep link buttons enabled"""
        # Disable all buttons and selects except link buttons
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                # Keep link buttons enabled (they don't need interaction handling)
                if item.style != discord.ButtonStyle.link:
                    item.disabled = True
            elif isinstance(item, discord.ui.Select):
                item.disabled = True
        
        # Try to update the message to show disabled buttons
        if self.message:
            try:
                # Generate the appropriate embed based on current view state
                if self.show_availability:
                    embed = self.get_availability_embed()
                else:
                    # Main critter details view
                    embed = self.critter.to_discord_embed()
                    
                    # Add critter type info in footer
                    critter_type = {
                        'fish': 'Fish',
                        'insect': 'Bug', 
                        'sea': 'Sea Creature'
                    }.get(self.critter.kind, self.critter.kind.title())
                    
                    footer_text = f"{critter_type}"
                    if self.critter.location:
                        footer_text += f" • {self.critter.location}"
                    embed.set_footer(text=footer_text)
                
                # Update footer to show timeout with user-friendly message
                if embed.footer and embed.footer.text:
                    embed.set_footer(text=f"{embed.footer.text} | 💤 Use the command again to interact with buttons")
                else:
                    embed.set_footer(text="💤 Buttons have expired - use the command again to interact")
                
                # Edit the message with disabled view, keeping the current view state
                await self.message.edit(embed=embed, view=self)
            except Exception as e:
                # Log the error but don't crash
                logger.error(f"Failed to update critter message on timeout: {e}", exc_info=True)
        # If no message reference, timeout silently

async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(ACNHCommands(bot))