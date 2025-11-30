"""Translation service for localized item lookups"""

import pathlib
import logging
from typing import Optional, Dict, Any, List
from ..repos.database import Database
from ..repos.user_repo import SUPPORTED_LANGUAGES

logger = logging.getLogger("bot.services.translation_service")


class TranslationService:
    """Service for retrieving translations and searching by localized names"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            repo_file = pathlib.Path(__file__)
            project_root = repo_file.parent.parent.parent
            db_path = str(project_root / "data" / "nooklook.db")
        
        self.db = Database(str(db_path))
    
    def _get_language_field(self, language: str) -> str:
        """Get the database field name for a language code"""
        lang_info = SUPPORTED_LANGUAGES.get(language, SUPPORTED_LANGUAGES['en'])
        return lang_info['field']
    
    async def get_item_translation(
        self, 
        ref_table: str, 
        ref_id: int, 
        language: str = 'en'
    ) -> Optional[str]:
        """Get a translated name for an item"""
        field = self._get_language_field(language)
        
        query = f"""
            SELECT {field} as translated_name 
            FROM item_translations 
            WHERE ref_table = ? AND ref_id = ?
        """
        
        result = await self.db.execute_query_one(query, (ref_table, ref_id))
        
        if result and result['translated_name']:
            return result['translated_name']
        
        return None
    
    async def get_all_translations(
        self, 
        ref_table: str, 
        ref_id: int
    ) -> Dict[str, str]:
        """Get all translations for an item"""
        query = """
            SELECT * FROM item_translations 
            WHERE ref_table = ? AND ref_id = ?
        """
        
        result = await self.db.execute_query_one(query, (ref_table, ref_id))
        
        if not result:
            return {}
        
        translations = {}
        for code, info in SUPPORTED_LANGUAGES.items():
            field = info['field']
            if field in result and result[field]:
                translations[code] = result[field]
        
        return translations
    
    async def search_by_translation(
        self, 
        search_term: str, 
        language: str = 'en',
        ref_table: str = 'items',
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Search for items by translated name.
        Returns list of matches with ref_id and all language names.
        """
        field = self._get_language_field(language)
        
        # Case-insensitive search with LIKE
        query = f"""
            SELECT ref_id, en_name, {field} as matched_name
            FROM item_translations 
            WHERE ref_table = ? AND {field} LIKE ?
            ORDER BY 
                CASE 
                    WHEN {field} = ? THEN 0 
                    WHEN {field} LIKE ? THEN 1 
                    ELSE 2 
                END,
                {field}
            LIMIT ?
        """
        
        results = await self.db.execute_query(
            query, 
            (ref_table, f'%{search_term}%', search_term, f'{search_term}%', limit)
        )
        
        return [
            {
                'ref_id': r['ref_id'],
                'en_name': r['en_name'],
                'matched_name': r['matched_name']
            }
            for r in results
        ]
    
    async def search_any_language(
        self, 
        search_term: str, 
        ref_table: str = 'items',
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Search across ALL languages for a match.
        Useful when language is unknown.
        """
        # Build OR clause for all language fields
        or_clauses = []
        for code, info in SUPPORTED_LANGUAGES.items():
            field = info['field']
            or_clauses.append(f"{field} LIKE ?")
        
        where_clause = ' OR '.join(or_clauses)
        pattern = f'%{search_term}%'
        params = [ref_table] + [pattern] * len(SUPPORTED_LANGUAGES) + [limit]
        
        query = f"""
            SELECT ref_id, en_name, 
                   ja_name, zh_name, ko_name, fr_name, 
                   de_name, es_name, it_name, nl_name, ru_name
            FROM item_translations 
            WHERE ref_table = ? AND ({where_clause})
            LIMIT ?
        """
        
        results = await self.db.execute_query(query, tuple(params))
        
        matches = []
        for r in results:
            # Find which language(s) matched
            matched_langs = []
            for code, info in SUPPORTED_LANGUAGES.items():
                field = info['field']
                if field in r and r[field] and search_term.lower() in r[field].lower():
                    matched_langs.append({
                        'language': code,
                        'name': r[field]
                    })
            
            matches.append({
                'ref_id': r['ref_id'],
                'en_name': r['en_name'],
                'matched_languages': matched_langs
            })
        
        return matches
    
    async def get_localized_name_or_fallback(
        self, 
        ref_table: str, 
        ref_id: int, 
        language: str,
        fallback_name: str
    ) -> str:
        """
        Get translated name if available, otherwise return fallback (usually English).
        """
        if language == 'en':
            return fallback_name
        
        translated = await self.get_item_translation(ref_table, ref_id, language)
        return translated or fallback_name
    
    async def has_translations(self, ref_table: str, ref_id: int) -> bool:
        """Check if an item has any translations"""
        query = """
            SELECT 1 FROM item_translations 
            WHERE ref_table = ? AND ref_id = ?
            LIMIT 1
        """
        result = await self.db.execute_query_one(query, (ref_table, ref_id))
        return result is not None
    
    async def get_translation_stats(self) -> Dict[str, Any]:
        """Get statistics about translation coverage"""
        # Total translations
        total_query = "SELECT COUNT(*) as count FROM item_translations"
        total = (await self.db.execute_query_one(total_query))['count']
        
        # By table
        by_table_query = """
            SELECT ref_table, COUNT(*) as count 
            FROM item_translations 
            GROUP BY ref_table
        """
        by_table = await self.db.execute_query(by_table_query)
        
        # Non-null count per language
        lang_coverage = {}
        for code, info in SUPPORTED_LANGUAGES.items():
            field = info['field']
            query = f"SELECT COUNT(*) as count FROM item_translations WHERE {field} IS NOT NULL AND {field} != ''"
            result = await self.db.execute_query_one(query)
            lang_coverage[code] = result['count']
        
        return {
            'total_translations': total,
            'by_table': {r['ref_table']: r['count'] for r in by_table},
            'language_coverage': lang_coverage
        }
