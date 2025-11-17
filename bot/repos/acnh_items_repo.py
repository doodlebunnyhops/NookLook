import pathlib
import sqlite3
from typing import Optional, Dict, Any, List, Tuple
from .database import Database
from bot.models.acnh_item import Item, ItemVariant, Critter, Recipe, Villager, Artwork

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
        import logging
        logger = logging.getLogger(__name__)
        
        query = query.strip()
        
        # Try multiple search strategies for better results with special characters
        results = []
        
        # Strategy 1: Try prefix matching (works for most cases)
        try:
            # Escape FTS5 special characters
            escaped_query = self._escape_fts_query(query)
            fts_query = f'{escaped_query}*'
            logger.debug(f"FTS5 search: original='{query}' -> escaped='{escaped_query}' -> fts_query='{fts_query}' category='{category_filter}'")
            
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
            logger.debug(f"FTS5 search results: {len(results)} items found")
        except Exception as e:
            # If FTS5 prefix matching fails, results will remain empty
            logger.debug(f"FTS5 search failed: {e}")
            pass
        
        # Strategy 2: If prefix matching failed or returned few results, try LIKE matching
        if len(results) < 5:
            try:
                # Use LIKE for partial matching when FTS5 fails with special characters
                like_query = f'%{query}%'
                logger.debug(f"LIKE search: query='{like_query}' category='{category_filter}'")
                
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
                logger.debug(f"LIKE search results: {len(like_results)} items found")
                
                # Combine results, avoiding duplicates
                existing_ids = {r['ref_id'] for r in results}
                for result in like_results:
                    if result['ref_id'] not in existing_ids:
                        results.append(result)
                        if len(results) >= limit:
                            break
            except Exception as e:
                logger.debug(f"LIKE search failed: {e}")
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

    async def get_item_variant_by_internal_group_and_indices(self, internal_group_id: int, primary_index: int, secondary_index: Optional[int] = None) -> Optional[tuple[str, str]]:
        """Get item name and variant display name by internal_group_id and variant indices"""
        query = """
        SELECT i.name, v.variation_label, v.pattern_label 
        FROM items i 
        JOIN item_variants v ON i.id = v.item_id 
        WHERE i.internal_group_id = ? 
        AND v.primary_index = ? 
        AND (v.secondary_index = ? OR (v.secondary_index IS NULL AND ? IS NULL))
        """
        result = await self.db.execute_query_one(query, (internal_group_id, primary_index, secondary_index, secondary_index))
        
        if result:
            item_name = result['name']
            
            # Build display name from variant labels
            variant_parts = []
            if result['variation_label']:
                variant_parts.append(result['variation_label'])
            if result['pattern_label']:
                variant_parts.append(result['pattern_label'])
            
            variant_display = " / ".join(variant_parts) if variant_parts else "Default"
            return item_name, variant_display
        
        return None
    
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
    
    async def get_artwork_by_id(self, artwork_id: int) -> Optional[Artwork]:
        """Get artwork by ID"""
        query = "SELECT * FROM artwork WHERE id = ?"
        result = await self.db.execute_query_one(query, (artwork_id,))
        return Artwork.from_dict(result) if result else None
    
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
    
    async def get_recipe_suggestions(self, search_term: str, limit: int = 25) -> List[tuple[str, int]]:
        """Get recipe name suggestions for autocomplete"""
        # Use FTS5 search with fallback to LIKE search
        try:
            # First try FTS5 search on recipes
            fts_query = """
                SELECT r.name, r.id, rank
                FROM search_index si
                JOIN recipes r ON si.ref_table = 'recipes' AND si.ref_id = r.id
                WHERE search_index MATCH ?
                ORDER BY rank
                LIMIT ?
            """
            results = await self.db.execute_query(fts_query, (search_term, limit))
            
            if results:
                return [(row['name'], row['id']) for row in results]
            
        except Exception:
            pass  # Fall back to LIKE search
        
        # Fallback LIKE search for recipes
        like_query = """
            SELECT name, id FROM recipes 
            WHERE name LIKE ? 
            ORDER BY name 
            LIMIT ?
        """
        results = await self.db.execute_query(like_query, (f"%{search_term}%", limit))
        return [(row['name'], row['id']) for row in results]
    
    async def get_random_recipes(self, limit: int = 25) -> List['Recipe']:
        """Get random recipes for autocomplete when query is too short"""
        query = "SELECT * FROM recipes ORDER BY RANDOM() LIMIT ?"
        results = await self.db.execute_query(query, (limit,))
        
        recipes = []
        for row in results:
            recipe = Recipe.from_dict(row)
            # Don't load ingredients for autocomplete suggestions (performance)
            recipes.append(recipe)
        
        return recipes
    
    async def get_artwork_suggestions(self, search_term: str, limit: int = 25) -> List[tuple[str, int]]:
        """Get artwork name suggestions for autocomplete"""
        # Use FTS5 search with fallback to LIKE search
        try:
            # First try FTS5 search on artwork
            fts_query = """
                SELECT a.name, a.id, a.genuine, rank
                FROM search_index si
                JOIN artwork a ON si.ref_table = 'artwork' AND si.ref_id = a.id
                WHERE search_index MATCH ?
                ORDER BY rank
                LIMIT ?
            """
            results = await self.db.execute_query(fts_query, (search_term, limit))
            
            if results:
                suggestions = []
                for row in results:
                    authenticity = " (Genuine)" if row['genuine'] else " (Fake)"
                    display_name = f"{row['name']}{authenticity}"
                    suggestions.append((display_name, row['id']))
                return suggestions
            
        except Exception:
            pass  # Fall back to LIKE search
        
        # Fallback LIKE search for artwork
        like_query = """
            SELECT name, id, genuine FROM artwork 
            WHERE name LIKE ? 
            ORDER BY name 
            LIMIT ?
        """
        results = await self.db.execute_query(like_query, (f"%{search_term}%", limit))
        suggestions = []
        for row in results:
            authenticity = " (Genuine)" if row['genuine'] else " (Fake)"
            display_name = f"{row['name']}{authenticity}"
            suggestions.append((display_name, row['id']))
        return suggestions
    
    async def get_random_artwork(self, limit: int = 25) -> List[tuple[str, int]]:
        """Get random artwork for autocomplete when query is too short"""
        query = "SELECT name, id, genuine FROM artwork ORDER BY RANDOM() LIMIT ?"
        results = await self.db.execute_query(query, (limit,))
        
        suggestions = []
        for row in results:
            authenticity = " (Genuine)" if row['genuine'] else " (Fake)"
            display_name = f"{row['name']}{authenticity}"
            suggestions.append((display_name, row['id']))
        
        return suggestions
    
    async def get_critter_suggestions(self, search_term: str, limit: int = 25) -> List[tuple[str, int]]:
        """Get critter name suggestions for autocomplete"""
        # Use FTS5 search with fallback to LIKE search
        try:
            # First try FTS5 search on critters
            fts_query = """
                SELECT c.name, c.id, c.kind, rank
                FROM search_index si
                JOIN critters c ON si.ref_table = 'critters' AND si.ref_id = c.id
                WHERE search_index MATCH ?
                ORDER BY rank
                LIMIT ?
            """
            results = await self.db.execute_query(fts_query, (search_term, limit))
            
            if results:
                suggestions = []
                for row in results:
                    suggestions.append((row['name'], row['id']))
                return suggestions
            
        except Exception:
            pass  # Fall back to LIKE search
        
        # Fallback LIKE search for critters
        like_query = """
            SELECT name, id, kind FROM critters 
            WHERE name LIKE ? 
            ORDER BY name 
            LIMIT ?
        """
        results = await self.db.execute_query(like_query, (f"%{search_term}%", limit))
        suggestions = []
        for row in results:
            suggestions.append((row['name'], row['id']))
        return suggestions
    
    async def get_random_critters(self, limit: int = 25) -> List[tuple[str, int]]:
        """Get random critters for autocomplete when query is too short"""
        query = "SELECT name, id, kind FROM critters ORDER BY RANDOM() LIMIT ?"
        results = await self.db.execute_query(query, (limit,))
        
        suggestions = []
        for row in results:
            suggestions.append((row['name'], row['id']))
        
        return suggestions
    
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