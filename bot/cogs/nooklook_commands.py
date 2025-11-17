"""Modern ACNH Discord commands using the new nooklook database"""

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
import asyncio
from functools import lru_cache
import time

logger = logging.getLogger(__name__)

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
        
        # Convert to choices
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

# class BrowseGroup(app_commands.Group):
    """Command group for browsing different types of ACNH content"""
    
    def __init__(self, service: NooklookService):
        super().__init__(name="browse", description="Browse ACNH content with filters")
        self.service = service
        
        # Cache filter options for autocomplete
        self.filter_options = {}
        self._filters_loaded = False
    
    async def _ensure_filters_loaded(self):
        """Ensure filter options are loaded for autocomplete"""
        if not self._filters_loaded:
            try:
                self.filter_options = await self.service.get_filter_options()
                self._filters_loaded = True
            except Exception as e:
                logger.error(f"Failed to load filter options: {e}")
                self.filter_options = {}
    
    # Autocomplete functions for filters
    async def category_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        """Autocomplete for item categories"""
        await self._ensure_filters_loaded()
        categories = self.filter_options.get('item_categories', [])
        
        # Filter based on current input
        filtered = [cat for cat in categories if current.lower() in cat.lower()][:25]
        return [app_commands.Choice(name=cat, value=cat) for cat in filtered]
    
    @app_commands.command(name="items", description="Browse furniture and items with filters")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
    @app_commands.describe(
        category="Filter by item category (e.g., Housewares, Miscellaneous)",
        color="Filter by primary color",
        price_range="Filter by price range"
    )
    @app_commands.autocomplete(category=category_autocomplete)
    @app_commands.choices(color=[
        app_commands.Choice(name="Red", value="red"),
        app_commands.Choice(name="Orange", value="orange"),
        app_commands.Choice(name="Yellow", value="yellow"),
        app_commands.Choice(name="Green", value="green"),
        app_commands.Choice(name="Blue", value="blue"),
        app_commands.Choice(name="Purple", value="purple"),
        app_commands.Choice(name="Pink", value="pink"),
        app_commands.Choice(name="Brown", value="brown"),
        app_commands.Choice(name="Black", value="black"),
        app_commands.Choice(name="White", value="white"),
        app_commands.Choice(name="Gray", value="gray")
    ])
    @app_commands.choices(price_range=[
        app_commands.Choice(name="Free (0 bells)", value="free"),
        app_commands.Choice(name="Cheap (1-1000 bells)", value="cheap"),
        app_commands.Choice(name="Moderate (1001-5000 bells)", value="moderate"),
        app_commands.Choice(name="Expensive (5001-20000 bells)", value="expensive"),
        app_commands.Choice(name="Very Expensive (20000+ bells)", value="very_expensive")
    ])
    async def browse_items(self, interaction: discord.Interaction, 
                          category: Optional[str] = None,
                          color: Optional[str] = None,
                          price_range: Optional[str] = None):
        """Browse items with optional filters"""
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        try:
            data = await self.service.browse_items(category, color, price_range)
            
            if not data['items']:
                embed = discord.Embed(
                    title="🔍 No Items Found",
                    description="No items match your filter criteria.",
                    color=0xe74c3c
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            view = ItemsPaginationView(
                bot=interaction.client,
                interaction_user=interaction.user,
                data=data,
                service=self.service,
                category=category,
                color=color,
                price_range=price_range
            )
            
            embed = view.create_embed()
            await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in browse_items: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while browsing items.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

class ACNHCommands(commands.Cog):
    """ACNH lookup commands using nooklook database"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.service = NooklookService()
        
        # Store service in bot for easy access from autocomplete functions
        bot.nooklook_service = self.service
        
        # Add the browse command group
        # self.browse = BrowseGroup(self.service)
        # self.bot.tree.add_command(self.browse)
    
    async def cog_load(self):
        """Initialize the database when cog loads"""
        try:
            await self.service.init_database()
            logger.info("✅ ACNH database initialized successfully")
            logger.info(f"📊 Autocomplete cache initialized (max_size: {_autocomplete_cache.max_size}, regular_ttl: {_autocomplete_cache.ttl}s, random_ttl: {_autocomplete_cache.random_ttl}s)")
        except Exception as e:
            logger.error(f"❌ Failed to initialize ACNH database: {e}", exc_info=True)
    
    async def cog_unload(self):
        """Cleanup when cog unloads"""
        # Log detailed cache statistics before clearing
        stats = _autocomplete_cache.get_cache_stats()
        logger.info(f"📊 Final Cache Stats - Size: {stats['cache_size']}, Hits: {stats['total_hits']}, Rate: {stats['hit_rate']}")
        if stats['popular_queries']:
            top_query = stats['popular_queries'][0]
            logger.info(f"🔥 Most popular query: '{top_query[0]}' ({top_query[1]} hits)")
        
        _autocomplete_cache.clear()
        
        # Remove service reference from bot
        if hasattr(self.bot, 'nooklook_service'):
            delattr(self.bot, 'nooklook_service')
            logger.info("🗑️ NooklookService reference removed from bot")
    
    @app_commands.command(name="search", description="Search across all ACNH content")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
    @app_commands.describe(
        query="What to search for (exact phrase matching)",
        category="Limit search to specific content type"
    )
    @app_commands.choices(category=[
        app_commands.Choice(name="Items", value="items"),
        app_commands.Choice(name="Critters", value="critters"),
        app_commands.Choice(name="Food Recipes", value="food_recipes"),
        app_commands.Choice(name="DIY Recipes", value="diy_recipes"),
        app_commands.Choice(name="Villagers", value="villagers")
    ])
    async def search(self, interaction: discord.Interaction, 
                    query: str, category: Optional[str] = None):
        """Search across all ACNH content using FTS5"""
        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        category_str = f" in {category}" if category else ""
        logger.info(f"🔍 /search command used by {interaction.user.display_name} ({user_id}) in {guild_name} - query: '{query}'{category_str}")
        
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        try:
            # Map Discord choice values to database category values
            category_mapping = {
                "items": "item",           # Discord "items" -> DB "item"
                "critters": "critter",     # Discord "critters" -> DB "critter"  
                "food_recipes": "recipe",  # Discord "food_recipes" -> DB "recipe"
                "diy_recipes": "recipe",   # Discord "diy_recipes" -> DB "recipe"
                "villagers": "villager"    # Discord "villagers" -> DB "villager"
            }
            
            # Convert category to database format
            db_category = category_mapping.get(category) if category else None
            
            # For recipe subcategories, we need special handling
            recipe_subtype = None
            if category == "food_recipes":
                recipe_subtype = "food"
            elif category == "diy_recipes":
                recipe_subtype = "diy"
            
            logger.debug(f"Search: executing search_all with query='{query}', category_filter='{db_category}', recipe_subtype='{recipe_subtype}' (Discord: '{category}')")
            
            results = await self.service.search_all(query, category_filter=db_category, recipe_subtype=recipe_subtype)
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
                    view = VariantSelectView(result, interaction.user)
                    embed = view.create_embed()
                    await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
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
                    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
            # Multiple results - show navigation view
            else:
                view = SearchResultsView(results, query, interaction.user)
                embed = view.create_embed()
                category_info = f" in {category}" if category else ""
                logger.info(f"✅ /search command completed for user {user_id} - found {len(results)} results for '{query}'{category_info}")
                await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in search: {e}")
            embed = discord.Embed(
                title="❌ Search Error",
                description="An error occurred while searching.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)
    
    # @app_commands.command(name="database-stats", description="Show database statistics")
    # async def database_stats(self, interaction: discord.Interaction):
    #     """Show comprehensive database statistics"""
    #     ephemeral = not is_dm(interaction)
    #     await interaction.response.defer(ephemeral=ephemeral)
        
    #     try:
    #         stats = await self.service.get_database_stats()
            
    #         embed = discord.Embed(
    #             title="📊 Database Statistics",
    #             color=0x3498db
    #         )
            
    #         if stats.get('database_active'):
    #             # Add individual counts
    #             stats_text = []
    #             if 'items' in stats:
    #                 stats_text.append(f"🏠 Items: {stats['items']:,}")
    #             if 'critters' in stats:
    #                 stats_text.append(f"🐛 Critters: {stats['critters']:,}")
    #             if 'recipes' in stats:
    #                 stats_text.append(f"🛠️ Recipes: {stats['recipes']:,}")
    #             if 'villagers' in stats:
    #                 stats_text.append(f"👥 Villagers: {stats['villagers']:,}")
                
    #             embed.add_field(
    #                 name="📈 Content Counts",
    #                 value="\n".join(stats_text),
    #                 inline=False
    #             )
                
    #             embed.add_field(
    #                 name="📦 Total Content",
    #                 value=f"{stats.get('total_content', 0):,} items",
    #                 inline=True
    #             )
                
    #             embed.color = 0x2ecc71
    #         else:
    #             embed.description = "Database is not available or empty."
    #             if 'error' in stats:
    #                 embed.add_field(name="Error", value=stats['error'], inline=False)
    #             embed.color = 0xe74c3c
            
    #         await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
    #     except Exception as e:
    #         logger.error(f"Error in database_stats: {e}")
    #         embed = discord.Embed(
    #             title="❌ Error",
    #             description="An error occurred while fetching database statistics.",
    #             color=0xe74c3c
    #         )
    #         await interaction.followup.send(embed=embed, ephemeral=ephemeral)

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
        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"🔍 /lookup command used by {interaction.user.display_name} ({user_id}) in {guild_name} - searching for: '{item}'")
        
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
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
                    view = VariantSelectView(result, interaction.user)
                    await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
                else:
                    # Single item - show directly
                    embed = result.to_discord_embed()
                    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Multiple results - show search-style list with pagination
            embed = discord.Embed(
                title=f"🔍 Lookup Results for '{item}'",
                color=0x3498db
            )
            
            # Create paginated view for multiple results
            paginated_view = PaginatedResultView(results, embed_title=f"🔍 Lookup Results for '{item}'")
            embed = paginated_view.create_page_embed()
            
            await interaction.followup.send(embed=embed, view=paginated_view, ephemeral=ephemeral)
            
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
        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"👥 /villager command used by {interaction.user.display_name} ({user_id}) in {guild_name} - searching for: '{name}'")
        
        await interaction.response.defer(thinking=True)
        
        # Check if this is a DM for ephemeral logic
        ephemeral = not is_dm(interaction)
        
        try:
            # Convert name to villager ID if it's numeric (from autocomplete)
            if name.isdigit():
                villager_id = int(name)
                villager = await self.service.get_villager_by_id(villager_id)
            else:
                # Search for villager by name
                search_results = await self.service.search(name, limit=50)
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
            
            # Create a view with buttons for additional details
            view = VillagerDetailsView(villager, interaction.user, self.service)
            
            await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
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
        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"🍳 /recipe command used by {interaction.user.display_name} ({user_id}) in {guild_name} - searching for: '{name}'")
        
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
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
            
            # Add recipe type info in footer
            recipe_type = "🍳 Food Recipe" if recipe.is_food() else "🛠️ DIY Recipe"
            embed.set_footer(text=f"{recipe_type} • {recipe.category or 'Unknown Category'}")
            
            logger.info(f"✅ /recipe command completed successfully for user {user_id} - found: {recipe.name} ({recipe_type})")
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
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
        ephemeral = not is_dm(interaction)
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
            
            # Add artwork category info in footer
            authenticity = "Genuine" if artwork.genuine else "Fake"
            category_text = f"🎨 {authenticity} Artwork"
            if artwork.art_category:
                category_text += f" • {artwork.art_category}"
            embed.set_footer(text=category_text)
            
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in artwork command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the artwork.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    @app_commands.command(name="critter", description="Look up a specific ACNH critter (fish, bug, or sea creature)")
    @app_commands.describe(name="The critter name to look up")
    @app_commands.autocomplete(name=critter_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def critter(self, interaction: discord.Interaction, name: str):
        """Look up critter details"""
        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"🔍 /critter command used by {interaction.user.display_name} ({user_id}) in {guild_name} - searching for: '{name}'")
        
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
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
                    value="• 🐟 Fish: Found in rivers, ponds, and the sea\n"
                          "• 🦋 Bugs: Found around flowers, trees, and rocks\n"
                          "• 🌊 Sea Creatures: Found while diving in the ocean\n"
                          "• Try `/search` with partial names or locations",
                    inline=False
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Create the critter embed
            embed = critter.to_discord_embed()
            
            # Add critter type info in footer
            critter_type = {
                'fish': '🐟 Fish',
                'insect': '🦋 Bug', 
                'sea': '🌊 Sea Creature'
            }.get(critter.kind, critter.kind.title())
            
            footer_text = f"{critter_type}"
            if critter.location:
                footer_text += f" • {critter.location}"
            embed.set_footer(text=footer_text)
            
            # Create a view with availability button
            view = CritterAvailabilityView(critter, interaction.user)
            
            logger.info(f"✅ /critter command completed successfully for user {user_id} - found: {critter.name}")
            await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"❌ Error in /critter command for user {user_id}, query '{name}': {e}", exc_info=True)
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the critter.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    @app_commands.command(name="cache-stats", description="Show autocomplete cache statistics (debug)")
    @app_commands.allowed_contexts(private_channels=True, guilds=True, dms=True)
    async def cache_stats(self, interaction: discord.Interaction):
        """Show cache performance statistics"""
        ephemeral = True  # Always ephemeral for debug info
        await interaction.response.defer(ephemeral=ephemeral)
        
        try:
            stats = _autocomplete_cache.get_cache_stats()
            
            embed = discord.Embed(
                title="📊 Autocomplete Cache Statistics",
                color=0x3498db
            )
            
            # Basic stats
            embed.add_field(
                name="📈 Performance",
                value=f"**Size:** {stats['cache_size']}/{stats['max_size']} ({stats['utilization']})\n"
                      f"**Total Hits:** {stats['total_hits']:,}\n"
                      f"**Hit Rate:** {stats['hit_rate']}",
                inline=True
            )
            
            # Popular queries
            if stats['popular_queries']:
                popular = "\n".join([
                    f"• `{key}`: {hits} hits" 
                    for key, hits in stats['popular_queries'][:5]
                ])
                embed.add_field(
                    name="🔥 Popular Queries",
                    value=popular,
                    inline=True
                )
            
            # Query patterns
            if stats['query_patterns']:
                patterns = "\n".join([
                    f"• **{pattern}**: {count:,} queries"
                    for pattern, count in list(stats['query_patterns'].items())[:5]
                ])
                embed.add_field(
                    name="📋 Query Patterns",
                    value=patterns,
                    inline=False
                )
            
            embed.set_footer(text="Cache helps reduce database load and improve response times")
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in cache_stats command: {e}", exc_info=True)
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while fetching cache statistics.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

class VillagerDetailsView(discord.ui.View):
    """View for showing additional villager details with navigation"""
    
    def __init__(self, villager, interaction_user: discord.Member, service, current_view: str = "main"):
        super().__init__(timeout=300)
        self.villager = villager
        self.interaction_user = interaction_user
        self.service = service
        self.current_view = current_view
    
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
    
    def get_embed_for_view(self, view_type: str) -> discord.Embed:
        """Get the appropriate embed based on view type"""
        if view_type == "house":
            embed = discord.Embed(
                title=f"🏠 {self.villager.name}'s House",
                color=discord.Color.blue()
            )
            
            house_info = []
            if self.villager.wallpaper:
                house_info.append(f"**Wallpaper:** {self.villager.wallpaper}")
            if self.villager.flooring:
                house_info.append(f"**Flooring:** {self.villager.flooring}")
            if self.villager.furniture_name_list:
                house_info.append(f"**Furniture:** {self.villager.furniture_name_list}")
            
            if house_info:
                embed.description = "\n".join(house_info)
            else:
                embed.description = "No house details available."
            
            # Set house image if available
            if self.villager.house_image:
                embed.set_image(url=self.villager.house_image)
                
        elif view_type == "clothing":
            embed = discord.Embed(
                title=f"👕 {self.villager.name}'s Style",
                color=discord.Color.green()
            )
            
            clothing_info = []
            if self.villager.default_clothing:
                clothing_info.append(f"**Default Clothing:** {self.villager.default_clothing}")
            if self.villager.default_umbrella:
                clothing_info.append(f"**Default Umbrella:** {self.villager.default_umbrella}")
            
            if clothing_info:
                embed.description = "\n".join(clothing_info)
            else:
                embed.description = "No clothing details available."
                
        elif view_type == "other":
            embed = discord.Embed(
                title=f"🔧 {self.villager.name}'s Other Details",
                color=discord.Color.orange()
            )
            
            other_info = []
            if self.villager.diy_workbench:
                other_info.append(f"**DIY Workbench:** {self.villager.diy_workbench}")
            if self.villager.kitchen_equipment:
                other_info.append(f"**Kitchen Equipment:** {self.villager.kitchen_equipment}")
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
        embed = self.get_embed_for_view("main")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🏠 House", style=discord.ButtonStyle.secondary)
    async def house_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show house details"""
        self.current_view = "house"
        embed = self.get_embed_for_view("house")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="👕 Clothing", style=discord.ButtonStyle.secondary)
    async def clothing_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show clothing details"""
        self.current_view = "clothing"
        
        # Create clothing embed with resolved names
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
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🔧 Other", style=discord.ButtonStyle.secondary)
    async def other_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show other details"""
        self.current_view = "other"
        embed = self.get_embed_for_view("other")
        await interaction.response.edit_message(embed=embed, view=self)

class CritterAvailabilityView(discord.ui.View):
    """View for showing critter availability with hemisphere and month selection"""
    
    def __init__(self, critter, interaction_user: discord.Member, show_availability: bool = False):
        super().__init__(timeout=300)
        self.critter = critter
        self.interaction_user = interaction_user
        self.current_hemisphere = "NH"  # Default to Northern Hemisphere
        self.current_month = "jan"  # Default to January
        self.show_availability = show_availability
        
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
    
    async def back_callback(self, interaction: discord.Interaction):
        """Go back to the main critter details"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
            
        embed = self.critter.to_discord_embed()
        
        # Add critter type info in footer
        critter_type = {
            'fish': '🐟 Fish',
            'insect': '🦋 Bug', 
            'sea': '🌊 Sea Creature'
        }.get(self.critter.kind, self.critter.kind.title())
        
        footer_text = f"{critter_type}"
        if self.critter.location:
            footer_text += f" • {self.critter.location}"
        embed.set_footer(text=footer_text)
        
        # Create a new view with only the availability button (no selects)
        view = CritterAvailabilityView(self.critter, self.interaction_user, show_availability=False)
        view.clear_items()
        view.add_view_availability_button()
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def availability_callback(self, interaction: discord.Interaction):
        """Show availability interface"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
            
        # Create new view with availability controls
        view = CritterAvailabilityView(self.critter, self.interaction_user, show_availability=True)
        
        embed = view.get_availability_embed()
        await interaction.response.edit_message(embed=embed, view=view)

async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(ACNHCommands(bot))