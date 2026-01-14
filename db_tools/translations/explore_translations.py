"""
Fetch and explore data from Nookipedia Cargo tables.

This is a proof-of-concept script to test the Cargo API before
implementing full import functionality.

Usage:
    python -m db_tools.translations.explore_translations
    
    # Or from project root:
    python db_tools/translations/explore_translations.py
    python db_tools/translations/explore_translations.py fish
    python db_tools/translations/explore_translations.py art
    python db_tools/translations/explore_translations.py tables
"""

import asyncio
import aiohttp
import json
from typing import Dict, List, Any
from pathlib import Path

CARGO_API_URL = "https://nookipedia.com/w/api.php"

# ===== LANGUAGE/TRANSLATION CONFIGURATION =====

LANGUAGE_FIELDS = [
    'en_name', 'ja_name', 'zh_name', 'ko_name', 
    'fr_name', 'de_name', 'es_name', 'it_name', 
    'nl_name', 'ru_name'
]

SUPPORTED_LANGUAGES = {
    'en': {'name': 'English', 'native': 'English'},
    'ja': {'name': 'Japanese', 'native': '日本語'},
    'zh': {'name': 'Chinese (Simplified)', 'native': '简体中文'},
    'ko': {'name': 'Korean', 'native': '한국어'},
    'fr': {'name': 'French', 'native': 'Français'},
    'de': {'name': 'German', 'native': 'Deutsch'},
    'es': {'name': 'Spanish', 'native': 'Español'},
    'it': {'name': 'Italian', 'native': 'Italiano'},
    'nl': {'name': 'Dutch', 'native': 'Nederlands'},
    'ru': {'name': 'Russian', 'native': 'Русский'},
}

# Cargo types available in nh_language_name
CARGO_TYPES = [
    'Clothing',
    'Furniture', 
    'Gyroid',
    'Interior',
    'Other Item',
    'Photo',
    'Poster',
    'Special character',
    'Tool',
    'Villager'
]

# ===== ADDITIONAL CARGO TABLES =====

# Tables for critters, art, fossils, recipes (no translations in nh_language_name)
CARGO_TABLES = {
    'nh_fish': {
        'fields': ['name', 'number', 'location', 'shadow_size', 'rarity', 
                   'sell_nook', 'sell_cj', 'catchphrase', 'n_availability', 
                   's_availability', 'time', 'image_url', 'render_url'],
        'key': 'name'
    },
    'nh_bug': {
        'fields': ['name', 'number', 'location', 'rarity', 'sell_nook', 
                   'sell_flick', 'catchphrase', 'weather', 'n_availability',
                   's_availability', 'time', 'image_url', 'render_url'],
        'key': 'name'
    },
    'nh_sea_creature': {
        'fields': ['name', 'number', 'shadow_size', 'shadow_movement', 'rarity',
                   'sell_nook', 'catchphrase', 'n_availability', 's_availability',
                   'time', 'image_url', 'render_url'],
        'key': 'name'
    },
    'nh_art': {
        'fields': ['name', 'art_name', 'author', 'year', 'art_style', 'art_type',
                   'has_fake', 'authenticity', 'buy_price', 'sell', 
                   'image_url', 'fake_image_url'],
        'key': 'name'
    },
    'nh_fossil': {
        'fields': ['name', 'fossil_group', 'sell', 'hha_base', 'color1', 'color2',
                   'interactable', 'image_url'],
        'key': 'name'
    },
    'nh_recipe': {
        'fields': ['en_name', 'type', 'card_color', 'internal_id', 'sell',
                   'material1', 'material1_num', 'material2', 'material2_num',
                   'material3', 'material3_num', 'material4', 'material4_num',
                   'material5', 'material5_num', 'material6', 'material6_num',
                   'diy_availability1', 'diy_availability1_note', 'image_url'],
        'key': 'en_name'
    },
}


async def fetch_translations_batch(
    session: aiohttp.ClientSession, 
    item_type: str, 
    offset: int = 0,
    limit: int = 500
) -> List[Dict[str, Any]]:
    """Fetch a batch of translations from Nookipedia Cargo API"""
    
    params = {
        'action': 'cargoquery',
        'tables': 'nh_language_name',
        'fields': ','.join(LANGUAGE_FIELDS),
        'format': 'json',
        'where': f'type="{item_type}"',
        'limit': limit,
        'offset': offset
    }
    
    try:
        async with session.get(CARGO_API_URL, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                return [item['title'] for item in data.get('cargoquery', [])]
            else:
                print(f"  ❌ HTTP {resp.status} for {item_type}")
                return []
    except Exception as e:
        print(f"  ❌ Error fetching {item_type}: {e}")
        return []


async def fetch_all_for_type(session: aiohttp.ClientSession, item_type: str) -> List[Dict[str, Any]]:
    """Fetch all translations for a given type with pagination"""
    
    all_items = []
    offset = 0
    batch_size = 500
    
    while True:
        batch = await fetch_translations_batch(session, item_type, offset, batch_size)
        if not batch:
            break
            
        all_items.extend(batch)
        print(f"    Fetched {len(all_items)} {item_type} items...")
        offset += batch_size
        
        # Rate limiting - be nice to Nookipedia
        await asyncio.sleep(0.3)
    
    return all_items


async def fetch_sample(item_type: str = "Furniture", limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch a small sample of translations for testing"""
    
    async with aiohttp.ClientSession() as session:
        return await fetch_translations_batch(session, item_type, 0, limit)


async def count_all_types() -> Dict[str, int]:
    """Count how many items of each type exist"""
    
    counts = {}
    
    async with aiohttp.ClientSession() as session:
        for item_type in CARGO_TYPES:
            items = await fetch_all_for_type(session, item_type)
            counts[item_type] = len(items)
            print(f"  ✓ {item_type}: {len(items)} items")
    
    return counts


async def search_by_name(name: str, language: str = 'en') -> List[Dict[str, Any]]:
    """Search for an item by name in a specific language"""
    
    field = f"{language}_name"
    
    params = {
        'action': 'cargoquery',
        'tables': 'nh_language_name',
        'fields': ','.join(LANGUAGE_FIELDS),
        'format': 'json',
        'where': f'{field} LIKE "%{name}%"',
        'limit': 25
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(CARGO_API_URL, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                return [item['title'] for item in data.get('cargoquery', [])]
            return []


async def export_sample(output_path: str = None):
    """Export a sample of translations to JSON for analysis"""
    
    if output_path is None:
        output_path = Path(__file__).parent.parent.parent / "data" / "translation_sample.json"
    
    print("Fetching translation samples...")
    
    samples = {}
    async with aiohttp.ClientSession() as session:
        for item_type in CARGO_TYPES:
            print(f"  Fetching {item_type}...")
            samples[item_type] = await fetch_translations_batch(session, item_type, 0, 10)
            await asyncio.sleep(0.3)
    
    # Save to file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Saved samples to {output_path}")
    return samples


def display_item(item: Dict[str, Any]):
    """Pretty print a single item's translations"""
    
    print("\n" + "=" * 60)
    print(f"English: {item.get('en_name', 'N/A')}")
    print("-" * 60)
    
    for lang_code, lang_info in SUPPORTED_LANGUAGES.items():
        if lang_code == 'en':
            continue
        field = f"{lang_code}_name"
        value = item.get(field, '')
        if value:
            print(f"  {lang_info['native']:12} ({lang_code}): {value}")


# ===== CARGO TABLE EXPLORATION =====

async def fetch_cargo_table(
    session: aiohttp.ClientSession,
    table: str,
    fields: List[str],
    limit: int = 10,
    offset: int = 0,
    where: str = None
) -> List[Dict[str, Any]]:
    """Fetch data from any Cargo table"""
    
    params = {
        'action': 'cargoquery',
        'tables': table,
        'fields': ','.join(fields),
        'format': 'json',
        'limit': limit,
        'offset': offset
    }
    
    if where:
        params['where'] = where
    
    try:
        async with session.get(CARGO_API_URL, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                if 'error' in data:
                    print(f"  API Error: {data['error'].get('info', 'Unknown')}")
                    return []
                return [item['title'] for item in data.get('cargoquery', [])]
            else:
                print(f"  HTTP {resp.status}")
                return []
    except Exception as e:
        print(f"  Error: {e}")
        return []


async def explore_table(table: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Explore a specific Cargo table"""
    
    if table not in CARGO_TABLES:
        print(f"Unknown table: {table}")
        print(f"Available: {', '.join(CARGO_TABLES.keys())}")
        return []
    
    config = CARGO_TABLES[table]
    
    async with aiohttp.ClientSession() as session:
        return await fetch_cargo_table(session, table, config['fields'], limit)


async def count_table(table: str) -> int:
    """Count items in a Cargo table"""
    
    if table not in CARGO_TABLES:
        return 0
    
    config = CARGO_TABLES[table]
    key_field = config['key']
    
    async with aiohttp.ClientSession() as session:
        # Fetch in batches to count
        total = 0
        offset = 0
        while True:
            items = await fetch_cargo_table(session, table, [key_field], 500, offset)
            if not items:
                break
            total += len(items)
            offset += 500
            await asyncio.sleep(0.2)
        
        return total


def display_cargo_item(item: Dict[str, Any], table: str):
    """Pretty print a Cargo table item"""
    
    print("\n" + "=" * 60)
    
    # Determine the name field
    name = item.get('name') or item.get('en_name') or 'Unknown'
    print(f"📦 {name}")
    print("-" * 60)
    
    # Display based on table type
    if table == 'nh_fish':
        print(f"  Location: {item.get('location', 'N/A')}")
        print(f"  Shadow: {item.get('shadow_size', 'N/A')}")
        print(f"  Rarity: {item.get('rarity', 'N/A')}")
        print(f"  Sell: {item.get('sell_nook', 'N/A')} (CJ: {item.get('sell_cj', 'N/A')})")
        print(f"  Time: {item.get('time', 'N/A')}")
        print(f"  North: {item.get('n_availability', 'N/A')}")
        if item.get('catchphrase'):
            print(f"  💬 \"{item.get('catchphrase')}\"")
    
    elif table == 'nh_bug':
        print(f"  Location: {item.get('location', 'N/A')}")
        print(f"  Rarity: {item.get('rarity', 'N/A')}")
        print(f"  Sell: {item.get('sell_nook', 'N/A')} (Flick: {item.get('sell_flick', 'N/A')})")
        print(f"  Weather: {item.get('weather', 'Any')}")
        print(f"  Time: {item.get('time', 'N/A')}")
        if item.get('catchphrase'):
            print(f"  💬 \"{item.get('catchphrase')}\"")
    
    elif table == 'nh_sea_creature':
        print(f"  Shadow: {item.get('shadow_size', 'N/A')}")
        print(f"  Movement: {item.get('shadow_movement', 'N/A')}")
        print(f"  Rarity: {item.get('rarity', 'N/A')}")
        print(f"  Sell: {item.get('sell_nook', 'N/A')}")
        print(f"  Time: {item.get('time', 'N/A')}")
        if item.get('catchphrase'):
            print(f"  💬 \"{item.get('catchphrase')}\"")
    
    elif table == 'nh_art':
        print(f"  Real Name: {item.get('art_name', 'N/A')}")
        print(f"  Artist: {item.get('author', 'N/A')}")
        print(f"  Year: {item.get('year', 'N/A')}")
        print(f"  Style: {item.get('art_style', 'N/A')}")
        print(f"  Type: {item.get('art_type', 'N/A')}")
        print(f"  Has Fake: {'Yes' if item.get('has_fake') == '1' else 'No'}")
        if item.get('authenticity'):
            auth = item.get('authenticity', '')[:100]
            print(f"  🔍 {auth}...")
    
    elif table == 'nh_fossil':
        group = item.get('fossil_group', '')
        print(f"  Group: {group if group else 'Standalone'}")
        print(f"  Sell: {item.get('sell', 'N/A')}")
        print(f"  HHA: {item.get('hha_base', 'N/A')}")
        print(f"  Colors: {item.get('color1', 'N/A')} / {item.get('color2', 'N/A')}")
    
    elif table == 'nh_recipe':
        print(f"  Type: {item.get('type', 'N/A')}")
        print(f"  Card: {item.get('card_color', 'N/A')}")
        print(f"  Sell: {item.get('sell', 'N/A')}")
        print(f"  Source: {item.get('diy_availability1', 'N/A')}")
        
        # Show materials
        materials = []
        for i in range(1, 7):
            mat = item.get(f'material{i}')
            num = item.get(f'material{i}_num')
            if mat and mat.strip():
                materials.append(f"{num}x {mat}")
        if materials:
            print(f"  Materials: {', '.join(materials)}")
    
    else:
        # Generic display
        for key, value in item.items():
            if value and key not in ['image_url', 'render_url', 'fake_image_url']:
                print(f"  {key}: {value}")


async def demo_table(table: str):
    """Demo a specific Cargo table"""
    
    print(f"\n{'=' * 60}")
    print(f"Exploring: {table}")
    print('=' * 60)
    
    items = await explore_table(table, 5)
    
    for item in items:
        display_cargo_item(item, table)


async def list_all_tables():
    """List all available NH Cargo tables and their item counts"""
    
    print("=" * 60)
    print("Nookipedia NH Cargo Tables")
    print("=" * 60)
    
    # Get all tables
    async with aiohttp.ClientSession() as session:
        params = {'action': 'cargotables', 'format': 'json'}
        async with session.get(CARGO_API_URL, params=params) as resp:
            data = await resp.json()
            tables = data.get('cargotables', [])
    
    # Filter to NH tables
    nh_tables = [t for t in tables if t.startswith('nh_')]
    
    print(f"\nFound {len(nh_tables)} NH tables:\n")
    for table in sorted(nh_tables):
        print(f"  • {table}")
    
    return nh_tables


async def demo():
    """Run a demonstration of the translation API"""
    
    print("=" * 60)
    print("Nookipedia Translation API Explorer")
    print("=" * 60)
    
    # 1. Show a sample item with all translations
    print("\n📦 Sample Furniture Items:")
    print("-" * 60)
    
    samples = await fetch_sample("Furniture", 3)
    for item in samples:
        display_item(item)
    
    # 2. Show villager translations
    print("\n\n👤 Sample Villager Names:")
    print("-" * 60)
    
    villagers = await fetch_sample("Villager", 5)
    for v in villagers:
        display_item(v)
    
    # 3. Search example
    print("\n\n🔍 Search Example: 'chair' in English")
    print("-" * 60)
    
    results = await search_by_name("chair", "en")
    print(f"Found {len(results)} results")
    for r in results[:5]:
        print(f"  • {r.get('en_name')} → {r.get('ja_name', 'N/A')}")
    
    # 4. Search in Japanese
    print("\n\n🔍 Search Example: 'イス' (chair) in Japanese")
    print("-" * 60)
    
    results = await search_by_name("イス", "ja")
    print(f"Found {len(results)} results")
    for r in results[:5]:
        print(f"  • {r.get('ja_name')} → {r.get('en_name', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


async def full_count():
    """Count all items across all types"""
    
    print("=" * 60)
    print("Counting all items in nh_language_name table")
    print("=" * 60)
    
    counts = await count_all_types()
    
    print("\n" + "-" * 60)
    total = sum(counts.values())
    print(f"TOTAL: {total:,} items with translations")
    
    return counts


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "count":
            asyncio.run(full_count())
        elif command == "export":
            asyncio.run(export_sample())
        elif command == "search":
            if len(sys.argv) > 2:
                query = sys.argv[2]
                lang = sys.argv[3] if len(sys.argv) > 3 else 'en'
                results = asyncio.run(search_by_name(query, lang))
                print(f"Found {len(results)} results for '{query}' in {lang}:")
                for r in results:
                    display_item(r)
            else:
                print("Usage: python explore_translations.py search <query> [language]")
        elif command == "tables":
            asyncio.run(list_all_tables())
        elif command in CARGO_TABLES:
            # Explore a specific table
            asyncio.run(demo_table(command))
        elif command in ['fish', 'bug', 'bugs', 'sea', 'art', 'fossil', 'fossils', 'recipe', 'recipes']:
            # Shortcuts
            table_map = {
                'fish': 'nh_fish',
                'bug': 'nh_bug',
                'bugs': 'nh_bug',
                'sea': 'nh_sea_creature',
                'art': 'nh_art',
                'fossil': 'nh_fossil',
                'fossils': 'nh_fossil',
                'recipe': 'nh_recipe',
                'recipes': 'nh_recipe',
            }
            asyncio.run(demo_table(table_map[command]))
        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  count    - Count all translation items")
            print("  export   - Export sample translations to JSON")
            print("  search   - Search for items by name")
            print("  tables   - List all NH Cargo tables")
            print("\nTable shortcuts:")
            print("  fish, bug, sea, art, fossil, recipe")
            print("\nOr specify full table name:")
            print(f"  {', '.join(CARGO_TABLES.keys())}")
    else:
        # Run demo by default
        asyncio.run(demo())
