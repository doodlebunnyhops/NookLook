"""Setup translations schema in the database"""

import asyncio
import pathlib
import sys

# Add project root to path
project_root = pathlib.Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from bot.repos.database import Database


async def setup_translations_schema():
    """Apply the translations schema to the database"""
    db_path = project_root / "data" / "nooklook.db"
    schema_path = project_root / "schemas" / "translations_schema.sql"
    
    print(f"Database: {db_path}")
    print(f"Schema: {schema_path}")
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        print("Run the main import first to create the database.")
        return
    
    if not schema_path.exists():
        print(f"Error: Schema file not found at {schema_path}")
        return
    
    db = Database(str(db_path))
    
    # Use ensure_schema which handles CREATE IF NOT EXISTS
    await db.ensure_schema(str(schema_path))
    
    # Verify tables were created
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('user_settings', 'item_translations')"
    tables = await db.execute_query(query)
    
    table_names = [t['name'] for t in tables]
    print(f"\nCreated tables: {', '.join(table_names)}")
    
    if 'user_settings' in table_names:
        print("✅ user_settings table ready")
    else:
        print("❌ user_settings table not found")
    
    if 'item_translations' in table_names:
        print("✅ item_translations table ready")
    else:
        print("❌ item_translations table not found")
    
    await db.close()
    print("\nSchema setup complete!")


if __name__ == '__main__':
    asyncio.run(setup_translations_schema())
