import difflib
import logging
from typing import Optional, Dict, Any
from ..repos.acnh_items_repo import ACNHItemsRepository
from ..models.acnh_item import ACNHItem

logger = logging.getLogger("bot.acnh_service")

class ACNHService:
    """Service for handling ACNH item operations using local database"""
    
    def __init__(self):
        self.repo = ACNHItemsRepository()
    
    async def init_database(self):
        """Initialize the database"""
        await self.repo.init_database()
    
    def normalize_name(self, name: str) -> str:
        """Normalize item name for searching"""
        return name.strip().lower()
    
    async def get_item(self, query: str) -> Optional[ACNHItem]:
        """Get an item by name from local database"""
        # 1) Try exact match first
        item = await self.repo.get_item_by_name(query)
        if item:
            logger.debug(f"Found exact match: {item.name}")
            return item
        
        # 2) Try fuzzy search as fallback
        fuzzy_item = await self._fuzzy_search_cache(query)
        if fuzzy_item:
            logger.debug(f"Found fuzzy match: {fuzzy_item.name}")
            return fuzzy_item
        
        logger.debug(f"No item found for query: {query}")
        return None
    

    
    async def _fuzzy_search_cache(self, query: str) -> Optional[ACNHItem]:
        """Perform fuzzy search on cached items"""
        try:
            all_names = await self.repo.get_all_item_names()
            if not all_names:
                return None
            
            best_match = difflib.get_close_matches(
                self.normalize_name(query),
                [self.normalize_name(name) for name in all_names],
                n=1,
                cutoff=0.6
            )
            
            if not best_match:
                return None
            
            # Find the original name and get the item
            best_norm = best_match[0]
            for name in all_names:
                if self.normalize_name(name) == best_norm:
                    return await self.repo.get_item_by_name(name)
            
        except Exception as e:
            logger.error(f"Error in fuzzy search: {e}")
        
        return None
    

    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the cache"""
        count = await self.repo.count_items()
        return {
            "cached_items": count,
            "database_path": str(self.repo.db.db_path)
        }
    
    async def clear_cache(self) -> int:
        """Clear all cached items"""
        return await self.repo.clear_cache()
    
    async def clear_old_cache(self, days: int = 30) -> int:
        """Clear cached items older than specified days"""
        return await self.repo.clear_old_cache(days)
    
