import pathlib
import aiosqlite
from typing import Optional, Dict, Any
from .database import Database
from bot.models.acnh_item import ACNHItem

class ACNHItemsRepository:
    """Repository for ACNH items database operations"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default to data folder
            base_dir = pathlib.Path(__file__).parent.parent.parent
            db_path = base_dir / "data" / "acnh_cache.db"
        
        self.db = Database(str(db_path))
        self.base_dir = pathlib.Path(__file__).parent.parent.parent
        self.schema_path = self.base_dir / "schemas" / "items.sql"
        self.queries_dir = self.base_dir / "schemas" / "queries"
    
    async def init_database(self):
        """Initialize the database with the schema"""
        await self.db.init_from_schema(str(self.schema_path))
    
    async def get_item_by_name(self, name: str) -> Optional[ACNHItem]:
        """Get an item by its normalized name"""
        normalized_name = name.strip().lower()
        
        # Get main item data
        item_query = "SELECT * FROM acnh_items WHERE name_normalized = ?"
        item_data = await self.db.execute_query_one(item_query, (normalized_name,))
        
        if not item_data:
            return None
        
        # Convert to ACNHItem object
        return ACNHItem.from_dict(item_data)
    
    async def save_item(self, item: Dict[str, Any]) -> int:
        """Save an item to the database with comprehensive structure matching your import system"""
        command = """
            INSERT OR REPLACE INTO acnh_items 
            (name, name_normalized, category, color_variant, hex_id, sell_price, hha_base, hha_category,
             grid_width, grid_length, item_series, item_set, tag, customizable, custom_kits, custom_kit_type,
             interact, outdoor, speaker_type, lighting_type, catalog, version_added, unlocked, filename,
             variant_id, internal_id, unique_entry_id, image_filename, image_url, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            item.get("name", ""),
            item.get("name", "").strip().lower(),
            item.get("category", ""),
            item.get("color_variant", ""),
            item.get("hex_id", ""),
            item.get("sell_price"),
            item.get("hha_base"),
            item.get("hha_category", ""),
            item.get("grid_width"),
            item.get("grid_length"),
            item.get("item_series", ""),
            item.get("item_set", ""),
            item.get("tag", ""),
            item.get("customizable", False),
            item.get("custom_kits", 0),
            item.get("custom_kit_type", ""),
            item.get("interact", ""),
            item.get("outdoor", ""),
            item.get("speaker_type", ""),
            item.get("lighting_type", ""),
            item.get("catalog", ""),
            item.get("version_added", ""),
            item.get("unlocked", ""),
            item.get("filename", ""),
            item.get("variant_id", ""),
            item.get("internal_id", ""),
            item.get("unique_entry_id", ""),
            item.get("image_filename", ""),
            item.get("image_url", ""),
            item.get("notes", "")
        )
        
        return await self.db.execute_command(command, params)
    
    async def search_items_by_name_fuzzy(self, name_pattern: str):
        """Search for items using LIKE pattern matching with smart ordering"""
        # Prioritize matches: exact -> starts with -> contains
        query = """
            SELECT * FROM acnh_items 
            WHERE name_normalized LIKE ? 
            ORDER BY 
                CASE 
                    WHEN name_normalized = ? THEN 1          -- Exact match
                    WHEN name_normalized LIKE ? THEN 2       -- Starts with
                    ELSE 3                                   -- Contains
                END,
                name
            LIMIT 100
        """
        pattern = name_pattern.strip().lower()
        contains_pattern = f"%{pattern}%"
        starts_with_pattern = f"{pattern}%"
        
        results = await self.db.execute_query(query, (contains_pattern, pattern, starts_with_pattern))
        
        # Convert each result to ACNHItem (basic data only for search results)
        items = []
        for item_data in results:
            # For search results, we'll create simplified ACNHItem objects
            # Full data can be loaded later if needed
            item = ACNHItem.from_dict(item_data)
            items.append(item)
        
        return items
    
    async def search_items_by_base_name_fuzzy(self, name_pattern: str):
        """Search for items using LIKE pattern matching with smart ordering"""
        # Prioritize matches: exact -> starts with -> contains
        query = """
            SELECT * FROM acnh_items 
            WHERE name LIKE ? 
            ORDER BY 
                CASE 
                    WHEN name = ? THEN 1          -- Exact match
                    WHEN name LIKE ? THEN 2       -- Starts with
                    ELSE 3                                   -- Contains
                END,
                name
            LIMIT 100
        """
        pattern = name_pattern.strip().lower()
        contains_pattern = f"%{pattern}%"
        starts_with_pattern = f"{pattern}%"
        
        results = await self.db.execute_query(query, (contains_pattern, pattern, starts_with_pattern))
        
        # Convert each result to ACNHItem (basic data only for search results)
        items = []
        for item_data in results:
            # For search results, we'll create simplified ACNHItem objects
            # Full data can be loaded later if needed
            item = ACNHItem.from_dict(item_data)
            items.append(item)
        
        return items
    
    async def get_all_item_names(self):
        """Get all item names for fuzzy matching"""
        query = "SELECT name FROM acnh_items ORDER BY name"
        results = await self.db.execute_query(query)
        return [item["name"] for item in results]
    
    async def count_items(self) -> int:
        """Get the total count of cached items"""
        query = "SELECT COUNT(*) as count FROM acnh_items"
        result = await self.db.execute_query_one(query)
        return result["count"] if result else 0
    
    async def clear_cache(self) -> int:
        """Clear all cached items"""
        command = "DELETE FROM acnh_items"
        return await self.db.execute_command(command)
    
    async def clear_old_cache(self, days: int = 30) -> int:
        """Clear cached items older than specified days"""
        command = "DELETE FROM acnh_items WHERE last_fetched < datetime('now', '-{} days')".format(days)
        return await self.db.execute_command(command)
    
    async def get_random_items_by_category(self, categories: list[str], limit: int = 25) -> list[ACNHItem]:
        """Get random items from specified categories"""
        if not categories:
            return []
        
        # Create placeholders for the categories
        placeholders = ','.join(['?' for _ in categories])
        query = f"""
            SELECT * FROM acnh_items 
            WHERE category IN ({placeholders})
            ORDER BY RANDOM() 
            LIMIT ?
        """
        
        params = tuple(categories) + (limit,)
        results = await self.db.execute_query(query, params)
        
        items = []
        for item_data in results:
            item = ACNHItem.from_dict(item_data)
            items.append(item)
        
        return items