import pathlib
import sqlite3
from typing import Optional, Dict, Any, List, Tuple
from .database import Database
from bot.models.acnh_item import Item, ItemVariant, Critter, Recipe, Villager

class NooklookRepository:
    """Repository for nooklook database operations"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default to nooklook.db in the root directory
            base_dir = pathlib.Path(__file__).parent.parent.parent
            db_path = base_dir / "nooklook.db"
        
        self.db = Database(str(db_path))
        self.base_dir = pathlib.Path(__file__).parent.parent.parent
    
    async def init_database(self):
        """Initialize the database connection"""
        # Database should already exist from import_all_datasets.py
        pass
    
    async def search_fts(self, query: str, category_filter: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Search using FTS5 search_index for strict matching"""
        # Use exact phrase matching for strict results
        fts_query = f'"{query.strip()}"'
        
        sql = """
            SELECT s.name, s.category, s.subcategory, s.ref_table, s.ref_id
            FROM search_index s
            WHERE s.name MATCH ?
        """
        params = [fts_query]
        
        if category_filter:
            sql += " AND s.category = ?"
            params.append(category_filter)
        
        sql += " ORDER by bm25(search_index) LIMIT ?"
        params.append(limit)
        
        return await self.db.execute_query(sql, params)
    
    def _escape_fts_query(self, query: str) -> str:
        """Escape FTS5 special characters"""
        # FTS5 special characters that need escaping: " ' - ( ) * 
        special_chars = ['"', "'", "-", "(", ")", "*"]
        escaped = query
        for char in special_chars:
            escaped = escaped.replace(char, f'"{char}"')
        return escaped

    async def search_fts_autocomplete(self, query: str, category_filter: str = None, limit: int = 25) -> List[Dict[str, Any]]:
        """Search using FTS5 for autocomplete with prefix matching"""
        query = query.strip()
        
        # Try multiple search strategies for better results with special characters
        results = []
        
        # Strategy 1: Try prefix matching (works for most cases)
        try:
            # Escape FTS5 special characters
            escaped_query = self._escape_fts_query(query)
            fts_query = f'{escaped_query}*'
            sql = """
                SELECT s.name, s.category, s.subcategory, s.ref_table, s.ref_id
                FROM search_index s
                WHERE s.name MATCH ?
            """
            params = [fts_query]
            
            if category_filter:
                sql += " AND s.category = ?"
                params.append(category_filter)
            
            sql += " ORDER BY bm25(search_index) LIMIT ?"
            params.append(limit)
            
            results = await self.db.execute_query(sql, params)
        except:
            # If FTS5 prefix matching fails, results will remain empty
            pass
        
        # Strategy 2: If prefix matching failed or returned few results, try LIKE matching
        if len(results) < 5:
            try:
                # Use LIKE for partial matching when FTS5 fails with special characters
                like_query = f'%{query}%'
                sql = """
                    SELECT s.name, s.category, s.subcategory, s.ref_table, s.ref_id
                    FROM search_index s
                    WHERE s.name LIKE ?
                """
                params = [like_query]
                
                if category_filter:
                    sql += " AND s.category = ?"
                    params.append(category_filter)
                
                sql += " ORDER BY CASE WHEN s.name LIKE ? THEN 0 ELSE 1 END, s.name LIMIT ?"
                params.extend([f'{query}%', limit])  # Prioritize items that start with the query
                
                like_results = await self.db.execute_query(sql, params)
                
                # Combine results, avoiding duplicates
                existing_ids = {r['ref_id'] for r in results}
                for result in like_results:
                    if result['ref_id'] not in existing_ids:
                        results.append(result)
                        if len(results) >= limit:
                            break
            except:
                pass
        
        return results[:limit]
    
    async def get_random_items(self, limit: int = 25) -> List[Item]:
        """Get random items from the database"""
        sql = """
            SELECT * FROM items 
            ORDER BY RANDOM() 
            LIMIT ?
        """
        
        item_data_list = await self.db.execute_query(sql, (limit,))
        
        items = []
        for item_data in item_data_list:
            item = Item.from_dict(item_data)
            items.append(item)
        
        return items
    
    async def get_item_by_id(self, item_id: int, load_variants: bool = True) -> Optional[Item]:
        """Get an item by its ID with optional variant loading"""
        item_query = "SELECT * FROM items WHERE id = ?"
        item_data = await self.db.execute_query_one(item_query, (item_id,))
        
        if not item_data:
            return None
        
        item = Item.from_dict(item_data)
        
        if load_variants:
            item.variants = await self.get_item_variants(item_id)
        
        return item
    
    async def get_item_name_by_id(self, item_id: int) -> Optional[str]:
        """Get just the item name by ID (lightweight)"""
        query = "SELECT name FROM items WHERE id = ?"
        result = await self.db.execute_query_one(query, (item_id,))
        return result['name'] if result else None
    
    async def get_item_name_by_internal_id(self, internal_id: int) -> Optional[str]:
        """Get item name by internal_group_id"""
        query = "SELECT name FROM items WHERE internal_group_id = ?"
        result = await self.db.execute_query_one(query, (internal_id,))
        return result['name'] if result else None
    
    async def get_item_variants(self, item_id: int) -> List[ItemVariant]:
        """Get all variants for an item"""
        query = "SELECT * FROM item_variants WHERE item_id = ? ORDER BY primary_index, secondary_index"
        results = await self.db.execute_query(query, (item_id,))
        
        return [ItemVariant.from_dict(row) for row in results]
    
    async def browse_items(self, category: str = None, color: str = None, 
                          price_range: str = None, offset: int = 0, limit: int = 10) -> Tuple[List[Item], int]:
        """Browse items with filtering - returns (items, total_count)"""
        # Build the base query
        base_query = "SELECT i.* FROM items i"
        count_query = "SELECT COUNT(*) as total FROM items i"
        
        # Build WHERE conditions
        where_conditions = []
        params = []
        
        if category:
            where_conditions.append("i.category = ?")
            params.append(category)
        
        # Color filtering through variants
        if color:
            base_query += " INNER JOIN item_variants iv ON i.id = iv.item_id"
            count_query += " INNER JOIN item_variants iv ON i.id = iv.item_id"
            where_conditions.append("(iv.color1 LIKE ? OR iv.color2 LIKE ?)")
            color_param = f"%{color}%"
            params.extend([color_param, color_param])
        
        # Price range filtering
        if price_range:
            if price_range == "under-1000":
                where_conditions.append("(i.sell_price < 1000 OR i.buy_price < 1000)")
            elif price_range == "1000-10000":
                where_conditions.append("((i.sell_price >= 1000 AND i.sell_price <= 10000) OR (i.buy_price >= 1000 AND i.buy_price <= 10000))")
            elif price_range == "over-10000":
                where_conditions.append("(i.sell_price > 10000 OR i.buy_price > 10000)")
        
        # Add WHERE clause if we have conditions
        if where_conditions:
            where_clause = " WHERE " + " AND ".join(where_conditions)
            base_query += where_clause
            count_query += where_clause
        
        # Get total count
        count_result = await self.db.execute_query_one(count_query, params)
        total_count = count_result['total'] if count_result else 0
        
        # Add pagination and ordering
        base_query += " ORDER BY i.name LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        # Execute query
        results = await self.db.execute_query(base_query, params)
        
        # Convert to Item objects and load variants
        items = []
        for row in results:
            item = Item.from_dict(row)
            item.variants = await self.get_item_variants(item.id)
            items.append(item)
        
        return items, total_count
    
    async def browse_critters(self, kind: str = None, season: str = None, 
                             offset: int = 0, limit: int = 10) -> Tuple[List[Critter], int]:
        """Browse critters with filtering - returns (critters, total_count)"""
        base_query = "SELECT * FROM critters"
        count_query = "SELECT COUNT(*) as total FROM critters"
        
        where_conditions = []
        params = []
        
        if kind:
            where_conditions.append("kind = ?")
            params.append(kind)
        
        # Season filtering (check if available in current season)
        if season:
            month_columns = {
                'spring': ['nh_mar', 'nh_apr', 'nh_may'],
                'summer': ['nh_jun', 'nh_jul', 'nh_aug'],
                'fall': ['nh_sep', 'nh_oct', 'nh_nov'],
                'winter': ['nh_dec', 'nh_jan', 'nh_feb']
            }
            if season in month_columns:
                season_conditions = []
                for month_col in month_columns[season]:
                    season_conditions.append(f"{month_col} IS NOT NULL AND {month_col} != ''")
                where_conditions.append(f"({' OR '.join(season_conditions)})")
        
        if where_conditions:
            where_clause = " WHERE " + " AND ".join(where_conditions)
            base_query += where_clause
            count_query += where_clause
        
        # Get total count
        count_result = await self.db.execute_query_one(count_query, params)
        total_count = count_result['total'] if count_result else 0
        
        # Add pagination and ordering
        base_query += " ORDER BY name LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        results = await self.db.execute_query(base_query, params)
        critters = [Critter.from_dict(row) for row in results]
        
        return critters, total_count
    
    async def browse_recipes(self, category: str = None, offset: int = 0, limit: int = 10) -> Tuple[List[Recipe], int]:
        """Browse recipes with filtering - returns (recipes, total_count)"""
        base_query = "SELECT * FROM recipes"
        count_query = "SELECT COUNT(*) as total FROM recipes"
        params = []
        
        if category:
            where_clause = " WHERE category = ?"
            base_query += where_clause
            count_query += where_clause
            params.append(category)
        
        # Get total count
        count_result = await self.db.execute_query_one(count_query, params)
        total_count = count_result['total'] if count_result else 0
        
        # Add pagination and ordering
        base_query += " ORDER BY name LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        results = await self.db.execute_query(base_query, params)
        
        # Convert to Recipe objects and load ingredients
        recipes = []
        for row in results:
            recipe = Recipe.from_dict(row)
            recipe.ingredients = await self.get_recipe_ingredients(recipe.id)
            recipes.append(recipe)
        
        return recipes, total_count
    
    async def get_recipe_ingredients(self, recipe_id: int) -> List[Tuple[str, int]]:
        """Get ingredients for a recipe"""
        query = "SELECT ingredient_name, quantity FROM recipe_ingredients WHERE recipe_id = ?"
        results = await self.db.execute_query(query, (recipe_id,))
        
        return [(row['ingredient_name'], row['quantity']) for row in results]
    
    async def browse_villagers(self, species: str = None, personality: str = None, 
                              offset: int = 0, limit: int = 10) -> Tuple[List[Villager], int]:
        """Browse villagers with filtering - returns (villagers, total_count)"""
        base_query = "SELECT * FROM villagers"
        count_query = "SELECT COUNT(*) as total FROM villagers"
        
        where_conditions = []
        params = []
        
        if species:
            where_conditions.append("species = ?")
            params.append(species)
        
        if personality:
            where_conditions.append("personality = ?")
            params.append(personality)
        
        if where_conditions:
            where_clause = " WHERE " + " AND ".join(where_conditions)
            base_query += where_clause
            count_query += where_clause
        
        # Get total count
        count_result = await self.db.execute_query_one(count_query, params)
        total_count = count_result['total'] if count_result else 0
        
        # Add pagination and ordering
        base_query += " ORDER BY name LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        results = await self.db.execute_query(base_query, params)
        villagers = [Villager.from_dict(row) for row in results]
        
        return villagers, total_count
    
    async def resolve_search_result(self, ref_table: str, ref_id: str) -> Optional[Any]:
        """Resolve a search result to the actual object"""
        try:
            obj_id = int(ref_id)
        except ValueError:
            return None
        
        if ref_table == 'items':
            return await self.get_item_by_id(obj_id)
        elif ref_table == 'critters':
            return await self.get_critter_by_id(obj_id)
        elif ref_table == 'recipes':
            return await self.get_recipe_by_id(obj_id)
        elif ref_table == 'villagers':
            return await self.get_villager_by_id(obj_id)
        elif ref_table == 'fossils':
            return await self.get_fossil_by_id(obj_id)
        elif ref_table == 'artwork':
            return await self.get_artwork_by_id(obj_id)
        
        return None
    
    async def get_critter_by_id(self, critter_id: int) -> Optional[Critter]:
        """Get a critter by ID"""
        query = "SELECT * FROM critters WHERE id = ?"
        result = await self.db.execute_query_one(query, (critter_id,))
        
        return Critter.from_dict(result) if result else None
    
    async def get_recipe_by_id(self, recipe_id: int) -> Optional[Recipe]:
        """Get a recipe by ID with ingredients"""
        query = "SELECT * FROM recipes WHERE id = ?"
        result = await self.db.execute_query_one(query, (recipe_id,))
        
        if not result:
            return None
        
        recipe = Recipe.from_dict(result)
        recipe.ingredients = await self.get_recipe_ingredients(recipe_id)
        return recipe
    
    async def get_villager_by_id(self, villager_id: int) -> Optional[Villager]:
        """Get a villager by ID"""
        query = "SELECT * FROM villagers WHERE id = ?"
        result = await self.db.execute_query_one(query, (villager_id,))
        
        return Villager.from_dict(result) if result else None
    
    async def get_fossil_by_id(self, fossil_id: int) -> Optional[Dict[str, Any]]:
        """Get a fossil by ID (simplified for now)"""
        query = "SELECT * FROM fossils WHERE id = ?"
        return await self.db.execute_query_one(query, (fossil_id,))
    
    async def get_artwork_by_id(self, artwork_id: int) -> Optional[Dict[str, Any]]:
        """Get artwork by ID (simplified for now)"""
        query = "SELECT * FROM artwork WHERE id = ?"
        return await self.db.execute_query_one(query, (artwork_id,))
    
    # Methods to get filter options
    async def get_item_categories(self) -> List[str]:
        """Get all available item categories"""
        query = "SELECT DISTINCT category FROM items ORDER BY category"
        results = await self.db.execute_query(query)
        return [row['category'] for row in results]
    
    async def get_critter_kinds(self) -> List[str]:
        """Get all available critter kinds"""
        query = "SELECT DISTINCT kind FROM critters ORDER BY kind"
        results = await self.db.execute_query(query)
        return [row['kind'] for row in results]
    
    async def get_villager_species(self) -> List[str]:
        """Get all available villager species"""
        query = "SELECT DISTINCT species FROM villagers WHERE species IS NOT NULL ORDER BY species"
        results = await self.db.execute_query(query)
        return [row['species'] for row in results]
    
    async def get_villager_personalities(self) -> List[str]:
        """Get all available villager personalities"""
        query = "SELECT DISTINCT personality FROM villagers WHERE personality IS NOT NULL ORDER BY personality"
        results = await self.db.execute_query(query)
        return [row['personality'] for row in results]
    
    async def get_recipe_categories(self) -> List[str]:
        """Get all available recipe categories"""
        query = "SELECT DISTINCT category FROM recipes WHERE category IS NOT NULL ORDER BY category"
        results = await self.db.execute_query(query)
        return [row['category'] for row in results]
    
    async def get_database_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        stats = {}
        
        # Count items
        result = await self.db.execute_query_one("SELECT COUNT(*) as count FROM items")
        stats['items'] = result['count'] if result else 0
        
        # Count variants
        result = await self.db.execute_query_one("SELECT COUNT(*) as count FROM item_variants")
        stats['variants'] = result['count'] if result else 0
        
        # Count critters
        result = await self.db.execute_query_one("SELECT COUNT(*) as count FROM critters")
        stats['critters'] = result['count'] if result else 0
        
        # Count recipes
        result = await self.db.execute_query_one("SELECT COUNT(*) as count FROM recipes")
        stats['recipes'] = result['count'] if result else 0
        
        # Count villagers
        result = await self.db.execute_query_one("SELECT COUNT(*) as count FROM villagers")
        stats['villagers'] = result['count'] if result else 0
        
        return stats