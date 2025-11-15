#!/usr/bin/env python3
"""
Enhanced CSV Importer that handles color variations
Imports each color variant as a separate item with color in the name
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

class VariantAwareCSVImporter:
    """CSV importer that handles color variations properly"""
    
    def __init__(self, db_path: str = "data/acnh_cache.db"):
        self.db = Database(db_path)
        self.import_stats = {
            "processed": 0,
            "imported": 0,
            "skipped": 0,
            "errors": 0
        }
    
    async def import_csv_file(self, file_path: str, category: str):
        """Import a single CSV file with variant handling"""
        print(f"📄 Importing {file_path} as category '{category}'")
        
        if not pathlib.Path(file_path).exists():
            print(f"❌ File not found: {file_path}")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                rows = list(csv_reader)
                
                print(f"📊 Found {len(rows)} rows to process")
                
                for i, row in enumerate(rows, 1):
                    await self._process_row(row, category)
                    
                    if i % 100 == 0:
                        print(f"   Processed {i}/{len(rows)} rows...")
                
                self._print_stats()
                
        except Exception as e:
            print(f"❌ Error importing {file_path}: {e}")
            import traceback
            traceback.print_exc()
    
    async def _process_row(self, row: Dict[str, str], category: str):
        """Process a single CSV row with variant awareness"""
        self.import_stats["processed"] += 1
        
        try:
            # Get base name and color
            base_name = self._get_value(row, ['Name', 'Item', 'name', 'item'])
            color = self._get_value(row, ['Variation', 'Variant', 'Color', 'variant', 'color'])
            
            if not base_name:
                self.import_stats["skipped"] += 1
                return
            
            # Create full name with color if present
            if color and color.upper() not in ['NA', 'N/A', '']:
                full_name = f"{base_name}"
                name_normalized = f"{base_name.strip().lower()} ({color.strip().lower()})"
            else:
                full_name = base_name
                name_normalized = base_name.strip().lower()
            
            # Check if this specific variant exists
            exists = await self._item_exists(name_normalized)
            if exists:
                self.import_stats["skipped"] += 1
                return
            
            # Map and save item
            item_data = await self._map_csv_to_db(row, full_name, name_normalized, category, color)
            await self._save_item(item_data)
            self.import_stats["imported"] += 1
            
        except Exception as e:
            self.import_stats["errors"] += 1
            print(f"⚠️  Error processing row: {e}")
    
    async def _map_csv_to_db(self, row: Dict[str, str], name: str, name_normalized: str, category: str, color: Optional[str]) -> Dict[str, Any]:
        """Map CSV row to database fields"""
        # Handle size field which is in format "1x1", "2x1", etc.
        size_str = self._get_value(row, ['Size'])
        grid_width, grid_length = self._parse_size(size_str)
        
        # Handle image filename - check inventory first, then storage, then fallback to regular filename
        filename, image_url = self._extract_filename_and_url(row)
        
        return {
            "name": name,
            "name_normalized": name_normalized,
            "category": category,
            "color_variant": color,  # Store original color
            "item_series": self._get_value(row, ['Series', 'series', 'HHA Series']),
            "item_set": self._get_value(row, ['Set', 'set', 'HHA Set']),
            "hha_category": self._get_value(row, ['HHA Category', 'hha_category']),
            "hha_base": self._get_int_value(row, ['HHA Base Points', 'hha_base']),
            "interact": self._get_value(row, ['Interact', 'interact']),
            "tag": self._get_value(row, ['Tag', 'tag']),
            "outdoor": self._get_value(row, ['Outdoor', 'outdoor']),
            "speaker_type": self._get_value(row, ['Speaker Type', 'speaker_type']),
            "lighting_type": self._get_value(row, ['Lighting Type', 'lighting_type']),
            "catalog": self._get_value(row, ['Catalog', 'catalog']),
            "version_added": self._get_value(row, ['Version Added', 'version_added']),
            "unlocked": self._get_value(row, ['Unlocked', 'unlocked']),
            "filename": filename,
            "image_filename": filename,  # Store both for compatibility
            "variant_id": self._get_value(row, ['Variant ID', 'variant_id']),
            "internal_id": self._get_value(row, ['Internal ID', 'internal_id']),
            "unique_entry_id": self._get_value(row, ['Unique Entry ID', 'unique_entry_id']),
            "sell_price": self._get_int_value(row, ['Sell']),
            "grid_width": grid_width,
            "grid_length": grid_length,
            "customizable": self._get_bool_value(row, ['Body Customize', 'Pattern Customize']),
            "custom_kits": self._get_int_value(row, ['Kit Cost']),
            "custom_kit_type": self._get_value(row, ['Kit Type']),
            "notes": self._get_value(row, ['Source Notes']),
            "image_url": image_url,
            "hex_id": None      # Will be populated by hex importer
        }
    
    async def _save_item(self, item_data: Dict[str, Any]):
        """Save item to database with comprehensive data"""
        query = """
            INSERT INTO acnh_items 
            (name, name_normalized, category, color_variant, hex_id, sell_price, hha_base, hha_category,
             grid_width, grid_length, item_series, item_set, tag, customizable, custom_kits, custom_kit_type,
             interact, outdoor, speaker_type, lighting_type, catalog, version_added, unlocked, filename,
             variant_id, internal_id, unique_entry_id, image_filename, image_url, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        await self.db.execute_command(
            query,
            (
                item_data["name"],
                item_data["name_normalized"],
                item_data["category"],
                item_data["color_variant"],
                item_data["hex_id"],
                item_data["sell_price"],
                item_data["hha_base"],
                item_data["hha_category"],
                item_data["grid_width"],
                item_data["grid_length"],
                item_data["item_series"],
                item_data["item_set"],
                item_data["tag"],
                item_data["customizable"],
                item_data["custom_kits"],
                item_data["custom_kit_type"],
                item_data["interact"],
                item_data["outdoor"],
                item_data["speaker_type"],
                item_data["lighting_type"],
                item_data["catalog"],
                item_data["version_added"],
                item_data["unlocked"],
                item_data["filename"],
                item_data["variant_id"],
                item_data["internal_id"],
                item_data["unique_entry_id"],
                item_data["image_filename"],
                item_data["image_url"],
                item_data["notes"]
            )
        )
    
    async def _item_exists(self, name_normalized: str) -> bool:
        """Check if item exists in database"""
        result = await self.db.execute_query(
            "SELECT 1 FROM acnh_items WHERE name_normalized = ?", 
            (name_normalized,)
        )
        return len(result) > 0
    
    def _get_value(self, row: Dict[str, str], possible_keys: List[str]) -> Optional[str]:
        """Get value from row, trying multiple possible column names"""
        for key in possible_keys:
            if key in row and row[key] and row[key].strip():
                value = row[key].strip()
                if value.upper() not in ['NFS', 'NA', 'N/A', '']:
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
    
    def _extract_filename_and_url(self, row: Dict[str, str]) -> tuple[Optional[str], Optional[str]]:
        """Extract filename and generate appropriate URL, trying inventory first, then storage, then regular filename"""
        
        # Try inventory filename first
        inventory_field = self._get_value(row, ['Inventory Filename'])
        if inventory_field:
            filename = self._extract_filename_from_image_formula(inventory_field)
            if filename:
                # Generate MenuIcon URL for inventory items
                image_url = f"https://acnhcdn.com/latest/MenuIcon/{filename.strip()}.png"
                return filename, image_url
        
        # Try storage filename second
        storage_field = self._get_value(row, ['Storage Filename'])
        if storage_field:
            filename = self._extract_filename_from_image_formula(storage_field)
            if filename:
                # Generate FtrIcon URL for storage items
                image_url = f"https://acnhcdn.com/latest/FtrIcon/{filename.strip()}.png"
                return filename, image_url
        
        # Fall back to regular filename field
        regular_filename = self._get_value(row, ['Filename', 'filename'])
        if regular_filename:
            # Use existing logic for regular filenames
            image_url = self._generate_image_url(regular_filename)
            return regular_filename, image_url
        
        return None, None
    
    def _extract_filename_from_image_formula(self, field_value: str) -> Optional[str]:
        """Extract filename from IMAGE() formula like 'IMAGE("https://acnhcdn.com/latest/FtrIcon/SquashOrange.png")'"""
        if not field_value:
            return None
        
        # Handle cases where it's just the filename (already processed)
        if not field_value.startswith('IMAGE('):
            return field_value.strip() if field_value.strip() not in ['', 'NA', 'N/A'] else None
        
        # Extract URL from IMAGE("url") format
        try:
            # Find the URL inside the quotes
            start_quote = field_value.find('"')
            if start_quote == -1:
                return None
            
            end_quote = field_value.find('"', start_quote + 1)
            if end_quote == -1:
                return None
            
            url = field_value[start_quote + 1:end_quote]
            
            # Extract filename from URL (last part before .png)
            if '/' in url:
                filename_with_ext = url.split('/')[-1]  # Get "SquashOrange.png"
                if '.' in filename_with_ext:
                    filename = filename_with_ext.rsplit('.', 1)[0]  # Remove ".png" to get "SquashOrange"
                    return filename.strip() if filename.strip() else None
            
        except Exception:
            pass
        
        return None
    
    def _print_stats(self):
        """Print import statistics"""
        print(f"\n📊 Import Statistics:")
        print(f"   Processed: {self.import_stats['processed']}")
        print(f"   Imported: {self.import_stats['imported']}")
        print(f"   Skipped: {self.import_stats['skipped']}")
        print(f"   Errors: {self.import_stats['errors']}")

async def main():
    """Main function - import collectables with enhanced filename handling"""
    # Initialize database first
    db = Database("data/acnh_cache.db")
    await db.init_from_schema("schemas/items.sql")
    
    importer = VariantAwareCSVImporter()
    await importer.import_csv_file("data/csv/collectable.csv", "Collectables")

if __name__ == "__main__":
    asyncio.run(main())