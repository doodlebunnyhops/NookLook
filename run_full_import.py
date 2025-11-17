#!/usr/bin/env python3
"""
Full ACNH Dataset Import from Google Sheets API
Imports all available datasets from Google Sheets into the database
"""
from import_all_datasets import ACNHDatasetImporter

def main():
    """Run the full import process"""
    print("🚀 Starting full ACNH dataset import from Google Sheets API")
    print("=" * 70)
    
    try:
        # Initialize importer
        importer = ACNHDatasetImporter()
        print("✅ Importer initialized successfully")
        
        # Initialize database
        print("\n📊 Initializing database...")
        importer.init_database()
        
        # Import all datasets
        print("\n📥 Starting dataset import...")
        importer.import_all_datasets()
        
        print("\n" + "=" * 70)
        print("🎉 Full import completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())