#!/usr/bin/env python3
"""
Manual URL Mappings

Handles events that need manual URL mapping because:
1. Names don't match Nookipedia API (e.g., "acorns and pine cones")
2. Events link to item pages rather than event pages (zodiac seasons)
3. Events link to category pages (blooming seasons -> bush starts)

These mappings supplement automatic Nookipedia enrichment.
"""

import sqlite3
from pathlib import Path
from typing import Dict


# Zodiac seasons -> fragment item pages
ZODIAC_URLS = {
    "Aquarius": "https://nookipedia.com/wiki/Item:Aquarius_fragment_(New_Horizons)",
    "Pisces": "https://nookipedia.com/wiki/Item:Pisces_fragment_(New_Horizons)",
    "Aries": "https://nookipedia.com/wiki/Item:Aries_fragment_(New_Horizons)",
    "Taurus": "https://nookipedia.com/wiki/Item:Taurus_fragment_(New_Horizons)",
    "Gemini": "https://nookipedia.com/wiki/Item:Gemini_fragment_(New_Horizons)",
    "Cancer": "https://nookipedia.com/wiki/Item:Cancer_fragment_(New_Horizons)",
    "Leo": "https://nookipedia.com/wiki/Item:Leo_fragment_(New_Horizons)",
    "Virgo": "https://nookipedia.com/wiki/Item:Virgo_fragment_(New_Horizons)",
    "Libra": "https://nookipedia.com/wiki/Item:Libra_fragment_(New_Horizons)",
    "Scorpio": "https://nookipedia.com/wiki/Item:Scorpio_fragment_(New_Horizons)",
    "Sagittarius": "https://nookipedia.com/wiki/Item:Sagittarius_fragment_(New_Horizons)",
    "Capricorn": "https://nookipedia.com/wiki/Item:Capricorn_fragment_(New_Horizons)",
}

# Blooming seasons -> bush start item pages
BLOOMING_URLS = {
    "azalea": "https://nookipedia.com/wiki/Item:Azalea_start_(New_Horizons)",
    "camellia": "https://nookipedia.com/wiki/Item:Camellia_start_(New_Horizons)",
    "hibiscus": "https://nookipedia.com/wiki/Item:Hibiscus_start_(New_Horizons)",
    "holly": "https://nookipedia.com/wiki/Item:Holly_start_(New_Horizons)",
    "hydrangea": "https://nookipedia.com/wiki/Item:Hydrangea_start_(New_Horizons)",
    "plumeria": "https://nookipedia.com/wiki/Item:Plumeria_start_(New_Horizons)",
    "tea olive": "https://nookipedia.com/wiki/Item:Tea-olive_start_(New_Horizons)",
}

# Crafting/material seasons -> recipe category pages
CRAFTING_URLS = {
    "acorns and pine cones": "https://nookipedia.com/wiki/DIY_recipes/Autumn",
}

# Special events with specific wiki pages
SPECIAL_URLS = {
    "Birthday": "https://nookipedia.com/wiki/Birthday",
}


def get_all_manual_mappings() -> Dict[str, str]:
    """Get all manual URL mappings combined."""
    mappings = {}
    mappings.update(ZODIAC_URLS)
    mappings.update(BLOOMING_URLS)
    mappings.update(CRAFTING_URLS)
    mappings.update(SPECIAL_URLS)
    return mappings


def apply_manual_url_mappings(db_path: str = None) -> Dict[str, int]:
    """
    Apply manual URL mappings to events in the database.
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        Stats dictionary with results
    """
    if db_path is None:
        db_path = _resolve_path("data/nooklook.db")
    
    print("\n" + "-" * 60)
    print("Applying Manual URL Mappings")
    print("-" * 60)
    
    mappings = get_all_manual_mappings()
    print(f"  {len(mappings)} manual mappings defined")
    
    stats = {
        "zodiac_updated": 0,
        "blooming_updated": 0,
        "crafting_updated": 0,
        "special_updated": 0,
        "total_updated": 0,
        "already_set": 0,
    }
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        for event_name, url in mappings.items():
            # Check current state
            cursor.execute(
                "SELECT id, nookipedia_url FROM events WHERE name = ?",
                (event_name,)
            )
            result = cursor.fetchone()
            
            if not result:
                continue
            
            event_id, current_url = result
            
            if current_url:
                stats["already_set"] += 1
                continue
            
            # Apply mapping
            cursor.execute(
                "UPDATE events SET nookipedia_url = ? WHERE id = ?",
                (url, event_id)
            )
            stats["total_updated"] += 1
            
            # Track by category
            if event_name in ZODIAC_URLS:
                stats["zodiac_updated"] += 1
            elif event_name in BLOOMING_URLS:
                stats["blooming_updated"] += 1
            elif event_name in CRAFTING_URLS:
                stats["crafting_updated"] += 1
            elif event_name in SPECIAL_URLS:
                stats["special_updated"] += 1
        
        conn.commit()
        
    finally:
        conn.close()
    
    print(f"  Updated: {stats['total_updated']}")
    print(f"    Zodiac: {stats['zodiac_updated']}")
    print(f"    Blooming: {stats['blooming_updated']}")
    print(f"    Crafting: {stats['crafting_updated']}")
    print(f"    Special: {stats['special_updated']}")
    print(f"  Already set: {stats['already_set']}")
    
    return stats


def _resolve_path(relative_path: str) -> Path:
    """Resolve a path relative to the project root."""
    path = Path(relative_path)
    if path.exists():
        return path
    
    for parent in [Path(".."), Path("../.."), Path("../../..")]:
        test_path = parent / relative_path
        if test_path.exists():
            return test_path
    
    return path
