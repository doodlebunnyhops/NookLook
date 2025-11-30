"""Import translations from Nookipedia Cargo API into local database"""

import asyncio
import aiohttp
import logging
import argparse
import pathlib
import sys
from typing import Dict, List, Any

# Add project root to path
project_root = pathlib.Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from bot.repos.database import Database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Nookipedia Cargo API configuration
CARGO_API_URL = "https://nookipedia.com/w/api.php"

# Maps ref_table to Cargo table name and key field
TABLE_MAPPINGS = {
    'items': {
        'cargo_table': 'nh_language_name',
        'key_field': 'en_name',
        'match_field': 'name'  # Field in our items table
    },
    # TODO: Add mappings for villagers, etc. when needed
}

# Language field mappings for nh_language_name table
# These are the actual Cargo API field names
LANGUAGE_FIELDS = {
    'en': 'en_name',
    'ja': 'ja_name',
    'zh': 'zh_name',      # Simplified Chinese
    'ko': 'ko_name',
    'fr': 'fr_name',
    'de': 'de_name',
    'es': 'es_name',
    'it': 'it_name',
    'nl': 'nl_name',
    'ru': 'ru_name',
}


async def fetch_cargo_data(
    session: aiohttp.ClientSession,
    table: str,
    fields: str,
    limit: int = 500,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """Fetch data from Cargo API with pagination"""
    params = {
        'action': 'cargoquery',
        'tables': table,
        'fields': fields,
        'limit': limit,
        'offset': offset,
        'format': 'json',
        'origin': '*'
    }
    
    async with session.get(CARGO_API_URL, params=params) as response:
        if response.status != 200:
            logger.error(f"API error: {response.status}")
            return []
        
        data = await response.json()
        
        if 'cargoquery' not in data:
            logger.error(f"No cargoquery in response: {data.keys()}")
            return []
        
        return [item['title'] for item in data['cargoquery']]


async def fetch_all_translations(session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
    """Fetch all translations from Nookipedia"""
    # Build field list
    fields = ','.join(LANGUAGE_FIELDS.values())
    
    all_translations = []
    offset = 0
    limit = 500
    
    while True:
        logger.info(f"Fetching translations offset {offset}...")
        batch = await fetch_cargo_data(session, 'nh_language_name', fields, limit, offset)
        
        if not batch:
            break
        
        all_translations.extend(batch)
        
        if len(batch) < limit:
            break
        
        offset += limit
        await asyncio.sleep(0.5)  # Rate limiting
    
    logger.info(f"Fetched {len(all_translations)} translations total")
    return all_translations


async def get_item_ids(db: Database) -> Dict[str, int]:
    """Get mapping of item names to IDs from database"""
    query = "SELECT id, name FROM items"
    rows = await db.execute_query(query)
    return {row['name'].lower(): row['id'] for row in rows}


async def import_translations(dry_run: bool = False, clear_existing: bool = False):
    """Main import function"""
    db_path = project_root / "data" / "nooklook.db"
    db = Database(str(db_path))
    
    logger.info(f"Using database: {db_path}")
    
    # Get existing item names for matching
    item_ids = await get_item_ids(db)
    logger.info(f"Found {len(item_ids)} items in database")
    
    if not item_ids:
        logger.error("No items found in database. Run item import first.")
        return
    
    # Fetch translations from Nookipedia
    async with aiohttp.ClientSession() as session:
        translations = await fetch_all_translations(session)
    
    if not translations:
        logger.error("No translations fetched")
        return
    
    # Clear existing if requested
    if clear_existing and not dry_run:
        logger.info("Clearing existing translations...")
        await db.execute_command("DELETE FROM item_translations WHERE ref_table = 'items'")
    
    # Match and prepare inserts
    matched = 0
    unmatched = 0
    insert_data = []
    
    for trans in translations:
        en_name = trans.get('en_name', '').strip()
        if not en_name:
            continue
        
        # Try to match to our items
        item_id = item_ids.get(en_name.lower())
        
        if item_id:
            matched += 1
            insert_data.append({
                'ref_table': 'items',
                'ref_id': item_id,
                'en_name': en_name,
                'ja_name': trans.get('ja_name', ''),
                'zh_name': trans.get('zh_name', ''),
                'ko_name': trans.get('ko_name', ''),
                'fr_name': trans.get('fr_name', ''),
                'de_name': trans.get('de_name', ''),
                'es_name': trans.get('es_name', ''),
                'it_name': trans.get('it_name', ''),
                'nl_name': trans.get('nl_name', ''),
                'ru_name': trans.get('ru_name', ''),
            })
        else:
            unmatched += 1
            if unmatched <= 10:  # Show first 10 unmatched
                logger.debug(f"No match for: {en_name}")
    
    logger.info(f"Matched: {matched}, Unmatched: {unmatched}")
    
    if dry_run:
        logger.info("DRY RUN - no changes made")
        # Show sample
        if insert_data:
            sample = insert_data[0]
            logger.info(f"Sample translation: {sample['en_name']}")
            logger.info(f"  Japanese: {sample['ja_name']}")
            logger.info(f"  French: {sample['fr_name']}")
            logger.info(f"  German: {sample['de_name']}")
        await db.close()
        return
    
    # Insert translations
    if insert_data:
        logger.info(f"Inserting {len(insert_data)} translations...")
        
        query = """
            INSERT OR REPLACE INTO item_translations 
            (ref_table, ref_id, en_name, ja_name, zh_name, ko_name, 
             fr_name, de_name, es_name, it_name, nl_name, ru_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        batch_size = 100
        for i in range(0, len(insert_data), batch_size):
            batch = insert_data[i:i+batch_size]
            for row in batch:
                await db.execute_command(query, (
                    row['ref_table'], row['ref_id'], row['en_name'],
                    row['ja_name'], row['zh_name'], row['ko_name'],
                    row['fr_name'], row['de_name'], row['es_name'],
                    row['it_name'], row['nl_name'], row['ru_name']
                ))
            logger.info(f"Inserted {min(i+batch_size, len(insert_data))}/{len(insert_data)}")
        
        logger.info("Import complete!")
    
    await db.close()


def main():
    parser = argparse.ArgumentParser(description='Import translations from Nookipedia')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be imported without changes')
    parser.add_argument('--clear', action='store_true', help='Clear existing translations before import')
    args = parser.parse_args()
    
    asyncio.run(import_translations(dry_run=args.dry_run, clear_existing=args.clear))


if __name__ == '__main__':
    main()
