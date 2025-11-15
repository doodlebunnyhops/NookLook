#!/usr/bin/env python3
"""
Initialize the ACNH database with schema and some test data
"""
import asyncio
import sys
import os

# Add the bot directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from bot.repos.database import Database

async def init_database():
    """Initialize the database with schema"""
    print("🗄️  Initializing ACNH Database")
    print("=" * 40)
    
    # Create database instance with proper path (same as repository uses)
    db_path = "data/acnh_cache.db"
    db = Database(db_path)
    
    try:
        # Initialize the database from schema
        schema_path = "schemas/items.sql"
        await db.init_from_schema(schema_path)
        print("✅ Database initialized successfully!")
        
        # Check if tables were created
        tables = await db.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
        
        print(f"\n📋 Created {len(tables)} tables:")
        for table in tables:
            print(f"   - {table['name']}")
        
        # Add some test data
        print("\n📝 Adding test data...")
        test_items = [
            ("Wooden Chair", "wooden-chair", "Housewares", "Simple", 100, 1, 1),
            ("Iron Chair", "iron-chair", "Housewares", None, 200, 1, 1),
            ("Wooden Table", "wooden-table", "Housewares", "Simple", 300, 2, 1),
            ("Wooden Bed", "wooden-bed", "Housewares", "Simple", 500, 2, 2),
            ("Chair", "chair", "Housewares", None, 150, 1, 1)
        ]
        
        for item in test_items:
            await db.execute_command("""
                INSERT OR IGNORE INTO acnh_items 
                (name, name_normalized, category, item_series, sell_price, grid_width, grid_length)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, item)
        
        # Check how many items we have
        result = await db.execute_query("SELECT COUNT(*) as count FROM acnh_items")
        count = result[0]['count']
        print(f"✅ Added {count} test items to database")
        
        print("\n🎉 Database setup complete! You can now test the bot commands.")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(init_database())