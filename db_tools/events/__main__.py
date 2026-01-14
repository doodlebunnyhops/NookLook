#!/usr/bin/env python3
"""
ACNH Events Import - Main Entry Point

A structured process for creating event-related tables and importing data.

Primary source: Google Sheets API (required)
Secondary source: Nookipedia API (optional enrichment)

Usage:
    python -m db_tools.events                    # Full import with enrichment
    python -m db_tools.events --no-enrich        # Google Sheets only
    python -m db_tools.events --items-only       # Just import event items
    python -m db_tools.events --check            # Check current state

Process:
    1. Initialize schema from schemas/events_schema.sql
    2. Import events from Google Sheets API (source of truth)
    3. Enrich with Nookipedia URLs (optional, uses API if token exists)
    4. Apply manual URL mappings (zodiac, blooming seasons, etc.)
    5. Import event items from Nookipedia HTML
"""

import argparse
import sqlite3
import sys
from pathlib import Path


def resolve_path(relative_path: str) -> Path:
    """Resolve a path relative to the project root."""
    path = Path(relative_path)
    if path.exists() or path.parent.exists():
        return path
    
    for parent in [Path(".."), Path("../.."), Path("../../..")]:
        test_path = parent / relative_path
        if test_path.exists() or test_path.parent.exists():
            return test_path
    
    return path


def check_status(db_path: str) -> None:
    """Check current state of events data."""
    db = resolve_path(db_path)
    
    if not db.exists():
        print(f"Database not found: {db}")
        return
    
    conn = sqlite3.connect(str(db))
    cursor = conn.cursor()
    
    print("\n" + "=" * 60)
    print("Events Database Status")
    print("=" * 60)
    
    # Events
    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM events WHERE nookipedia_url IS NOT NULL")
    with_urls = cursor.fetchone()[0]
    
    print(f"\nEvents:")
    print(f"  Total: {total_events}")
    print(f"  With Nookipedia URLs: {with_urls}")
    print(f"  Without URLs: {total_events - with_urls}")
    
    # Event types
    cursor.execute("""
        SELECT event_type, COUNT(*) 
        FROM events 
        GROUP BY event_type 
        ORDER BY COUNT(*) DESC
    """)
    print(f"\nEvent Types:")
    for event_type, count in cursor.fetchall():
        print(f"  {event_type}: {count}")
    
    # Dates
    cursor.execute("SELECT COUNT(*) FROM event_dates")
    total_dates = cursor.fetchone()[0]
    
    cursor.execute("SELECT MIN(year), MAX(year) FROM event_dates")
    min_year, max_year = cursor.fetchone()
    
    print(f"\nEvent Dates:")
    print(f"  Total: {total_dates}")
    print(f"  Year range: {min_year}-{max_year}")
    
    # Event Items
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='event_items'
    """)
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM event_items")
        total_items = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM event_items WHERE event_id IS NOT NULL")
        linked_items = cursor.fetchone()[0]
        
        print(f"\nEvent Items:")
        print(f"  Total: {total_items}")
        print(f"  Linked to events: {linked_items}")
    else:
        print(f"\nEvent Items: Table not created")
    
    # Missing URLs
    cursor.execute("""
        SELECT name FROM events 
        WHERE nookipedia_url IS NULL 
        ORDER BY name 
        LIMIT 10
    """)
    missing = cursor.fetchall()
    if missing:
        print(f"\nEvents missing URLs (first 10):")
        for (name,) in missing:
            print(f"  - {name}")
    
    conn.close()


def run_full_import(
    db_path: str = "data/nooklook.db",
    enrich: bool = True,
    import_items: bool = True,
    verbose: bool = False
) -> dict:
    """
    Run the full events import process.
    
    Args:
        db_path: Path to database
        enrich: Whether to enrich with Nookipedia URLs
        import_items: Whether to import event items
        verbose: Whether to show detailed output
        
    Returns:
        Combined stats from all steps
    """
    from .importer import EventImporter
    from .nookipedia_enricher import NookipediaEnricher
    from .event_items import EventItemsImporter
    from .url_mappings import apply_manual_url_mappings
    
    all_stats = {}
    db = str(resolve_path(db_path))
    
    # Step 1: Import from Google Sheets (required)
    print("\n" + "=" * 60)
    print("Step 1: Import Events from Google Sheets")
    print("=" * 60)
    
    try:
        importer = EventImporter(db_path=db)
        all_stats['events'] = importer.import_events()
    except Exception as e:
        print(f"Error importing events: {e}")
        return all_stats
    
    # Step 2: Enrich with Nookipedia URLs (optional)
    if enrich:
        print("\n" + "=" * 60)
        print("Step 2: Enrich with Nookipedia URLs")
        print("=" * 60)
        
        try:
            enricher = NookipediaEnricher(db_path=db)
            all_stats['nookipedia'] = enricher.enrich_events()
        except Exception as e:
            print(f"Warning: Nookipedia enrichment failed: {e}")
            all_stats['nookipedia'] = {'error': str(e)}
    
    # Step 3: Apply manual URL mappings
    if enrich:
        print("\n" + "=" * 60)
        print("Step 3: Apply Manual URL Mappings")
        print("=" * 60)
        
        try:
            all_stats['manual_urls'] = apply_manual_url_mappings(db_path=db)
        except Exception as e:
            print(f"Warning: Manual URL mappings failed: {e}")
            all_stats['manual_urls'] = {'error': str(e)}
    
    # Step 4: Import event items (optional)
    if import_items:
        print("\n" + "=" * 60)
        print("Step 4: Import Event Items")
        print("=" * 60)
        
        try:
            items_importer = EventItemsImporter(db_path=db)
            all_stats['items'] = items_importer.import_items()
        except Exception as e:
            print(f"Warning: Event items import failed: {e}")
            all_stats['items'] = {'error': str(e)}
    
    # Final summary
    print("\n" + "=" * 60)
    print("Import Complete - Final Summary")
    print("=" * 60)
    
    if 'events' in all_stats:
        print(f"\nEvents:")
        print(f"  Imported: {all_stats['events'].get('events_imported', 0)}")
        print(f"  Updated: {all_stats['events'].get('events_updated', 0)}")
        print(f"  Dates: {all_stats['events'].get('dates_imported', 0)}")
    
    if 'nookipedia' in all_stats and 'error' not in all_stats['nookipedia']:
        print(f"\nNookipedia Enrichment:")
        print(f"  URLs added: {all_stats['nookipedia'].get('urls_added', 0)}")
    
    if 'manual_urls' in all_stats and 'error' not in all_stats['manual_urls']:
        print(f"\nManual URL Mappings:")
        print(f"  Applied: {all_stats['manual_urls'].get('total_updated', 0)}")
    
    if 'items' in all_stats and 'error' not in all_stats['items']:
        print(f"\nEvent Items:")
        print(f"  Imported: {all_stats['items'].get('items_imported', 0)}")
        print(f"  Linked: {all_stats['items'].get('items_linked', 0)}")
    
    return all_stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='ACNH Events Import System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m db_tools.events                    # Full import
    python -m db_tools.events --no-enrich        # Skip Nookipedia enrichment
    python -m db_tools.events --no-items         # Skip event items
    python -m db_tools.events --check            # Check current state
        """
    )
    
    parser.add_argument(
        '--db', type=str, default='data/nooklook.db',
        help='Path to SQLite database'
    )
    parser.add_argument(
        '--no-enrich', action='store_true',
        help='Skip Nookipedia URL enrichment'
    )
    parser.add_argument(
        '--no-items', action='store_true',
        help='Skip event items import'
    )
    parser.add_argument(
        '--items-only', action='store_true',
        help='Only import event items (assumes events exist)'
    )
    parser.add_argument(
        '--check', action='store_true',
        help='Check current database state'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    if args.check:
        check_status(args.db)
        return
    
    if args.items_only:
        from .event_items import EventItemsImporter
        db = str(resolve_path(args.db))
        items_importer = EventItemsImporter(db_path=db)
        items_importer.import_items()
        return
    
    run_full_import(
        db_path=args.db,
        enrich=not args.no_enrich,
        import_items=not args.no_items,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
