#!/usr/bin/env python3
"""
Mock Sheet Update - Simulate that the sheet was updated after your last import
This tricks the bot into thinking an update is needed
"""
import sqlite3
from datetime import datetime, timedelta
import pathlib

def mock_sheet_update():
    """
    Realistic mock: Set our last import time to be BEFORE the actual sheet modification time
    This simulates the real scenario where the sheet was updated after our last import
    """
    
    # Path to your database
    db_path = pathlib.Path("nooklook.db")
    
    if not db_path.exists():
        print("Database not found. Run import first.")
        return
    
    try:
        # First, get the REAL sheet modification time
        from import_all_datasets import ACNHDatasetImporter
        importer = ACNHDatasetImporter()
        
        print("🔍 Getting real sheet modification time...")
        sheet_info = importer.check_sheet_last_modified()
        
        if not sheet_info:
            print("Could not get sheet modification time")
            return
            
        real_sheet_modified = sheet_info['modified_time']
        print(f"Real sheet last modified: {real_sheet_modified}")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current import log
        cursor.execute("SELECT * FROM import_log ORDER BY id DESC LIMIT 1")
        current_log = cursor.fetchone()
        
        if not current_log:
            print("No import log found. Run an import first.")
            return
            
        print("\nCurrent import log:")
        print(f"   Import Time: {current_log[1]}")
        print(f"   Sheet Modified (recorded): {current_log[2]}")
        print(f"   Records: {current_log[3]}")
        
        # Set our import time to be 1 hour BEFORE the real sheet modification
        sheet_dt = datetime.fromisoformat(real_sheet_modified.replace('Z', '+00:00'))
        fake_import_time = (sheet_dt - timedelta(hours=1)).isoformat().replace('+00:00', '') + 'Z'
        
        cursor.execute("""
            UPDATE import_log 
            SET import_timestamp = ?, sheet_modified_time = ?
            WHERE id = ?
        """, (fake_import_time, fake_import_time, current_log[0]))
        
        conn.commit()
        conn.close()
        
        print(f"\nMocked scenario:")
        print(f"   Set our import time to: {fake_import_time}")
        print(f"   Real sheet modified at: {real_sheet_modified}")
        print(f"   Gap: Sheet appears to be updated 1 hour AFTER our import")
        print("\nNext bot data check will detect this as a needed update!")
        print("This simulates a real-world scenario where the sheet was updated after import")
        
    except Exception as e:
        print(f"Error mocking update: {e}")
        import traceback
        traceback.print_exc()

def delete_random_data():
    """Delete some random data to test if import properly restores it"""
    import random
    
    db_path = pathlib.Path("nooklook.db")
    if not db_path.exists():
        print("Database not found.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🗑️ Deleting random data for testing...")
        
        # Delete 10 random items
        cursor.execute("SELECT COUNT(*) FROM items")
        item_count = cursor.fetchone()[0]
        
        cursor.execute("DELETE FROM items WHERE id IN (SELECT id FROM items ORDER BY RANDOM() LIMIT 10)")
        items_deleted = cursor.rowcount
        
        # Delete 5 random villagers  
        cursor.execute("SELECT COUNT(*) FROM villagers")
        villager_count = cursor.fetchone()[0]
        
        cursor.execute("DELETE FROM villagers WHERE id IN (SELECT id FROM villagers ORDER BY RANDOM() LIMIT 5)")
        villagers_deleted = cursor.rowcount
        
        # Delete some item variants
        cursor.execute("DELETE FROM item_variants WHERE id IN (SELECT id FROM item_variants ORDER BY RANDOM() LIMIT 20)")
        variants_deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"Test deletion complete:")
        print(f"   Deleted {items_deleted} items (was {item_count})")
        print(f"   Deleted {villagers_deleted} villagers (was {villager_count})")  
        print(f"   Deleted {variants_deleted} variants")
        print(f"\nNext import should restore this data!")
        
    except Exception as e:
        print(f"Error deleting test data: {e}")

def check_for_duplicates():
    """Check the database for duplicate entries that might indicate import issues"""
    
    db_path = pathlib.Path("nooklook.db")
    if not db_path.exists():
        print("Database not found.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Checking for duplicate entries...")
        
        # Check for duplicate items by source_unique_id (these should be truly unique)
        cursor.execute("""
            SELECT source_unique_id, COUNT(*) as count, GROUP_CONCAT(name) as names
            FROM items 
            WHERE source_unique_id IS NOT NULL
            GROUP BY source_unique_id 
            HAVING count > 1 
            ORDER BY count DESC 
            LIMIT 10
        """)
        item_dupes = cursor.fetchall()
        
        # Check for duplicate villagers by source_unique_id
        cursor.execute("""
            SELECT source_unique_id, COUNT(*) as count, GROUP_CONCAT(name) as names
            FROM villagers 
            WHERE source_unique_id IS NOT NULL
            GROUP BY source_unique_id 
            HAVING count > 1 
            ORDER BY count DESC 
            LIMIT 10
        """)
        villager_dupes = cursor.fetchall()
        
        # Check for duplicate variants by source_unique_id (these should be unique)
        cursor.execute("""
            SELECT source_unique_id, COUNT(*) as count
            FROM item_variants 
            WHERE source_unique_id IS NOT NULL
            GROUP BY source_unique_id 
            HAVING count > 1 
            ORDER BY count DESC 
            LIMIT 10
        """)
        variant_dupes = cursor.fetchall()
        
        # Also check for items that might have the same name+category combination (potential logic issues)
        cursor.execute("""
            SELECT name, category, COUNT(*) as count 
            FROM items 
            GROUP BY name, category, internal_group_id
            HAVING count > 1 
            ORDER BY count DESC 
            LIMIT 5
        """)
        logic_dupes = cursor.fetchall()
        
        # Get total counts
        cursor.execute("SELECT COUNT(*) FROM items")
        total_items = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM villagers")
        total_villagers = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM item_variants")
        total_variants = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"\nDatabase Status:")
        print(f"   Total Items: {total_items}")
        print(f"   Total Villagers: {total_villagers}")
        print(f"   Total Variants: {total_variants}")
        
        print(f"\nDuplicate Check Results:")
        
        if item_dupes:
            print(f"   Found {len(item_dupes)} duplicate items by source_unique_id:")
            for source_id, count, names in item_dupes:
                print(f"      - Source ID '{source_id}': {count} copies ({names})")
        else:
            print("   No duplicate items found")
            
        if villager_dupes:
            print(f"   Found {len(villager_dupes)} duplicate villagers by source_unique_id:")
            for source_id, count, names in villager_dupes:
                print(f"      - Source ID '{source_id}': {count} copies ({names})")
        else:
            print("   No duplicate villagers found")
            
        if variant_dupes:
            print(f"   Found {len(variant_dupes)} duplicate variants by source_unique_id:")
            for source_id, count in variant_dupes:
                print(f"      - Source ID '{source_id}': {count} copies")
        else:
            print("   No duplicate variants found")
            
        if logic_dupes:
            print(f"   Found {len(logic_dupes)} potential import logic issues:")
            for name, category, count in logic_dupes:
                print(f"      - '{name}' ({category}): {count} copies")
        else:
            print("   No import logic issues detected")
            
        total_dupes = len(item_dupes) + len(villager_dupes) + len(variant_dupes) + len(logic_dupes)
        if total_dupes == 0:
            print(f"\nDatabase is clean - no duplicates detected!")
        else:
            print(f"\nFound {total_dupes} types of potential issues - may need investigation")
        
    except Exception as e:
        print(f"Error checking duplicates: {e}")

def run_full_test():
    """Run the complete test sequence"""
    print("Running Full Import Test Sequence")
    print("=" * 60)
    
    print("\n1️. Checking current database state...")
    check_for_duplicates()
    
    print("\n2️. Deleting some data for testing...")
    delete_random_data()
    
    print("\n3️. Setting up mock sheet update scenario...")
    mock_sheet_update()
    
    print("\n4️. Test complete! Next steps:")
    print("   Restart your bot or run: python test_update_logic.py")
    print("   After import, run: python mock_sheet_update.py --check")
    print("   This will verify the import worked and no duplicates were created")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        check_for_duplicates()
    elif len(sys.argv) > 1 and sys.argv[1] == "--delete":
        delete_random_data()
    elif len(sys.argv) > 1 and sys.argv[1] == "--full-test":
        run_full_test()
    else:
        # Default behavior - just mock the update
        mock_sheet_update()
        print("\nAdditional options:")
        print("   python mock_sheet_update.py --check      # Check for duplicates")
        print("   python mock_sheet_update.py --delete     # Delete random data") 
        print("   python mock_sheet_update.py --full-test  # Run complete test")