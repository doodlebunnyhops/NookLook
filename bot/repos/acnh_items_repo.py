import pathlib
import aiosqlite
from typing import Optional, Dict, Any
from .database import Database
from ..models.acnh_item import ACNHItem

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
        """Get an item by its normalized name with all related data"""
        normalized_name = name.strip().lower()
        
        # Get main item data
        item_query = "SELECT * FROM acnh_items WHERE name_normalized = ?"
        item_data = await self.db.execute_query_one(item_query, (normalized_name,))
        
        if not item_data:
            return None
        
        item_id = item_data["id"]
        
        # Get related data
        themes_query = "SELECT theme FROM acnh_item_themes WHERE item_id = ?"
        themes = await self.db.execute_query(themes_query, (item_id,))
        item_data["themes"] = [t["theme"] for t in themes]
        
        functions_query = "SELECT function_name FROM acnh_item_functions WHERE item_id = ?"
        functions = await self.db.execute_query(functions_query, (item_id,))
        item_data["functions"] = [f["function_name"] for f in functions]
        
        buy_prices_query = "SELECT price, currency FROM acnh_item_buy_prices WHERE item_id = ?"
        buy_prices = await self.db.execute_query(buy_prices_query, (item_id,))
        item_data["buy"] = buy_prices
        
        availability_query = "SELECT source, note FROM acnh_item_availability WHERE item_id = ?"
        availability = await self.db.execute_query(availability_query, (item_id,))
        item_data["availability"] = [{"from": a["source"], "note": a["note"]} for a in availability]
        
        # Get variations with colors
        variations_query = "SELECT id, variation, pattern, image_url FROM acnh_item_variations WHERE item_id = ?"
        variations = await self.db.execute_query(variations_query, (item_id,))
        
        for variation in variations:
            colors_query = "SELECT color FROM acnh_variation_colors WHERE variation_id = ?"
            colors = await self.db.execute_query(colors_query, (variation["id"],))
            variation["colors"] = [c["color"] for c in colors]
            # Remove the internal id from the response
            del variation["id"]
        
        item_data["variations"] = variations
        
        # Convert to ACNHItem object
        return ACNHItem.from_dict(item_data)
    
    async def save_item(self, item: Dict[str, Any]) -> int:
        """Save an item to the database with full Nookipedia data structure"""
        # Start a transaction to ensure data consistency
        async with aiosqlite.connect(self.db.db_path) as db:
            try:
                # Insert main item record
                main_command = """
                    INSERT OR REPLACE INTO acnh_items 
                    (name, name_normalized, url, category, item_series, item_set, 
                     hha_category, hha_base, tag, lucky, lucky_season, sell_price,
                     variation_total, pattern_total, customizable, custom_kits, 
                     custom_kit_type, custom_body_part, custom_pattern_part,
                     grid_width, grid_length, height, door_decor, version_added, 
                     unlocked, notes, last_fetched)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """
                
                main_params = (
                    item["name"],
                    item["name"].strip().lower(),
                    item.get("url"),
                    item.get("category"),
                    item.get("item_series"),
                    item.get("item_set"),
                    item.get("hha_category"),
                    item.get("hha_base"),
                    item.get("tag"),
                    item.get("lucky", False),
                    item.get("lucky_season"),
                    item.get("sell"),
                    item.get("variation_total", 0),
                    item.get("pattern_total", 0),
                    item.get("customizable", False),
                    item.get("custom_kits", 0),
                    item.get("custom_kit_type"),
                    item.get("custom_body_part"),
                    item.get("custom_pattern_part"),
                    item.get("grid_width"),
                    item.get("grid_length"),
                    item.get("height"),
                    item.get("door_decor", False),
                    item.get("version_added"),
                    item.get("unlocked", True),
                    item.get("notes")
                )
                
                cursor = await db.execute(main_command, main_params)
                item_id = cursor.lastrowid
                
                # Clear existing related data for this item
                await db.execute("DELETE FROM acnh_item_themes WHERE item_id = ?", (item_id,))
                await db.execute("DELETE FROM acnh_item_functions WHERE item_id = ?", (item_id,))
                await db.execute("DELETE FROM acnh_item_buy_prices WHERE item_id = ?", (item_id,))
                await db.execute("DELETE FROM acnh_item_availability WHERE item_id = ?", (item_id,))
                await db.execute("DELETE FROM acnh_variation_colors WHERE variation_id IN (SELECT id FROM acnh_item_variations WHERE item_id = ?)", (item_id,))
                await db.execute("DELETE FROM acnh_item_variations WHERE item_id = ?", (item_id,))
                
                # Insert themes
                if "themes" in item and item["themes"]:
                    for theme in item["themes"]:
                        await db.execute(
                            "INSERT INTO acnh_item_themes (item_id, theme) VALUES (?, ?)",
                            (item_id, theme)
                        )
                
                # Insert functions
                if "functions" in item and item["functions"]:
                    for function in item["functions"]:
                        await db.execute(
                            "INSERT INTO acnh_item_functions (item_id, function_name) VALUES (?, ?)",
                            (item_id, function)
                        )
                
                # Insert buy prices
                if "buy" in item and item["buy"]:
                    for buy_info in item["buy"]:
                        await db.execute(
                            "INSERT INTO acnh_item_buy_prices (item_id, price, currency) VALUES (?, ?, ?)",
                            (item_id, buy_info.get("price"), buy_info.get("currency"))
                        )
                
                # Insert availability
                if "availability" in item and item["availability"]:
                    for avail in item["availability"]:
                        await db.execute(
                            "INSERT INTO acnh_item_availability (item_id, source, note) VALUES (?, ?, ?)",
                            (item_id, avail.get("from"), avail.get("note"))
                        )
                
                # Insert variations and their colors
                if "variations" in item and item["variations"]:
                    for variation in item["variations"]:
                        var_cursor = await db.execute(
                            "INSERT INTO acnh_item_variations (item_id, variation, pattern, image_url) VALUES (?, ?, ?, ?)",
                            (item_id, variation.get("variation"), variation.get("pattern"), variation.get("image_url"))
                        )
                        variation_id = var_cursor.lastrowid
                        
                        # Insert colors for this variation
                        if "colors" in variation and variation["colors"]:
                            for color in variation["colors"]:
                                await db.execute(
                                    "INSERT INTO acnh_variation_colors (variation_id, color) VALUES (?, ?)",
                                    (variation_id, color)
                                )
                
                await db.commit()
                return item_id
                
            except Exception as e:
                await db.rollback()
                raise e
    
    async def search_items_by_name_fuzzy(self, name_pattern: str) -> list[ACNHItem]:
        """Search for items using LIKE pattern matching"""
        query = """
            SELECT * FROM acnh_items 
            WHERE name_normalized LIKE ? 
            ORDER BY name
            LIMIT 10
        """
        pattern = f"%{name_pattern.strip().lower()}%"
        results = await self.db.execute_query(query, (pattern,))
        
        # Convert each result to ACNHItem (basic data only for search results)
        items = []
        for item_data in results:
            # For search results, we'll create simplified ACNHItem objects
            # Full data can be loaded later if needed
            item = ACNHItem.from_dict(item_data)
            items.append(item)
        
        return items
    
    async def get_all_item_names(self) -> list[str]:
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