"""Autocomplete handlers for ACNH commands"""
from discord import app_commands, Interaction
from typing import List
import logging

# import discord

from bot.utils.autocomplete_cache import autocomplete_cache

logger = logging.getLogger(__name__)

async def villager_name_autocomplete(interaction: Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for villager names with caching"""
    user_id = getattr(interaction.user, 'id', 'unknown')
    logger.debug(f"Villager autocomplete called by user {user_id} with query: '{current}'")
    
    try:
        # Normalize query for consistent caching
        query = current.lower().strip()
        cache_key = f"villager:{query}"
        
        # Check cache first
        cached_result = autocomplete_cache.get(cache_key)
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
        autocomplete_cache.set(cache_key, choices)
        return choices
        
    except Exception as e:
        logger.error(f"Error in villager autocomplete for user {user_id}, query '{current}': {e}", exc_info=True)
        return []

async def recipe_name_autocomplete(interaction: Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for recipe names with caching"""
    user_id = getattr(interaction.user, 'id', 'unknown')
    logger.debug(f"Recipe autocomplete called by user {user_id} with query: '{current}'")
    
    try:
        # Normalize query for consistent caching
        query = current.lower().strip()
        cache_key = f"recipe:{query}"
        
        # Check cache first
        cached_result = autocomplete_cache.get(cache_key)
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
            cached_result = autocomplete_cache.get(cache_key)
            if cached_result:
                logger.debug(f"Recipe autocomplete: returning {len(cached_result)} cached random results")
                return cached_result
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
        autocomplete_cache.set(cache_key, choices)
        return choices

    except Exception as e:
        logger.error(f"Error in recipe autocomplete for user {user_id}, query '{current}': {e}", exc_info=True)
        return []

async def artwork_name_autocomplete(interaction: Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for artwork names with caching"""
    user_id = getattr(interaction.user, 'id', 'unknown')
    logger.debug(f"Artwork autocomplete called by user {user_id} with query: '{current}'")
    
    try:
        # Normalize query for consistent caching
        query = current.lower().strip()
        cache_key = f"artwork:{query}"
        
        # Check cache first
        cached_result = autocomplete_cache.get(cache_key)
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
            cached_result = autocomplete_cache.get(cache_key)
            if cached_result:
                logger.debug(f"Artwork autocomplete: returning {len(cached_result)} cached random results")
                return cached_result
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
        autocomplete_cache.set(cache_key, choices)
        return choices

    except Exception as e:
        logger.error(f"Error in artwork autocomplete for user {user_id}, query '{current}': {e}", exc_info=True)
        return []

async def critter_name_autocomplete(interaction: Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for critter names with caching"""
    user_id = getattr(interaction.user, 'id', 'unknown')
    logger.debug(f"Critter autocomplete called by user {user_id} with query: '{current}'")
    
    try:
        # Normalize query for consistent caching
        query = current.lower().strip()
        cache_key = f"critter:{query}"
        
        # Check cache first
        cached_result = autocomplete_cache.get(cache_key)
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
            cached_result = autocomplete_cache.get(cache_key)
            if cached_result:
                logger.debug(f"Critter autocomplete: returning {len(cached_result)} cached random results")
                return cached_result
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
        autocomplete_cache.set(cache_key, choices)
        return choices
        
    except Exception as e:
        logger.error(f"Error in critter autocomplete for user {user_id}, query '{current}': {e}", exc_info=True)
        return []

async def fossil_name_autocomplete(interaction: Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for fossil names with caching"""
    user_id = getattr(interaction.user, 'id', 'unknown')
    logger.debug(f"Fossil autocomplete called by user {user_id} with query: '{current}'")
    
    try:
        # Use cache with fossil-specific key
        cache_key = f"fossil_autocomplete:{current.lower()}"
        cached_results = autocomplete_cache.get(cache_key)
        
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
        autocomplete_cache.set(cache_key, choices)
        
        logger.debug(f"Fossil autocomplete for user {user_id}, query '{current}' - found {len(choices)} results")
        return choices
        
    except Exception as e:
        logger.error(f"Error in fossil autocomplete for user {user_id}, query '{current}': {e}", exc_info=True)
        return []

async def item_name_autocomplete(interaction: Interaction, current: str) -> list[app_commands.Choice[str]]:
    """Autocomplete for item names (base items only, no variants)"""
    user_id = getattr(interaction.user, 'id', 'unknown')
    logger.debug(f"Item autocomplete called by user {user_id} with query: '{current}'")

    try:
        # Get service from bot instance
        service = getattr(interaction.client, 'nooklook_service', None)
        if not service:
            logger.error("Item autocomplete: NooklookService not found on bot instance")
            return []
        
        if not current or len(current) <= 2:
            logger.debug(f"Item autocomplete: generating random items for user {user_id} (no cache for items)")
            # Show 25 random items when query is too short - no caching for true randomness
            base_items = await service.get_random_item_suggestions(25)
        else:
            logger.debug(f"Item autocomplete: searching database for '{current}' (user {user_id})")
            # Get base item names and IDs using the service
            base_items = await service.get_base_item_suggestions(current)
        
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
