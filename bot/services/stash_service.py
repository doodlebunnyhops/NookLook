"""Stash service for user collection business logic"""

import logging
from typing import Optional, List, Dict, Any
from bot.repos.stash_repo import StashRepository, MAX_STASHES_PER_USER, MAX_ITEMS_PER_STASH

logger = logging.getLogger("bot.services.stash_service")


class StashService:
    """Service layer for stash operations with business logic"""
    
    def __init__(self):
        self.repo = StashRepository()
    
    @property
    def max_stashes(self) -> int:
        return MAX_STASHES_PER_USER
    
    @property
    def max_items(self) -> int:
        return MAX_ITEMS_PER_STASH
    
    # =========================================================
    # STASH MANAGEMENT
    # =========================================================
    
    async def get_user_stashes(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all stashes for a user with item counts"""
        return await self.repo.get_user_stashes(user_id)
    
    async def get_stash(self, stash_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific stash by ID"""
        return await self.repo.get_stash_by_id(stash_id, user_id)
    
    async def get_stash_by_name(self, user_id: int, name: str) -> Optional[Dict[str, Any]]:
        """Get a stash by name"""
        return await self.repo.get_stash_by_name(user_id, name)
    
    async def create_stash(self, user_id: int, name: str) -> tuple[bool, str, Optional[int]]:
        """
        Create a new stash.
        
        Returns:
            (success, message, stash_id) tuple
        """
        # Validate name
        name = name.strip()
        if not name:
            return False, "Stash name cannot be empty", None
        
        if len(name) > 50:
            return False, "Stash name must be 50 characters or less", None
        
        # Check stash limit
        current_count = await self.repo.get_user_stash_count(user_id)
        if current_count >= MAX_STASHES_PER_USER:
            return False, f"You've reached the maximum of {MAX_STASHES_PER_USER} stashes", None
        
        # Check for duplicate name
        existing = await self.repo.get_stash_by_name(user_id, name)
        if existing:
            return False, f"You already have a stash named '{name}'", None
        
        # Create the stash
        stash_id = await self.repo.create_stash(user_id, name)
        if stash_id:
            logger.info(f"User {user_id} created stash '{name}' (ID: {stash_id})")
            return True, f"Created stash '{name}'", stash_id
        
        return False, "Failed to create stash", None
    
    async def rename_stash(self, stash_id: int, user_id: int, new_name: str) -> tuple[bool, str]:
        """Rename a stash"""
        new_name = new_name.strip()
        if not new_name:
            return False, "Stash name cannot be empty"
        
        if len(new_name) > 50:
            return False, "Stash name must be 50 characters or less"
        
        # Verify stash exists
        stash = await self.repo.get_stash_by_id(stash_id, user_id)
        if not stash:
            return False, "Stash not found"
        
        # Check for duplicate name
        existing = await self.repo.get_stash_by_name(user_id, new_name)
        if existing and existing['id'] != stash_id:
            return False, f"You already have a stash named '{new_name}'"
        
        success = await self.repo.rename_stash(stash_id, user_id, new_name)
        if success:
            logger.info(f"User {user_id} renamed stash {stash_id} to '{new_name}'")
            return True, f"Renamed stash to '{new_name}'"
        
        return False, "Failed to rename stash"
    
    async def delete_stash(self, stash_id: int, user_id: int) -> tuple[bool, str]:
        """Delete a stash and all its items"""
        stash = await self.repo.get_stash_by_id(stash_id, user_id)
        if not stash:
            return False, "Stash not found"
        
        stash_name = stash['name']
        success = await self.repo.delete_stash(stash_id, user_id)
        if success:
            logger.info(f"User {user_id} deleted stash '{stash_name}' (ID: {stash_id})")
            return True, f"Deleted stash '{stash_name}'"
        
        return False, "Failed to delete stash"
    
    async def clear_stash(self, stash_id: int, user_id: int) -> tuple[bool, str]:
        """Remove all items from a stash"""
        stash = await self.repo.get_stash_by_id(stash_id, user_id)
        if not stash:
            return False, "Stash not found"
        
        success = await self.repo.clear_stash(stash_id, user_id)
        if success:
            logger.info(f"User {user_id} cleared stash '{stash['name']}' (ID: {stash_id})")
            return True, f"Cleared all items from '{stash['name']}'"
        
        return False, "Failed to clear stash"
    
    # =========================================================
    # STASH ITEM MANAGEMENT
    # =========================================================
    
    async def get_stash_items(self, stash_id: int, user_id: int) -> List[Dict[str, Any]]:
        """Get all items in a stash"""
        return await self.repo.get_stash_items(stash_id, user_id)

    async def get_stash_item_count(self, stash_id: int) -> int:
        """Get the number of items in a stash"""
        return await self.repo.get_stash_item_count(stash_id)
    
    async def add_to_stash(
        self, 
        stash_id: int, 
        user_id: int, 
        ref_table: str, 
        ref_id: int, 
        display_name: str,
        variant_id: int = None
    ) -> tuple[bool, str]:
        """Add an item to a stash"""
        success, message = await self.repo.add_item_to_stash(
            stash_id, user_id, ref_table, ref_id, display_name, variant_id
        )
        
        if success:
            variant_info = f" (variant {variant_id})" if variant_id else ""
            logger.info(f"User {user_id} added {ref_table}:{ref_id}{variant_info} to stash {stash_id}")
        
        return success, message
    
    async def remove_from_stash(
        self, 
        stash_id: int, 
        user_id: int, 
        ref_table: str, 
        ref_id: int,
        variant_id: int = None
    ) -> tuple[bool, str]:
        """Remove an item from a stash"""
        success = await self.repo.remove_item_from_stash(stash_id, user_id, ref_table, ref_id, variant_id)
        
        if success:
            logger.info(f"User {user_id} removed {ref_table}:{ref_id} from stash {stash_id}")
            return True, "Item removed from stash"
        
        return False, "Item not found in stash"
    
    async def remove_item_by_id(self, item_id: int, user_id: int) -> tuple[bool, str]:
        """Remove a stash item by its ID"""
        success = await self.repo.remove_item_by_id(item_id, user_id)
        
        if success:
            logger.info(f"User {user_id} removed stash item {item_id}")
            return True, "Item removed from stash"
        
        return False, "Item not found"
    
    async def get_stashes_containing_item(
        self, 
        user_id: int, 
        ref_table: str, 
        ref_id: int,
        variant_id: int = None
    ) -> List[Dict[str, Any]]:
        """Get list of user's stashes that contain a specific item"""
        return await self.repo.is_item_in_any_stash(user_id, ref_table, ref_id, variant_id)
    
    # =========================================================
    # UTILITY METHODS
    # =========================================================
    
    def get_type_emoji(self, ref_table: str) -> str:
        """Get an emoji for the item type"""
        emojis = {
            'items': '🪑',
            'critters': '🦋',
            'recipes': '📖',
            'villagers': '🏠',
            'fossils': '🦴',
            'artwork': '🖼️'
        }
        return emojis.get(ref_table, '📦')
    
    def get_type_name(self, ref_table: str) -> str:
        """Get a friendly name for the item type"""
        names = {
            'items': 'Item',
            'critters': 'Critter',
            'recipes': 'Recipe',
            'villagers': 'Villager',
            'fossils': 'Fossil',
            'artwork': 'Artwork'
        }
        return names.get(ref_table, 'Unknown')
