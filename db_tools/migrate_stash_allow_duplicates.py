"""Migration script to allow duplicate items in stashes.

This migration removes the UNIQUE constraint on stash_items table
to allow users to add the same item multiple times (for TI orders).

Run this once to update existing databases.
"""

import sqlite3
import pathlib
import shutil
from datetime import datetime

def migrate_database(db_path: str = None):
    """Remove the UNIQUE constraint from stash_items table."""
    
    if db_path is None:
        # Default to the project data directory
        script_dir = pathlib.Path(__file__).parent
        project_root = script_dir.parent
        db_path = str(project_root / "data" / "nooklook.db")
    
    db_file = pathlib.Path(db_path)
    
    if not db_file.exists():
        print(f"Database not found at {db_path}")
        return False
    
    # Create backup first
    backup_dir = db_file.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"nooklook_before_stash_migration_{timestamp}.db"
    
    print(f"Creating backup at {backup_path}...")
    shutil.copy2(db_path, backup_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Starting migration to allow duplicate stash items...")
        
        # Check if the old table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='stash_items'
        """)
        
        if not cursor.fetchone():
            print("stash_items table does not exist - nothing to migrate")
            return True
        
        # SQLite doesn't support dropping constraints directly
        # We need to recreate the table without the constraint
        
        # Step 1: Create new table without the UNIQUE constraint
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stash_items_new (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                stash_id            INTEGER NOT NULL REFERENCES user_stashes(id) ON DELETE CASCADE,
                ref_table           TEXT NOT NULL,
                ref_id              INTEGER NOT NULL,
                variant_id          INTEGER,
                display_name        TEXT NOT NULL,
                added_at            DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Step 2: Copy data from old table
        cursor.execute("""
            INSERT INTO stash_items_new (id, stash_id, ref_table, ref_id, variant_id, display_name, added_at)
            SELECT id, stash_id, ref_table, ref_id, variant_id, display_name, added_at
            FROM stash_items
        """)
        
        # Step 3: Drop old table
        cursor.execute("DROP TABLE stash_items")
        
        # Step 4: Rename new table to original name
        cursor.execute("ALTER TABLE stash_items_new RENAME TO stash_items")
        
        # Step 5: Recreate the index
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_stash_items_stash_id 
            ON stash_items(stash_id)
        """)
        
        conn.commit()
        print("✅ Migration completed successfully!")
        print("   - Removed UNIQUE constraint from stash_items")
        print("   - Users can now add duplicate items for TI orders")
        print(f"   - Backup saved at: {backup_path}")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Migration failed: {e}")
        print(f"   Database restored from backup if needed: {backup_path}")
        return False
        
    finally:
        conn.close()


if __name__ == "__main__":
    import sys
    
    db_path = sys.argv[1] if len(sys.argv) > 1 else None
    success = migrate_database(db_path)
    sys.exit(0 if success else 1)
