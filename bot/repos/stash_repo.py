"""Stash repository for user collection management"""

import pathlib
import logging
from typing import Optional, List, Dict, Any
from .database import Database

logger = logging.getLogger("bot.repos.stash_repo")

# Limits
MAX_STASHES_PER_USER = 5
MAX_ITEMS_PER_STASH = 40


class StashRepository:
    """Repository for user stash operations"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            repo_file = pathlib.Path(__file__)
            project_root = repo_file.parent.parent.parent
            db_path = str(project_root / "data" / "nooklook.db")
        
        self.db = Database(str(db_path))
    
    # =========================================================
    # STASH CRUD OPERATIONS
    # =========================================================
    
    async def get_user_stashes(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all stashes for a user"""
        query = """
            SELECT s.id, s.name, s.created_at, s.updated_at,
                   COUNT(si.id) as item_count
            FROM user_stashes s
            LEFT JOIN stash_items si ON s.id = si.stash_id
            WHERE s.user_id = ?
            GROUP BY s.id
            ORDER BY s.name
        """
        return await self.db.execute_query(query, (str(user_id),))
    
    async def get_user_stash_count(self, user_id: int) -> int:
        """Get the number of stashes a user has"""
        query = "SELECT COUNT(*) as count FROM user_stashes WHERE user_id = ?"
        result = await self.db.execute_query_one(query, (str(user_id),))
        return result['count'] if result else 0
    
    async def get_stash_by_id(self, stash_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific stash by ID (verifies ownership)"""
        query = """
            SELECT s.id, s.name, s.created_at, s.updated_at,
                   COUNT(si.id) as item_count
            FROM user_stashes s
            LEFT JOIN stash_items si ON s.id = si.stash_id
            WHERE s.id = ? AND s.user_id = ?
            GROUP BY s.id
        """
        return await self.db.execute_query_one(query, (stash_id, str(user_id)))
    
    async def get_stash_by_name(self, user_id: int, name: str) -> Optional[Dict[str, Any]]:
        """Get a stash by name for a user"""
        query = """
            SELECT s.id, s.name, s.created_at, s.updated_at,
                   COUNT(si.id) as item_count
            FROM user_stashes s
            LEFT JOIN stash_items si ON s.id = si.stash_id
            WHERE s.user_id = ? AND LOWER(s.name) = LOWER(?)
            GROUP BY s.id
        """
        return await self.db.execute_query_one(query, (str(user_id), name))
    
    async def create_stash(self, user_id: int, name: str) -> Optional[int]:
        """Create a new stash, returns stash ID or None if limit reached"""
        # Check stash count limit
        current_count = await self.get_user_stash_count(user_id)
        if current_count >= MAX_STASHES_PER_USER:
            return None
        
        # Check if name already exists
        existing = await self.get_stash_by_name(user_id, name)
        if existing:
            return None
        
        query = "INSERT INTO user_stashes (user_id, name) VALUES (?, ?)"
        await self.db.execute_command(query, (str(user_id), name))
        
        # Get the created stash ID
        result = await self.db.execute_query_one(
            "SELECT id FROM user_stashes WHERE user_id = ? AND name = ?",
            (str(user_id), name)
        )
        return result['id'] if result else None
    
    async def rename_stash(self, stash_id: int, user_id: int, new_name: str) -> bool:
        """Rename a stash, returns True if successful"""
        # Check if new name already exists
        existing = await self.get_stash_by_name(user_id, new_name)
        if existing and existing['id'] != stash_id:
            return False
        
        query = "UPDATE user_stashes SET name = ? WHERE id = ? AND user_id = ?"
        affected = await self.db.execute_command(query, (new_name, stash_id, str(user_id)))
        return affected > 0
    
    async def delete_stash(self, stash_id: int, user_id: int) -> bool:
        """Delete a stash and all its items, returns True if successful"""
        query = "DELETE FROM user_stashes WHERE id = ? AND user_id = ?"
        affected = await self.db.execute_command(query, (stash_id, str(user_id)))
        return affected > 0
    
    # =========================================================
    # STASH ITEM OPERATIONS
    # =========================================================
    
    async def get_stash_items(self, stash_id: int, user_id: int) -> List[Dict[str, Any]]:
        """Get all items in a stash (verifies ownership)"""
        query = """
            SELECT si.id, si.ref_table, si.ref_id, si.variant_id, si.display_name, si.added_at
            FROM stash_items si
            JOIN user_stashes s ON si.stash_id = s.id
            WHERE si.stash_id = ? AND s.user_id = ?
            ORDER BY si.added_at DESC
        """
        return await self.db.execute_query(query, (stash_id, str(user_id)))
    
    async def get_stash_item_count(self, stash_id: int) -> int:
        """Get the number of items in a stash"""
        query = "SELECT COUNT(*) as count FROM stash_items WHERE stash_id = ?"
        result = await self.db.execute_query_one(query, (stash_id,))
        return result['count'] if result else 0
    
    async def add_item_to_stash(
        self, 
        stash_id: int, 
        user_id: int, 
        ref_table: str, 
        ref_id: int, 
        display_name: str,
        variant_id: int = None
    ) -> tuple[bool, str]:
        """
        Add an item to a stash.
        
        Returns:
            (success, message) tuple
        """
        # Verify stash ownership
        stash = await self.get_stash_by_id(stash_id, user_id)
        if not stash:
            return False, "Stash not found"
        
        # Check item count limit
        item_count = await self.get_stash_item_count(stash_id)
        if item_count >= MAX_ITEMS_PER_STASH:
            return False, f"Stash is full ({MAX_ITEMS_PER_STASH} items max)"

        # Note: Duplicates are now allowed so users can add multiples for TI orders

        # Add the item
        query = """
            INSERT INTO stash_items (stash_id, ref_table, ref_id, variant_id, display_name)
            VALUES (?, ?, ?, ?, ?)
        """
        await self.db.execute_command(query, (stash_id, ref_table, ref_id, variant_id, display_name))
        return True, "Item added to stash"
    
    async def remove_item_from_stash(
        self, 
        stash_id: int, 
        user_id: int, 
        ref_table: str, 
        ref_id: int,
        variant_id: int = None
    ) -> bool:
        """Remove an item from a stash, returns True if successful"""
        # Verify stash ownership first
        stash = await self.get_stash_by_id(stash_id, user_id)
        if not stash:
            return False
        
        if variant_id is not None:
            query = "DELETE FROM stash_items WHERE stash_id = ? AND ref_table = ? AND ref_id = ? AND variant_id = ?"
            affected = await self.db.execute_command(query, (stash_id, ref_table, ref_id, variant_id))
        else:
            query = "DELETE FROM stash_items WHERE stash_id = ? AND ref_table = ? AND ref_id = ? AND variant_id IS NULL"
            affected = await self.db.execute_command(query, (stash_id, ref_table, ref_id))
        return affected > 0
    
    async def remove_item_by_id(self, item_id: int, user_id: int) -> bool:
        """Remove a stash item by its ID, returns True if successful"""
        # Verify ownership through join
        query = """
            DELETE FROM stash_items 
            WHERE id = ? AND stash_id IN (
                SELECT id FROM user_stashes WHERE user_id = ?
            )
        """
        affected = await self.db.execute_command(query, (item_id, str(user_id)))
        return affected > 0
    
    async def is_item_in_any_stash(self, user_id: int, ref_table: str, ref_id: int, variant_id: int = None) -> List[Dict[str, Any]]:
        """Check which of user's stashes contain this item (optionally with specific variant)"""
        if variant_id is not None:
            query = """
                SELECT s.id, s.name
                FROM user_stashes s
                JOIN stash_items si ON s.id = si.stash_id
                WHERE s.user_id = ? AND si.ref_table = ? AND si.ref_id = ? AND si.variant_id = ?
            """
            return await self.db.execute_query(query, (str(user_id), ref_table, ref_id, variant_id))
        else:
            query = """
                SELECT s.id, s.name
                FROM user_stashes s
                JOIN stash_items si ON s.id = si.stash_id
                WHERE s.user_id = ? AND si.ref_table = ? AND si.ref_id = ? AND si.variant_id IS NULL
            """
            return await self.db.execute_query(query, (str(user_id), ref_table, ref_id))
    
    async def clear_stash(self, stash_id: int, user_id: int) -> bool:
        """Remove all items from a stash, returns True if successful"""
        # Verify ownership
        stash = await self.get_stash_by_id(stash_id, user_id)
        if not stash:
            return False
        
        query = "DELETE FROM stash_items WHERE stash_id = ?"
        await self.db.execute_command(query, (stash_id,))
        return True
