from typing import Optional, Dict, Any, List
from bot.repos.acnh_items_repo import NooklookRepository
from bot.models.acnh_item import Item, ItemVariant, Critter, Recipe, Villager, Artwork, Fossil
import logging
from bot.repos.acnh_items_repo import CLOTHING_CATEGORIES
from bot.services.translation_service import TranslationService
from bot.repos.user_repo import UserRepository

logger = logging.getLogger("bot.acnh_service")

class NooklookService:
    """Service for handling nooklook database operations"""
    
    def __init__(self):
        self.repo = NooklookRepository()
        self.translation_service = TranslationService()
        self.user_repo = UserRepository()
    
    async def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language code"""
        return await self.user_repo.get_user_language(user_id)
    
    async def init_database(self) -> bool:
        """Initialize and validate the database.
        
        Returns:
            bool: True if database is valid and ready
            
        Raises:
            FileNotFoundError: If database file doesn't exist
            RuntimeError: If required tables are missing
        """
        return await self.repo.init_database()
    
    async def close_connections(self):
        """Close persistent database connections"""
        await self.repo.db.close()
        logger.info("Database connections closed")
    
    async def search_all(self, query: str, category_filter: str = None, recipe_subtype: str = None, item_subcategory: str = None, user_id: int = None) -> List[Any]:
        """Search across all content types using FTS5 with prefix matching.
        
        If user_id is provided and user has non-English language, also searches translations.
        """
        try:
            # Get user's language for translation search
            search_language = 'en'
            if user_id:
                search_language = await self.get_user_language(user_id)
            
            # Always do English FTS search first
            search_results = await self.repo.search_fts_autocomplete(query, category_filter, limit=50)
            
            # If user has non-English language and we're searching items, also search translations
            translation_item_ids = set()
            if search_language != 'en' and (category_filter is None or category_filter == 'item'):
                translated_matches = await self.translation_service.search_by_translation(
                    query, language=search_language, ref_table='items', limit=25
                )
                translation_item_ids = {match['ref_id'] for match in translated_matches}
                
                # Add translation matches that aren't already in results
                existing_item_ids = {r['ref_id'] for r in search_results if r['ref_table'] == 'items'}
                for match in translated_matches:
                    if match['ref_id'] not in existing_item_ids:
                        search_results.append({
                            'ref_table': 'items',
                            'ref_id': match['ref_id'],
                            'name': match['en_name']
                        })
            
            # Batch resolve all search results (optimized - reduces N+1 queries to ~6)
            resolved_map = await self.repo.resolve_search_results_batch(search_results)
            
            # Track seen clothing items to deduplicate variants
            seen_clothing_items = {}  # key: (name, category), value: item
            
            # Process results in original search order
            resolved_items = []
            for result in search_results:
                key = f"{result['ref_table']}:{result['ref_id']}"
                obj = resolved_map.get(key)
                if obj:
                    # Filter recipes by subtype if specified
                    if recipe_subtype and hasattr(obj, 'is_food'):
                        if recipe_subtype == "food" and not obj.is_food():
                            continue  # Skip non-food recipes when looking for food
                        elif recipe_subtype == "diy" and obj.is_food():
                            continue  # Skip food recipes when looking for DIY
                    
                    # Filter items by subcategory if specified
                    if item_subcategory and hasattr(obj, 'category'):
                        if obj.category != item_subcategory:
                            continue  # Skip items that don't match the subcategory
                    
                    # Deduplicate clothing items by name (since each variant is a separate item)
                    if hasattr(obj, 'category') and obj.category in CLOTHING_CATEGORIES:
                        item_key = (obj.name, obj.category)
                        if item_key in seen_clothing_items:
                            continue  # Skip duplicate clothing items with same name
                        seen_clothing_items[item_key] = obj
                    
                    resolved_items.append(obj)
            
            return resolved_items
            
        except Exception as e:
            logger.error(f"Error in search: {e}")
            return []
    
    async def get_item_by_id(self, item_id: int) -> Optional[Item]:
        """Get a specific item by ID with variants"""
        return await self.repo.get_item_by_id(item_id, load_variants=True)
    
    # ==================== Translation Methods ====================
    
    async def search_items_localized(self, query: str, user_id: int, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Search items using the user's preferred language.
        Returns items with both English and localized names.
        """
        language = await self.get_user_language(user_id)
        
        # If user's language is English, just do normal search
        if language == 'en':
            results = await self.repo.get_base_item_suggestions(query)
            return [{'id': item_id, 'name': name, 'localized_name': name} for name, item_id in results[:limit]]
        
        # Search in user's language first
        translated_matches = await self.translation_service.search_by_translation(
            query, language=language, ref_table='items', limit=limit
        )
        
        if translated_matches:
            return [
                {
                    'id': match['ref_id'],
                    'name': match['en_name'],
                    'localized_name': match['matched_name']
                }
                for match in translated_matches
            ]
        
        # Fallback to English search if no translated matches
        results = await self.repo.get_base_item_suggestions(query)
        return [{'id': item_id, 'name': name, 'localized_name': name} for name, item_id in results[:limit]]
    
    async def get_localized_item_name(self, item_id: int, user_id: int, fallback_name: str) -> str:
        """Get item name in user's preferred language"""
        language = await self.get_user_language(user_id)
        return await self.translation_service.get_localized_name_or_fallback(
            'items', item_id, language, fallback_name
        )
    
    async def get_item_suggestions_localized(self, query: str, user_id: int, limit: int = 25) -> List[tuple[str, int]]:
        """
        Get item suggestions for autocomplete in user's language.
        Returns (display_name, item_id) tuples where display_name shows localized name.
        """
        language = await self.get_user_language(user_id)
        
        # If English, use normal suggestions
        if language == 'en':
            return await self.get_base_item_suggestions(query)
        
        # Search in translated names
        translated_matches = await self.translation_service.search_by_translation(
            query, language=language, ref_table='items', limit=limit
        )
        
        if translated_matches:
            # Return localized name for display, with English in parentheses if different
            results = []
            for match in translated_matches:
                localized = match['matched_name']
                english = match['en_name']
                if localized and localized != english:
                    # Show: "Localized Name (English)"
                    display = f"{localized} ({english})" if len(f"{localized} ({english})") <= 100 else localized
                else:
                    display = english
                results.append((display, match['ref_id']))
            return results
        
        # Fallback to English
        return await self.get_base_item_suggestions(query)
    
    # ==================== End Translation Methods ====================
    
    async def get_villager_by_id(self, villager_id: int) -> Optional[Villager]:
        """Get a specific villager by ID"""
        return await self.repo.get_villager_by_id(villager_id)
    
    async def get_item_name_by_id(self, item_id: int) -> Optional[str]:
        """Get item name by ID"""
        return await self.repo.get_item_name_by_id(item_id)
    
    async def get_item_name_by_internal_id(self, internal_id: int) -> Optional[str]:
        """Get item name by internal_id or internal_group_id"""
        return await self.repo.get_item_name_by_internal_id(internal_id)

    async def get_item_variant_by_internal_group_and_indices(self, internal_group_id: int, primary_index: int, secondary_index: Optional[int] = None) -> Optional[tuple[str, str]]:
        """Get item name and variant display name by internal_group_id and variant indices"""
        return await self.repo.get_item_variant_by_internal_group_and_indices(internal_group_id, primary_index, secondary_index)
    
    async def get_recipe_by_id(self, recipe_id: int) -> Optional[Recipe]:
        """Get a specific recipe by ID with ingredients"""
        return await self.repo.get_recipe_by_id(recipe_id)
    
    async def get_recipe_suggestions(self, search_term: str, limit: int = 25) -> List[tuple[str, int]]:
        """Get recipe name suggestions for autocomplete"""
        try:
            return await self.repo.get_recipe_suggestions(search_term, limit)
        except Exception as e:
            logger.error(f"Error getting recipe suggestions: {e}")
            return []
    
    async def get_random_recipe_suggestions(self, limit: int = 25) -> List[tuple[str, int]]:
        """Get random recipe suggestions for autocomplete when query is too short"""
        try:
            random_recipes = await self.repo.get_random_recipes(limit)
            return [(recipe.name, recipe.id) for recipe in random_recipes if recipe.name]
        except Exception as e:
            logger.error(f"Error getting random recipe suggestions: {e}")
            return []
    
    async def get_artwork_by_id(self, artwork_id: int) -> Optional[Artwork]:
        """Get a specific artwork by ID"""
        return await self.repo.get_artwork_by_id(artwork_id)
    
    async def get_artwork_suggestions(self, search_term: str, limit: int = 25) -> List[tuple[str, int]]:
        """Get artwork name suggestions for autocomplete"""
        try:
            return await self.repo.get_artwork_suggestions(search_term, limit)
        except Exception as e:
            logger.error(f"Error getting artwork suggestions: {e}")
            return []
    
    async def get_random_artwork_suggestions(self, limit: int = 25) -> List[tuple[str, int]]:
        """Get random artwork suggestions for autocomplete when query is too short"""
        try:
            return await self.repo.get_random_artwork(limit)
        except Exception as e:
            logger.error(f"Error getting random artwork suggestions: {e}")
            return []
    
    async def get_critter_by_id(self, critter_id: int) -> Optional[Critter]:
        """Get a specific critter by ID"""
        return await self.repo.get_critter_by_id(critter_id)
    
    async def get_critter_suggestions(self, search_term: str, limit: int = 25) -> List[tuple[str, int]]:
        """Get critter name suggestions for autocomplete"""
        try:
            return await self.repo.get_critter_suggestions(search_term, limit)
        except Exception as e:
            logger.error(f"Error getting critter suggestions: {e}")
            return []
    
    async def get_random_critter_suggestions(self, limit: int = 25) -> List[tuple[str, int]]:
        """Get random critter suggestions for autocomplete when query is too short"""
        try:
            return await self.repo.get_random_critters(limit)
        except Exception as e:
            logger.error(f"Error getting random critter suggestions: {e}")
            return []
    
    async def get_fossil_by_id(self, fossil_id: int) -> Optional[Fossil]:
        """Get a specific fossil by ID"""
        return await self.repo.get_fossil_by_id(fossil_id)
    
    async def get_fossil_suggestions(self, search_term: str, limit: int = 25) -> List[tuple[str, int]]:
        """Get fossil name suggestions for autocomplete"""
        try:
            return await self.repo.get_fossil_suggestions(search_term, limit)
        except Exception as e:
            logger.error(f"Error getting fossil suggestions: {e}")
            return []
    
    async def get_random_fossil_suggestions(self, limit: int = 25) -> List[tuple[str, int]]:
        """Get random fossil suggestions for autocomplete when query is too short"""
        try:
            return await self.repo.get_random_fossils(limit)
        except Exception as e:
            logger.error(f"Error getting random fossil suggestions: {e}")
            return []
    
    async def browse_items(self, category: str = None, color: str = None, 
                          price_range: str = None, page: int = 0, per_page: int = 10) -> Dict[str, Any]:
        """Browse items with filtering and pagination"""
        offset = page * per_page
        items, total_count = await self.repo.browse_items(category, color, price_range, offset, per_page)
        
        total_pages = (total_count + per_page - 1) // per_page  # Ceiling division
        
        return {
            'items': items,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_items': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages - 1,
                'has_previous': page > 0
            }
        }
    
    async def browse_critters(self, kind: str = None, season: str = None, 
                             page: int = 0, per_page: int = 10) -> Dict[str, Any]:
        """Browse critters with filtering and pagination"""
        offset = page * per_page
        critters, total_count = await self.repo.browse_critters(kind, season, offset, per_page)
        
        total_pages = (total_count + per_page - 1) // per_page
        
        return {
            'critters': critters,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_items': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages - 1,
                'has_previous': page > 0
            }
        }
    
    
    async def browse_villagers(self, species: str = None, personality: str = None, 
                              page: int = 0, per_page: int = 10) -> Dict[str, Any]:
        """Browse villagers with filtering and pagination"""
        offset = page * per_page
        villagers, total_count = await self.repo.browse_villagers(species, personality, offset, per_page)
        
        total_pages = (total_count + per_page - 1) // per_page
        
        return {
            'villagers': villagers,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_items': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages - 1,
                'has_previous': page > 0
            }
        }
    
    # Methods to get filter options for commands
    async def get_filter_options(self) -> Dict[str, List[str]]:
        """Get all available filter options for commands"""
        return {
            'item_categories': await self.repo.get_item_categories(),
            'critter_kinds': await self.repo.get_critter_kinds(),
            'villager_species': await self.repo.get_villager_species(),
            'villager_personalities': await self.repo.get_villager_personalities(),
            'recipe_categories': await self.repo.get_recipe_categories()
        }
    
    async def get_villager_suggestions(self, query: str) -> List[tuple[str, int]]:
        """Get villager name and ID suggestions for autocomplete"""
        try:
            logger.debug(f"Getting villager suggestions for query: '{query}'")
            # Use FTS5 autocomplete search for villagers
            search_results = await self.repo.search_fts_autocomplete(query, category_filter="villager", limit=25)
            logger.debug(f"FTS autocomplete search returned {len(search_results)} villager results")
            
            suggestions = []
            for result in search_results:
                if result['ref_table'] == 'villagers':
                    suggestions.append((result['name'], result['ref_id']))
            
            # If no FTS results, get random villagers
            if not suggestions:
                logger.debug("No FTS results, getting random villagers")
                villagers_data = await self.browse_villagers(page=0, per_page=25)
                random_villagers = villagers_data['villagers']
                for villager in random_villagers:
                    suggestions.append((villager.name, villager.id))
            
            logger.debug(f"Returning {len(suggestions)} villager suggestions")
            return suggestions[:25]
        
        except Exception as e:
            logger.error(f"Error getting villager suggestions: {e}")
            # Fallback to empty list
            return []

    async def get_base_item_suggestions(self, query: str) -> List[tuple[str, int]]:
        """Get base item name and ID suggestions for autocomplete (no variants)"""
        try:
            logger.debug(f"Getting suggestions for query: '{query}'")
            # Use FTS5 autocomplete search for prefix matching
            search_results = await self.repo.search_fts_autocomplete(query, category_filter="item", limit=25)
            logger.debug(f"FTS autocomplete search returned {len(search_results)} results")
            
            # Filter to only items and batch resolve
            item_results = [r for r in search_results if r['ref_table'] == 'items']
            resolved_map = await self.repo.resolve_search_results_batch(item_results)
            
            base_items = []
            seen_names = set()
            
            for result in item_results:
                key = f"{result['ref_table']}:{result['ref_id']}"
                item = resolved_map.get(key)
                if item and item.name and item.name not in seen_names:
                    base_items.append((item.name, item.id))
                    seen_names.add(item.name)
                    logger.debug(f"Added item: {item.name} (ID: {item.id})")
            
            logger.debug(f"Returning {len(base_items)} unique base items: {[name for name, _ in base_items[:5]]}")
            return base_items
            
        except Exception as e:
            logger.error(f"Error getting base item suggestions: {e}")
            return []

    async def get_random_item_suggestions(self, limit: int = 25) -> List[tuple[str, int]]:
        """Get random item suggestions for autocomplete when query is too short"""
        try:
            logger.debug(f"Getting {limit} random item suggestions")
            
            # Get random items from the repository (request more to account for deduplication)
            random_items = await self.repo.get_random_items(limit * 2)
            
            # Deduplicate by name (keep first occurrence)
            seen_names = set()
            suggestions = []
            for item in random_items:
                if item.name and item.name not in seen_names:
                    suggestions.append((item.name, item.id))
                    seen_names.add(item.name)
                    if len(suggestions) >= limit:
                        break
            
            logger.debug(f"Returning {len(suggestions)} random items")
            return suggestions
            
        except Exception as e:
            logger.error(f"Error getting random item suggestions: {e}")
            return []

    async def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        try:
            stats = await self.repo.get_database_stats()
            
            return {
                **stats,
                "total_content": sum(stats.values()),
                "database_active": sum(stats.values()) > 0
            }
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {
                "error": str(e),
                "database_active": False
            }

# Backward compatibility alias
ACNHService = NooklookService
    
