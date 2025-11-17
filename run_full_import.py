#!/usr/bin/env python3
"""
Full ACNH Dataset Import from Google Sheets API
Imports all available datasets from Google Sheets into the database
"""
from import_all_datasets import ACNHDatasetImporter

def main():
    """Run the smart import process (only imports if data changed)"""
    print("🚀 Starting smart ACNH dataset import from Google Sheets API")
    print("=" * 70)
    
    try:
        # Initialize importer
        importer = ACNHDatasetImporter()
        print("✅ Importer initialized successfully")
        
        # Initialize database
        print("\nInitializing database...")
        importer.init_database()
        
        # Smart import (only if data changed)
        print("\nStarting smart dataset import...")
        import_performed = importer.import_all_datasets_smart()
        
        if import_performed:
            print("\n" + "=" * 70)
            print("Smart import completed successfully!")
        else:
            print("\n" + "=" * 70)
            print("No import needed - data is already up-to-date!")
        
    except Exception as e:
        print(f"\nImport failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())