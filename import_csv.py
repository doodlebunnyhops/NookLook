#!/usr/bin/env python3
"""
CSV Data Importer for ACNH Items
Imports data from the community spreadsheet CSV files into our database
"""
import asyncio
import csv
import pathlib
import sys
import os
from typing import List, Dict, Any, Optional

# Add the bot directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from bot.repos.database import Database

class ACNHCSVImporter:
    """Imports ACNH item data from CSV files"""
    
    def __init__(self, db_path: str = "data/acnh_cache.db"):
        self.db = Database(db_path)
        self.import_stats = {
            "processed": 0,
            "imported": 0,
            "skipped": 0,
            "errors": 0
        }
    
    async def import_csv_file(self, csv_path: str, item_category: str = "Housewares"):
        """Import a single CSV file"""
        print(f"📄 Importing {csv_path} as category '{item_category}'")
        
        if not pathlib.Path(csv_path).exists():
            print(f"❌ File not found: {csv_path}")
            return
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                # Try to detect if file has a BOM
                content = file.read()
                if content.startswith('\ufeff'):
                    content = content[1:]  # Remove BOM
                
                # Parse CSV
                csv_reader = csv.DictReader(content.splitlines())
                rows = list(csv_reader)
                
                print(f"📊 Found {len(rows)} rows to process")
                
                for i, row in enumerate(rows):
                    await self._process_row(row, item_category)
                    
                    if (i + 1) % 100 == 0:
                        print(f"   Processed {i + 1}/{len(rows)} rows...")
                
                self._print_stats()
                
        except Exception as e:
            print(f"❌ Error importing {csv_path}: {e}")
            import traceback
            traceback.print_exc()
    
    async def _process_row(self, row: Dict[str, str], category: str):
        """Process a single CSV row"""
        self.import_stats["processed"] += 1
        
        try:
            # Extract item name (try common column names)
            name = self._get_value(row, ['Name', 'name', 'Item Name', 'Item'])
            if not name:
                self.import_stats["skipped"] += 1
                return
            
            # Normalize name
            name_normalized = name.strip().lower()
            
            # Check if item already exists
            exists = await self._item_exists(name_normalized)
            if exists:
                self.import_stats["skipped"] += 1
                return
            
            # Map CSV columns to database fields
            item_data = await self._map_csv_to_db(row, name, name_normalized, category)
            
            # Insert item
            await self._insert_item(item_data)
            self.import_stats["imported"] += 1
            
        except Exception as e:
            self.import_stats["errors"] += 1
            print(f"⚠️  Error processing row: {e}")
            print(f"   Row data: {dict(list(row.items())[:3])}...")  # Show first 3 fields
    
    async def _map_csv_to_db(self, row: Dict[str, str], name: str, name_normalized: str, category: str) -> Dict[str, Any]:
        """Map CSV row to database fields"""
        # Handle size field which is in format "1x1", "2x1", etc.
        size_str = self._get_value(row, ['Size'])
        grid_width, grid_length = self._parse_size(size_str)
        
        # Handle image filename and generate URL
        filename = self._get_value(row, ['Filename'])
        image_url = self._generate_image_url(filename) if filename else None
        
        return {
            "name": name,
            "name_normalized": name_normalized,
            "category": category,
            "item_series": self._get_value(row, ['HHA Series']),
            "item_set": self._get_value(row, ['HHA Set']),
            "hha_category": self._get_value(row, ['HHA Category']),
            "hha_base": self._get_int_value(row, ['HHA Base Points']),
            "tag": self._get_value(row, ['Tag']),
            "sell_price": self._get_int_value(row, ['Sell']),
            "grid_width": grid_width,
            "grid_length": grid_length,
            "customizable": self._get_bool_value(row, ['Body Customize', 'Pattern Customize']),
            "custom_kits": self._get_int_value(row, ['Kit Cost']),
            "custom_kit_type": self._get_value(row, ['Kit Type']),
            "version_added": self._get_value(row, ['Version Added']),
            "notes": self._get_value(row, ['Source Notes']),
            "image_filename": filename,
            "image_url": image_url,
        }
    
    async def _insert_item(self, item_data: Dict[str, Any]):
        """Insert item into database"""
        query = """
            INSERT OR IGNORE INTO acnh_items 
            (name, name_normalized, category, item_series, item_set, hha_category, 
             hha_base, tag, sell_price, grid_width, grid_length, customizable, 
             custom_kits, custom_kit_type, version_added, notes, image_filename, image_url, hex_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            item_data["name"],
            item_data["name_normalized"],
            item_data["category"],
            item_data["item_series"],
            item_data["item_set"],
            item_data["hha_category"],
            item_data["hha_base"],
            item_data["tag"],
            item_data["sell_price"],
            item_data["grid_width"],
            item_data["grid_length"],
            item_data["customizable"],
            item_data["custom_kits"],
            item_data["custom_kit_type"],
            item_data["version_added"],
            item_data["notes"],
            item_data["image_filename"],
            item_data["image_url"],
            item_data.get("hex_id")
        )
        
        await self.db.execute_command(query, params)
    
    async def _item_exists(self, name_normalized: str) -> bool:
        """Check if item already exists in database"""
        result = await self.db.execute_query_one(
            "SELECT 1 FROM acnh_items WHERE name_normalized = ?", 
            (name_normalized,)
        )
        return result is not None
    
    def _get_value(self, row: Dict[str, str], possible_keys: List[str]) -> Optional[str]:
        """Get value from row, trying multiple possible column names"""
        for key in possible_keys:
            if key in row and row[key] and row[key].strip():
                value = row[key].strip()
                if value.upper() in ['NFS', 'NA', 'N/A', '']:
                    return None
                return value
        return None
    
    def _get_int_value(self, row: Dict[str, str], possible_keys: List[str], default: Optional[int] = None) -> Optional[int]:
        """Get integer value from row"""
        value = self._get_value(row, possible_keys)
        if value is None:
            return default
        
        try:
            # Remove commas and other non-numeric characters
            numeric_value = ''.join(c for c in value if c.isdigit() or c == '-')
            if numeric_value:
                return int(numeric_value)
        except ValueError:
            pass
        
        return default
    
    def _get_bool_value(self, row: Dict[str, str], possible_keys: List[str]) -> bool:
        """Get boolean value from row"""
        values = []
        for key in possible_keys:
            value = self._get_value(row, [key])
            if value:
                values.append(value)
        
        if not values:
            return False
        
        # Check if any of the values indicate customization is possible
        for value in values:
            if value.lower() in ['yes', 'true', '1', 'y']:
                return True
        
        return False
    
    def _parse_size(self, size_str: Optional[str]) -> tuple[int, int]:
        """Parse size string like '1x1', '2x1' into width and length"""
        if not size_str:
            return (1, 1)
        
        try:
            parts = size_str.lower().split('x')
            if len(parts) == 2:
                width = int(parts[0].strip())
                length = int(parts[1].strip())
                return (width, length)
        except (ValueError, IndexError):
            pass
        
        return (1, 1)
    
    def _generate_image_url(self, filename: Optional[str]) -> Optional[str]:
        """Generate image URL from filename using ACNH CDN pattern"""
        if not filename or filename.strip() in ['', 'NA']:
            return None
        
        # Use the ACNH CDN pattern discovered from the Google Sheet
        return f"https://acnhcdn.com/latest/FtrIcon/{filename.strip()}.png"
    
    def _print_stats(self):
        """Print import statistics"""
        print("\n📊 Import Statistics:")
        print(f"   Processed: {self.import_stats['processed']}")
        print(f"   Imported: {self.import_stats['imported']}")
        print(f"   Skipped: {self.import_stats['skipped']}")
        print(f"   Errors: {self.import_stats['errors']}")
    
    async def import_multiple_files(self, file_mappings: Dict[str, str]):
        """Import multiple CSV files with their categories"""
        print("🚀 Starting bulk CSV import")
        print("=" * 50)
        
        # Initialize database first
        await self.db.init_from_schema("schemas/items.sql")
        print("✅ Database initialized")
        
        total_stats = {"processed": 0, "imported": 0, "skipped": 0, "errors": 0}
        
        for csv_path, category in file_mappings.items():
            print(f"\n📂 Processing {pathlib.Path(csv_path).name}")
            await self.import_csv_file(csv_path, category)
            
            # Add to total stats
            for key in total_stats:
                total_stats[key] += self.import_stats[key]
            
            # Reset stats for next file
            self.import_stats = {"processed": 0, "imported": 0, "skipped": 0, "errors": 0}
        
        print("\n🎉 Bulk import complete!")
        print("=" * 50)
        print("📊 Total Statistics:")
        for key, value in total_stats.items():
            print(f"   {key.title()}: {value}")
        
        # Show final database stats
        result = await self.db.execute_query("SELECT COUNT(*) as count FROM acnh_items")
        total_items = result[0]['count']
        print(f"\n📦 Total items in database: {total_items}")

async def main():
    """Main function - example usage"""
    importer = ACNHCSVImporter()
    
    # Define CSV files and their categories
    csv_files = {
        # Import the Bottoms CSV you provided (clothing data)
        "data/csv/bottoms.csv": "Bottoms",
    }
    
    if not csv_files:
        print("📝 No CSV files configured for import.")
        print("\nTo use this importer:")
        print("1. Download CSV files from the ACNH spreadsheet")
        print("2. Place them in the data/csv/ directory")
        print("3. Update the csv_files dictionary in this script")
        print("4. Run the script again")
        print("\nExample CSV files to download:")
        print("- Housewares tab → housewares.csv")
        print("- Miscellaneous tab → miscellaneous.csv")
        print("- Wall-mounted tab → wall_mounted.csv")
        print("- etc.")
        return
    
    await importer.import_multiple_files(csv_files)

if __name__ == "__main__":
    asyncio.run(main())