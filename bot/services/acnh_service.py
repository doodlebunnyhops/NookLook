from typing import Optional, Dict, Any, List
from bot.repos.acnh_items_repo import NooklookRepository
from bot.models.acnh_item import Item, ItemVariant, Critter, Recipe, Villager, Artwork
import logging

logger = logging.getLogger("bot.acnh_service")

class NooklookService:
    """Service for handling nooklook database operations"""
    
    def __init__(self):
        self.repo = NooklookRepository()
    
    async def init_database(self):
        """Initialize the database"""
        await self.repo.init_database()
    
    async def close_connections(self):
        """Close any existing database connections for maintenance"""
        # Since we use aiosqlite with context managers, connections auto-close
        # But we can add any cleanup logic here if needed in the future
        logger.info("Database connections use auto-closing context managers - no manual cleanup needed")
    
    async def search_all(self, query: str, category_filter: str = None, recipe_subtype: str = None) -> List[Any]:
        """Search across all content types using FTS5 with prefix matching"""
        try:
            search_results = await self.repo.search_fts_autocomplete(query, category_filter, limit=50)
            
            # Resolve search results to actual objects
            resolved_items = []
            for result in search_results:
                obj = await self.repo.resolve_search_result(result['ref_table'], result['ref_id'])
                if obj:
                    # Filter recipes by subtype if specified
                    if recipe_subtype and hasattr(obj, 'is_food'):
                        if recipe_subtype == "food" and not obj.is_food():
                            continue  # Skip non-food recipes when looking for food
                        elif recipe_subtype == "diy" and obj.is_food():
                            continue  # Skip food recipes when looking for DIY
                    
                    resolved_items.append(obj)
            
            return resolved_items
            
        except Exception as e:
            logger.error(f"Error in search: {e}")
            return []
    
    async def get_item_by_id(self, item_id: int) -> Optional[Item]:
        """Get a specific item by ID with variants"""
        return await self.repo.get_item_by_id(item_id, load_variants=True)
    
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
    
    async def browse_recipes(self, category: str = None, page: int = 0, per_page: int = 10) -> Dict[str, Any]:
        """Browse recipes with filtering and pagination"""
        offset = page * per_page
        recipes, total_count = await self.repo.browse_recipes(category, offset, per_page)
        
        total_pages = (total_count + per_page - 1) // per_page
        
        return {
            'recipes': recipes,
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
            
            base_items = []
            seen_names = set()
            
            for result in search_results:
                if result['ref_table'] == 'items':
                    # Get the item to access its name and ID
                    item = await self.repo.resolve_search_result(result['ref_table'], result['ref_id'])
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
            
            # Get random items from the repository
            random_items = await self.repo.get_random_items(limit)
            
            # Return name, id tuples
            suggestions = [(item.name, item.id) for item in random_items if item.name]
            
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
    
