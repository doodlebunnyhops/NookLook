#!/usr/bin/env python3
"""
Force Import - Always imports regardless of modification time
Use this when you want to force a fresh import of all data
"""
try:
    from .import_all_datasets import ACNHDatasetImporter
except ImportError:
    from import_all_datasets import ACNHDatasetImporter

def main():
    """Force import all data regardless of modification timestamps"""
    print("Starting FORCED ACNH dataset import from Google Sheets API")
    print("WARNING: This will import all data regardless of modification time")
    print("=" * 70)
    
    try:
        # Initialize importer
        importer = ACNHDatasetImporter()
        print("Importer initialized successfully")
        
        # Initialize database
        print("\nInitializing database...")
        importer.init_database()
        
        # Force import all datasets (bypasses smart checking)
        print("\nStarting forced dataset import...")
        importer.import_all_datasets()
        
        print("\n" + "=" * 70)
        print("Forced import completed successfully!")
        
    except Exception as e:
        print(f"\nImport failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())