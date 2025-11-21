"""Server settings repository for guild configuration management"""

import pathlib
import logging
from typing import Optional, Dict, Any, List
from .database import Database

logger = logging.getLogger("bot.repos.server_repo")

class ServerRepository:
    """Repository for server/guild settings operations"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Use absolute path based on this file's location
            repo_file = pathlib.Path(__file__)  # This file is bot/repos/server_repo.py
            project_root = repo_file.parent.parent.parent  # Go up to project root
            db_path = str(project_root / "data" / "nooklook.db")
            
            # Debug logging to track the path calculation
            logger.debug(f" ServerRepository __init__: __file__ = {repo_file}")
            logger.debug(f" ServerRepository __init__: project_root = {project_root}")
            logger.debug(f" ServerRepository __init__: calculated db_path = {db_path}")
            logger.debug(f" ServerRepository __init__: db_path exists = {pathlib.Path(db_path).exists()}")
        
        self.db = Database(str(db_path))
    
    async def get_guild_settings(self, guild_id: int) -> Dict[str, Any]:
        """Get guild settings from database, creating default if not exists"""
        query = "SELECT ephemeral_responses, created_at, updated_at FROM guild_settings WHERE guild_id = ?"
        result = await self.db.execute_query_one(query, (str(guild_id),))
        
        if result is None:
            # Create default settings (False = public responses by default)
            await self.db.execute_command(
                "INSERT INTO guild_settings (guild_id, ephemeral_responses) VALUES (?, ?)",
                (str(guild_id), False)
            )
            logger.info(f"Created default settings for guild {guild_id} with public responses")
            return {
                "ephemeral_responses": False,
                "created_at": None,
                "updated_at": None
            }
        else:
            return {
                "ephemeral_responses": bool(result['ephemeral_responses']),
                "created_at": result['created_at'],
                "updated_at": result['updated_at']
            }
    
    async def get_guild_settings_if_exists(self, guild_id: int) -> Optional[Dict[str, Any]]:
        """Get guild settings from database without creating if they don't exist"""
        query = "SELECT ephemeral_responses, created_at, updated_at FROM guild_settings WHERE guild_id = ?"
        result = await self.db.execute_query_one(query, (str(guild_id),))
        
        if result is None:
            return None  # Return None if no settings exist
        else:
            return {
                "ephemeral_responses": bool(result['ephemeral_responses']),
                "created_at": result['created_at'],
                "updated_at": result['updated_at']
            }
    
    async def update_ephemeral_setting(self, guild_id: int, ephemeral_responses: bool) -> bool:
        """Update ephemeral responses setting for a guild"""
        try:
            # First ensure the guild exists in the table
            await self._ensure_guild_exists(guild_id)
            
            # Update the setting
            affected_rows = await self.db.execute_command(
                "UPDATE guild_settings SET ephemeral_responses = ? WHERE guild_id = ?",
                (ephemeral_responses, str(guild_id))
            )
            
            if affected_rows > 0:
                logger.info(f"Updated ephemeral_responses to {ephemeral_responses} for guild {guild_id}")
                return True
            else:
                logger.warning(f"No rows updated for guild {guild_id} - guild may not exist")
                return False
                
        except Exception as e:
            logger.error(f"Error updating ephemeral setting for guild {guild_id}: {e}")
            return False
    
    async def _ensure_guild_exists(self, guild_id: int):
        """Ensure a guild exists in the guild_settings table"""
        query = "SELECT 1 FROM guild_settings WHERE guild_id = ?"
        exists = await self.db.execute_query_one(query, (str(guild_id),))
        
        if not exists:
            await self.db.execute_command(
                "INSERT INTO guild_settings (guild_id, ephemeral_responses) VALUES (?, ?)",
                (str(guild_id), False)
            )
            logger.info(f"Created guild_settings entry for guild {guild_id} with public responses")
    
    async def get_all_guild_settings(self) -> List[Dict[str, Any]]:
        """Get all guild settings (for administrative purposes)"""
        query = "SELECT guild_id, ephemeral_responses, created_at, updated_at FROM guild_settings ORDER BY created_at DESC"
        results = await self.db.execute_query(query)
        
        return [
            {
                "guild_id": row["guild_id"],
                "ephemeral_responses": bool(row["ephemeral_responses"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            for row in results
        ]
    
    async def delete_guild_settings(self, guild_id: int) -> bool:
        """Delete guild settings (for when bot leaves a server)"""
        try:
            affected_rows = await self.db.execute_command(
                "DELETE FROM guild_settings WHERE guild_id = ?",
                (str(guild_id),)
            )
            
            if affected_rows > 0:
                logger.info(f"Deleted guild settings for guild {guild_id}")
                return True
            else:
                logger.warning(f"No guild settings found to delete for guild {guild_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting guild settings for guild {guild_id}: {e}")
            return False
    
    async def get_guilds_with_setting(self, setting_name: str, setting_value: Any) -> List[str]:
        """Get list of guild IDs that have a specific setting value"""
        if setting_name not in ["ephemeral_responses"]:
            raise ValueError(f"Invalid setting name: {setting_name}")
        
        query = f"SELECT guild_id FROM guild_settings WHERE {setting_name} = ?"
        results = await self.db.execute_query(query, (setting_value,))
        
        return [row["guild_id"] for row in results]