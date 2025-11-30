"""User settings repository for preference management"""

import pathlib
import logging
from typing import Optional, Dict, Any, List
from .database import Database

logger = logging.getLogger("bot.repos.user_repo")

# Supported languages with display info
SUPPORTED_LANGUAGES = {
    'en': {'name': 'English', 'native': 'English', 'field': 'en_name'},
    'ja': {'name': 'Japanese', 'native': '日本語', 'field': 'ja_name'},
    'zh': {'name': 'Chinese (Simplified)', 'native': '简体中文', 'field': 'zh_name'},
    'ko': {'name': 'Korean', 'native': '한국어', 'field': 'ko_name'},
    'fr': {'name': 'French', 'native': 'Français', 'field': 'fr_name'},
    'de': {'name': 'German', 'native': 'Deutsch', 'field': 'de_name'},
    'es': {'name': 'Spanish', 'native': 'Español', 'field': 'es_name'},
    'it': {'name': 'Italian', 'native': 'Italiano', 'field': 'it_name'},
    'nl': {'name': 'Dutch', 'native': 'Nederlands', 'field': 'nl_name'},
    'ru': {'name': 'Russian', 'native': 'Русский', 'field': 'ru_name'},
}


class UserRepository:
    """Repository for user settings operations"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            repo_file = pathlib.Path(__file__)
            project_root = repo_file.parent.parent.parent
            db_path = str(project_root / "data" / "nooklook.db")
        
        self.db = Database(str(db_path))
    
    async def get_user_settings(self, user_id: int) -> Dict[str, Any]:
        """Get user settings, returning defaults if not exists"""
        query = """
            SELECT preferred_language, hemisphere, created_at, updated_at 
            FROM user_settings WHERE user_id = ?
        """
        result = await self.db.execute_query_one(query, (str(user_id),))
        
        if result is None:
            # Return defaults without creating a record
            return {
                "preferred_language": "en",
                "hemisphere": "north",
                "created_at": None,
                "updated_at": None,
                "is_new_user": True  # Flag indicating no settings exist
            }
        
        return {
            "preferred_language": result['preferred_language'],
            "hemisphere": result['hemisphere'],
            "created_at": result['created_at'],
            "updated_at": result['updated_at'],
            "is_new_user": False
        }
    
    async def is_new_user(self, user_id: int) -> bool:
        """Check if user has any settings stored (first time user)"""
        query = "SELECT 1 FROM user_settings WHERE user_id = ? LIMIT 1"
        result = await self.db.execute_query_one(query, (str(user_id),))
        return result is None
    
    async def get_user_language(self, user_id: int) -> str:
        """Get just the user's preferred language code"""
        settings = await self.get_user_settings(user_id)
        return settings.get('preferred_language', 'en')
    
    async def get_user_hemisphere(self, user_id: int) -> str:
        """Get just the user's hemisphere preference"""
        settings = await self.get_user_settings(user_id)
        return settings.get('hemisphere', 'north')
    
    async def set_preferred_language(self, user_id: int, language: str) -> bool:
        """Set user's preferred language"""
        # Validate language code
        if language not in SUPPORTED_LANGUAGES:
            logger.warning(f"Invalid language code: {language}")
            return False
        
        try:
            # Upsert - insert or update
            query = """
                INSERT INTO user_settings (user_id, preferred_language) 
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET 
                    preferred_language = excluded.preferred_language
            """
            await self.db.execute_command(query, (str(user_id), language))
            logger.info(f"Set language to {language} for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error setting language for user {user_id}: {e}")
            return False
    
    async def set_hemisphere(self, user_id: int, hemisphere: str) -> bool:
        """Set user's hemisphere preference"""
        if hemisphere not in ['north', 'south']:
            logger.warning(f"Invalid hemisphere: {hemisphere}")
            return False
        
        try:
            query = """
                INSERT INTO user_settings (user_id, hemisphere) 
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET 
                    hemisphere = excluded.hemisphere
            """
            await self.db.execute_command(query, (str(user_id), hemisphere))
            logger.info(f"Set hemisphere to {hemisphere} for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error setting hemisphere for user {user_id}: {e}")
            return False
    
    async def update_settings(self, user_id: int, **kwargs) -> bool:
        """Update multiple settings at once"""
        valid_fields = {'preferred_language', 'hemisphere'}
        updates = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not updates:
            return False
        
        # Validate values
        if 'preferred_language' in updates and updates['preferred_language'] not in SUPPORTED_LANGUAGES:
            return False
        if 'hemisphere' in updates and updates['hemisphere'] not in ['north', 'south']:
            return False
        
        try:
            # Build upsert query
            fields = ['user_id'] + list(updates.keys())
            placeholders = ', '.join(['?'] * len(fields))
            update_clause = ', '.join([f"{k} = excluded.{k}" for k in updates.keys()])
            
            query = f"""
                INSERT INTO user_settings ({', '.join(fields)}) 
                VALUES ({placeholders})
                ON CONFLICT(user_id) DO UPDATE SET {update_clause}
            """
            
            values = [str(user_id)] + list(updates.values())
            await self.db.execute_command(query, tuple(values))
            return True
        except Exception as e:
            logger.error(f"Error updating settings for user {user_id}: {e}")
            return False
    
    async def delete_user_settings(self, user_id: int) -> bool:
        """Delete user settings (reset to defaults)"""
        try:
            query = "DELETE FROM user_settings WHERE user_id = ?"
            affected = await self.db.execute_command(query, (str(user_id),))
            return affected > 0
        except Exception as e:
            logger.error(f"Error deleting settings for user {user_id}: {e}")
            return False
    
    @staticmethod
    def get_language_info(code: str) -> Optional[Dict[str, str]]:
        """Get display info for a language code"""
        return SUPPORTED_LANGUAGES.get(code)
    
    @staticmethod
    def get_all_languages() -> Dict[str, Dict[str, str]]:
        """Get all supported languages"""
        return SUPPORTED_LANGUAGES
