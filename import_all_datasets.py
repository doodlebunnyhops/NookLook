#!/usr/bin/env python3
"""
Complete ACNH Dataset Importer
Imports all ACNH datasets from Google Sheets API into the nooklook.db SQLite database using the nooklook_schema.sql structure
"""
import sqlite3
import csv
import pathlib
import sys
import os
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Tuple

class ACNHDatasetImporter:
    """Imports all ACNH datasets from Google Sheets API into the database"""
    
    def __init__(self, db_path: str = "nooklook.db", datasets_dir: str = "datasets"):
        # Load environment variables
        load_dotenv()
        
        self.db_path = db_path
        self.datasets_dir = pathlib.Path(datasets_dir)
        self.import_stats = {
            "processed": 0,
            "imported": 0,
            "skipped": 0,
            "errors": 0
        }
        
        # Google Sheets API configuration
        self.google_sheet_url = os.getenv('GOOGLE_SHEET')
        self.gcp_api_key = os.getenv('GCP_API_KEY')
        
        if not self.google_sheet_url or not self.gcp_api_key:
            raise ValueError("GOOGLE_SHEET and GCP_API_KEY must be set in environment variables")
            
        # Extract spreadsheet ID from URL
        self.spreadsheet_id = self._extract_spreadsheet_id(self.google_sheet_url)
        
        # Mapping from CSV filenames to Google Sheet titles
        self.sheet_mappings = {
            'accessories.csv': 'Accessories',
            'bags.csv': 'Bags', 
            'bottoms.csv': 'Bottoms',
            'ceiling-decor.csv': 'Ceiling Decor',
            'clothing-other.csv': 'Clothing Other',
            'dress-up.csv': 'Dress-Up',
            'fencing.csv': 'Fencing',
            'floors.csv': 'Floors',
            'gyroids.csv': 'Gyroids',
            'headwear.csv': 'Headwear',
            'housewares.csv': 'Housewares',
            'interior-structures.csv': 'Interior Structures',
            'miscellaneous.csv': 'Miscellaneous',
            'music.csv': 'Music',
            'other.csv': 'Other',
            'photos.csv': 'Photos',
            'posters.csv': 'Posters',
            'rugs.csv': 'Rugs',
            'shoes.csv': 'Shoes',
            'socks.csv': 'Socks',
            'tools-goods.csv': 'Tools/Goods',
            'tops.csv': 'Tops',
            'umbrellas.csv': 'Umbrellas',
            'wall-mounted.csv': 'Wall-mounted',
            'wallpaper.csv': 'Wallpaper',
            'fish.csv': 'Fish',
            'insects.csv': 'Insects', 
            'sea-creatures.csv': 'Sea Creatures',
            'fossils.csv': 'Fossils',
            'artwork.csv': 'Artwork',
            'villagers.csv': 'Villagers',
            'recipes.csv': 'Recipes',
        }
        
    def init_database(self, schema_path: str = "schemas/nooklook_schema.sql"):
        """Initialize database from schema file"""
        schema_file = pathlib.Path(schema_path)
        
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
            
        print(f"Initializing database from schema: {schema_path}")
        
        # Read and execute schema
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Execute the entire script at once - SQLite can handle multiple statements
        try:
            cursor.executescript(schema_sql)
            print("Schema executed successfully")
        except sqlite3.Error as e:
            print(f"Error executing schema: {e}")
            # If executescript fails, try statement by statement
            lines = []
            for line in schema_sql.split('\n'):
                line = line.strip()
                if line and not line.startswith('--'):
                    lines.append(line)
            
            clean_sql = ' '.join(lines)
            statements = [stmt.strip() for stmt in clean_sql.split(';') if stmt.strip()]
            
            for statement in statements:
                try:
                    cursor.execute(statement)
                    print(f"Executed: {statement[:50]}...")
                except sqlite3.Error as e:
                    print(f"Warning executing schema statement: {e}")
                    print(f"   Statement: {statement[:100]}...")
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")

    def import_all_datasets(self):
        """Import all available datasets"""
        print("Starting complete dataset import")
        print("=" * 60)
        
        # Define dataset mapping to their respective import methods
        dataset_mappings = {
            # Items (go to items + item_variants tables)
            'accessories.csv': ('items', 'accessories'),
            'bags.csv': ('items', 'bags'),
            'bottoms.csv': ('items', 'bottoms'),
            'ceiling-decor.csv': ('items', 'ceiling-decor'),
            'clothing-other.csv': ('items', 'clothing-other'),
            'dress-up.csv': ('items', 'dress-up'),
            'fencing.csv': ('items', 'fencing'),
            'floors.csv': ('items', 'floors'),
            'gyroids.csv': ('items', 'gyroids'),
            'headwear.csv': ('items', 'headwear'),
            'housewares.csv': ('items', 'housewares'),
            'interior-structures.csv': ('items', 'interior-structures'),
            'miscellaneous.csv': ('items', 'miscellaneous'),
            'music.csv': ('items', 'music'),
            'other.csv': ('items', 'other'),
            'photos.csv': ('items', 'photos'),
            'posters.csv': ('items', 'posters'),
            'rugs.csv': ('items', 'rugs'),
            'shoes.csv': ('items', 'shoes'),
            'socks.csv': ('items', 'socks'),
            'tools-goods.csv': ('items', 'tools-goods'),
            'tops.csv': ('items', 'tops'),
            'umbrellas.csv': ('items', 'umbrellas'),
            'wall-mounted.csv': ('items', 'wall-mounted'),
            'wallpaper.csv': ('items', 'wallpaper'),
            
            # Special tables
            'fish.csv': ('critters', 'fish'),
            'insects.csv': ('critters', 'insects'),
            'sea-creatures.csv': ('critters', 'sea-creatures'),
            'fossils.csv': ('fossils', None),
            'artwork.csv': ('artwork', None),
            'villagers.csv': ('villagers', None),
            'recipes.csv': ('recipes', None),
        }
        
        for filename, (table_type, category) in dataset_mappings.items():
            sheet_title = self.sheet_mappings.get(filename)
            if sheet_title:
                print(f"\nProcessing {filename} from sheet '{sheet_title}'")
                try:
                    # Fetch data from Google Sheets API
                    rows = self._fetch_sheet_data(sheet_title)
                    if not rows:
                        print(f"   Warning: No data found for sheet '{sheet_title}'")
                        continue
                        
                    if table_type == 'items':
                        self._import_items_dataset_from_rows(rows, category)
                    elif table_type == 'critters':
                        self._import_critters_dataset_from_rows(rows, category)
                    elif table_type == 'fossils':
                        self._import_fossils_dataset_from_rows(rows)
                    elif table_type == 'artwork':
                        self._import_artwork_dataset_from_rows(rows)
                    elif table_type == 'villagers':
                        self._import_villagers_dataset_from_rows(rows)
                    elif table_type == 'recipes':
                        self._import_recipes_dataset_from_rows(rows)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    self.import_stats["errors"] += 1
            else:
                print(f"Sheet mapping not found for: {filename}")
        
        # Populate search index and museum index
        self._populate_search_index()
        self._populate_museum_index()
        
        self._print_final_stats()

    def _extract_spreadsheet_id(self, url: str) -> str:
        """Extract spreadsheet ID from Google Sheets URL"""
        if '/spreadsheets/' in url:
            # Handle both regular URLs and API URLs
            if '/spreadsheets/d/' in url:
                return url.split('/spreadsheets/d/')[1].split('/')[0]
            else:
                # API URL format: https://sheets.googleapis.com/v4/spreadsheets/{id}
                return url.split('/spreadsheets/')[1].split('/')[0]
        raise ValueError(f"Invalid Google Sheets URL: {url}")
    
    def get_sheet_metadata(self):
        """Get spreadsheet metadata - unfortunately Sheets API doesn't provide last updated time"""
        print("Fetching spreadsheet metadata...")
        
        # Google Sheets API doesn't include modification timestamps in spreadsheet metadata
        # Only Drive API has modifiedTime field
        api_url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}?key={self.gcp_api_key}&fields=properties.title,properties.locale,properties.timeZone"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            
            data = response.json()
            properties = data.get('properties', {})
            
            metadata = {
                'title': properties.get('title', 'Unknown'),
                'locale': properties.get('locale', 'Unknown'),
                'timezone': properties.get('timeZone', 'Unknown'),
                'spreadsheet_id': self.spreadsheet_id
            }
            
            print(f"   Title: {metadata['title']}")
            print(f"   Locale: {metadata['locale']}")  
            print(f"   Timezone: {metadata['timezone']}")
            print(f"   Last modified time not available via Sheets API")
            print(f"   Use Drive API for modification timestamps")
            
            return metadata
            
        except requests.RequestException as e:
            print(f"   Error fetching metadata: {e}")
            return None
    
    def check_sheet_last_modified(self):
        """
        Check when the sheet was last modified using Drive API
        Note: Requires Google Drive API to be enabled in Google Cloud Console
        """
        print("Checking sheet last modified time...")
        
        # Drive API endpoint to get file modification time
        drive_url = f"https://www.googleapis.com/drive/v3/files/{self.spreadsheet_id}?key={self.gcp_api_key}&fields=modifiedTime,name,version"
        
        try:
            response = requests.get(drive_url)
            response.raise_for_status()
            
            data = response.json()
            
            from datetime import datetime
            modified_time = data.get('modifiedTime')
            if modified_time:
                # Convert ISO 8601 to datetime object
                modified_dt = datetime.fromisoformat(modified_time.replace('Z', '+00:00'))
                
                print(f"   Last Modified: {modified_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                print(f"   Name: {data.get('name', 'Unknown')}")
                print(f"   Version: {data.get('version', 'Unknown')}")
                
                return {
                    'modified_time': modified_time,
                    'modified_datetime': modified_dt,
                    'name': data.get('name'),
                    'version': data.get('version')
                }
            else:
                print("   No modification time available")
                return None
                
        except requests.RequestException as e:
            print(f"   Drive API Error: {e}")
            print(f"   Response content: {getattr(e.response, 'text', 'No response content')}")
            if "Drive API has not been used" in str(e) or "403" in str(e):
                print("   Drive API not enabled. Enable it in Google Cloud Console for modification times.")
                print("   Alternative: Use get_sheet_metadata() for basic info")
            return None
    
    def _get_last_import_time(self):
        """Get the timestamp of the last successful import from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if import_log table exists, create if not
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS import_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    import_timestamp TEXT NOT NULL,
                    sheet_modified_time TEXT NOT NULL,
                    records_imported INTEGER NOT NULL,
                    import_duration_seconds REAL NOT NULL
                )
            """)
            
            # Get the most recent successful import
            cursor.execute("""
                SELECT sheet_modified_time, import_timestamp, records_imported 
                FROM import_log 
                ORDER BY id DESC LIMIT 1
            """)
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                from datetime import datetime
                sheet_time, import_time, records = result
                return {
                    'sheet_modified_time': sheet_time,
                    'import_timestamp': import_time,
                    'records_imported': records,
                    'sheet_modified_datetime': datetime.fromisoformat(sheet_time.replace('Z', '+00:00'))
                }
            else:
                return None
                
        except sqlite3.Error as e:
            print(f"   Error checking last import time: {e}")
            return None
    
    def _log_import_completion(self, sheet_modified_time: str, records_imported: int, duration: float):
        """Log successful import completion with timestamps"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            from datetime import datetime
            import_timestamp = datetime.utcnow().isoformat() + 'Z'
            
            cursor.execute("""
                INSERT INTO import_log (import_timestamp, sheet_modified_time, records_imported, import_duration_seconds)
                VALUES (?, ?, ?, ?)
            """, (import_timestamp, sheet_modified_time, records_imported, duration))
            
            conn.commit()
            conn.close()
            
            print(f"   Import completion logged: {records_imported} records in {duration:.1f}s")
            
        except sqlite3.Error as e:
            print(f"   Error logging import completion: {e}")
    
    def check_if_import_needed(self):
        """
        Check if import is needed by comparing sheet modification time with last import
        Returns: (needs_import: bool, reason: str, sheet_info: dict)
        """
        print("Checking if import is needed...")
        
        # Get current sheet modification time
        current_sheet_info = self.check_sheet_last_modified()
        if not current_sheet_info:
            return True, "Unable to get sheet modification time - importing to be safe", None
        
        # Get last import information
        last_import = self._get_last_import_time()
        if not last_import:
            return True, "No previous import found", current_sheet_info
        
        # Compare modification times
        current_modified = current_sheet_info['modified_datetime']
        last_sheet_modified = last_import['sheet_modified_datetime']
        
        if current_modified > last_sheet_modified:
            time_diff = current_modified - last_sheet_modified
            return True, f"Sheet updated {time_diff} ago", current_sheet_info
        else:
            print(f"   Data is up-to-date (last import: {last_import['import_timestamp']})")
            print(f"   Last import had {last_import['records_imported']} records")
            return False, "Data is already up-to-date", current_sheet_info
    
    def import_all_datasets_smart(self):
        """
        Smart import that only imports if data has changed since last import
        """
        import time
        start_time = time.time()
        
        print("Starting smart ACNH dataset import")
        print("=" * 60)
        
        # Check if import is needed
        needs_import, reason, sheet_info = self.check_if_import_needed()
        
        if not needs_import:
            print(f"Skipping import: {reason}")
            return False
        
        print(f"Import needed: {reason}")
        print("=" * 60)
        
        try:
            # Initialize database schema if needed (in case database doesn't exist or is incomplete)
            if not pathlib.Path(self.db_path).exists():
                print("Database not found, initializing schema...")
                self.init_database()
            else:
                # Check if required tables exist
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Check for key tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('critters', 'fossils', 'artwork')")
                existing_tables = [row[0] for row in cursor.fetchall()]
                conn.close()
                
                missing_tables = set(['critters', 'fossils', 'artwork']) - set(existing_tables)
                if missing_tables:
                    print(f"Missing tables {missing_tables}, reinitializing schema...")
                    self.init_database()
            
            # Perform the actual import with upsert logic
            self.import_all_datasets()
            
            # Log the successful import
            duration = time.time() - start_time
            total_records = self.import_stats["imported"]
            
            if sheet_info and sheet_info.get('modified_time'):
                self._log_import_completion(
                    sheet_info['modified_time'], 
                    total_records, 
                    duration
                )
            
            print(f"\nSmart import completed successfully in {duration:.1f}s!")
            return True
            
        except Exception as e:
            print(f"\nImport failed: {e}")
            raise
    
    def _fetch_sheet_data(self, sheet_title: str) -> List[Dict[str, str]]:
        """Fetch data from a Google Sheet and return as list of dictionaries"""
        print(f"   Fetching data from Google Sheets API for '{sheet_title}'...")
        
        # URL-encode the sheet title to handle special characters like '/'
        # Use replace for forward slashes specifically, as quote() doesn't work for sheet names
        encoded_sheet_title = sheet_title.replace('/', '%2F')
        
        # Construct the API URL with FORMULA render option to get IMAGE formulas
        api_url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}/values/{encoded_sheet_title}?key={self.gcp_api_key}&valueRenderOption=FORMULA"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            
            data = response.json()
            values = data.get('values', [])
            
            if not values:
                return []
            
            # First row contains headers
            headers = values[0]
            rows = []
            
            # Convert to list of dictionaries
            for row_data in values[1:]:
                # Pad row_data to match headers length
                while len(row_data) < len(headers):
                    row_data.append('')
                
                row_dict = {}
                for i, header in enumerate(headers):
                    row_dict[header] = row_data[i] if i < len(row_data) else ''
                
                rows.append(row_dict)
            
            print(f"   Successfully fetched {len(rows)} rows")
            return rows
            
        except requests.exceptions.RequestException as e:
            print(f"   Error fetching data from Google Sheets: {e}")
            return []
        except (KeyError, IndexError) as e:
            print(f"   Error parsing Google Sheets response: {e}")
            return []

    def _import_items_dataset_from_rows(self, rows: List[Dict[str, str]], category: str):
        """Import items dataset from API data - properly group variants under base items"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Group rows by base item (name + internal_group_id should identify the same base item)
        item_groups = {}
        
        for row in rows:
            try:
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                    
                # Use name + internal_group_id as the grouping key
                # Items with same name and internal_group_id are variants of the same item
                internal_group_id = self._get_int_value(row, ['Internal ID'])
                group_key = f"{name}|{internal_group_id}" if internal_group_id else name
                
                if group_key not in item_groups:
                    item_groups[group_key] = []
                item_groups[group_key].append(row)
                
            except Exception as e:
                print(f"   Error grouping row {name if 'name' in locals() else 'Unknown'}: {e}")
                self.import_stats["errors"] += 1
                continue
        
        # Process each item group
        for group_key, group_rows in item_groups.items():
            try:
                self.import_stats["processed"] += len(group_rows)
                
                # Use the first row as the base item data (all rows in group should have same base data)
                base_row = group_rows[0]
                name = self._get_value(base_row, ['Name'])
                internal_group_id = self._get_int_value(base_row, ['Internal ID'])
                
                # Check if base item already exists using name + internal_group_id
                if internal_group_id:
                    cursor.execute("SELECT id FROM items WHERE name = ? AND internal_group_id = ?", (name, internal_group_id))
                else:
                    cursor.execute("SELECT id FROM items WHERE name = ? AND internal_group_id IS NULL", (name,))
                existing_item = cursor.fetchone()
                
                if existing_item:
                    item_id = existing_item[0]
                    # Update existing item with latest data from base row
                    item_data = self._map_item_data(base_row, category, is_base_item=True)
                    # Skip name (index 0) and source_unique_id (index 2) since we're using id in WHERE
                    update_params = item_data[1:2] + item_data[3:]  # category, then skip source_unique_id, then rest
                    cursor.execute("""
                        UPDATE items 
                        SET category = ?, internal_group_id = ?, is_diy = ?, buy_price = ?, sell_price = ?, 
                            hha_base = ?, source = ?, catalog = ?, version_added = ?, tag = ?, style1 = ?, style2 = ?, 
                            label_themes = ?, filename = ?, image_url = ?, extra_json = ?
                        WHERE id = ?
                    """, update_params + (item_id,))
                else:
                    # Insert new base item
                    item_data = self._map_item_data(base_row, category, is_base_item=True)
                    cursor.execute("""
                        INSERT INTO items (name, category, source_unique_id, internal_group_id, is_diy, buy_price, sell_price, 
                                         hha_base, source, catalog, version_added, tag, style1, style2, 
                                         label_themes, filename, image_url, extra_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, item_data)
                    item_id = cursor.lastrowid
                    self.import_stats["imported"] += 1
                
                # Process each variant row for this base item
                for variant_row in group_rows:
                    variant_source_unique_id = self._get_value(variant_row, ['Unique Entry ID'])
                    
                    # Check if this specific variant already exists
                    cursor.execute("SELECT id FROM item_variants WHERE source_unique_id = ?", (variant_source_unique_id,))
                    existing_variant = cursor.fetchone()
                    
                    # Map variant data for this row
                    variant_data = self._map_variant_data(variant_row, item_id)
                    
                    if existing_variant:
                        # Update existing variant
                        cursor.execute("""
                            UPDATE item_variants 
                            SET item_id = ?, variant_id_raw = ?, primary_index = ?, secondary_index = ?, variation_label = ?, 
                                body_title = ?, pattern_label = ?, pattern_title = ?, color1 = ?, color2 = ?, 
                                body_customizable = ?, pattern_customizable = ?, cyrus_customizable = ?, 
                                pattern_options = ?, internal_id = ?, item_hex = ?, ti_primary = ?, ti_secondary = ?, 
                                ti_customize_str = ?, ti_full_hex = ?, image_url = ?, image_url_alt = ?
                            WHERE source_unique_id = ?
                        """, variant_data[0:1] + variant_data[2:] + (variant_source_unique_id,))
                    else:
                        # Insert new variant
                        cursor.execute("""
                            INSERT INTO item_variants (item_id, source_unique_id, variant_id_raw, primary_index, secondary_index, variation_label, 
                                                     body_title, pattern_label, pattern_title, color1, color2, body_customizable, 
                                                     pattern_customizable, cyrus_customizable, pattern_options, internal_id, 
                                                     item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex, 
                                                     image_url, image_url_alt)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, variant_data)
                
            except Exception as e:
                print(f"   Error processing item group {group_key}: {e}")
                self.import_stats["errors"] += 1
                continue
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} variant rows grouped into {len(item_groups)} base items for {category}")

    def _import_items_dataset(self, file_path: pathlib.Path, category: str):
        """Import items dataset (clothing, furniture, etc.)"""
        rows = self._read_csv_file(file_path)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for row in rows:
            try:
                self.import_stats["processed"] += 1
                
                # Extract basic item info
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                
                # Check if item already exists using source unique ID
                source_unique_id = self._get_value(row, ['Unique Entry ID'])
                cursor.execute("SELECT id FROM items WHERE source_unique_id = ?", (source_unique_id,))
                existing_item = cursor.fetchone()
                
                if existing_item:
                    item_id = existing_item[0]
                    # Update existing item with latest data
                    item_data = self._map_item_data(row, category)
                    # Skip source_unique_id (index 2) for UPDATE since it's in WHERE clause
                    update_params = item_data[0:2] + item_data[3:]  # name, category, then skip source_unique_id, then rest
                    cursor.execute("""
                        UPDATE items 
                        SET name = ?, category = ?, internal_group_id = ?, is_diy = ?, buy_price = ?, sell_price = ?, 
                            hha_base = ?, source = ?, catalog = ?, version_added = ?, tag = ?, style1 = ?, style2 = ?, 
                            label_themes = ?, filename = ?, image_url = ?, extra_json = ?
                        WHERE source_unique_id = ?
                    """, update_params + (source_unique_id,))
                else:
                    # Insert base item
                    item_data = self._map_item_data(row, category)
                    cursor.execute("""
                        INSERT INTO items (name, category, source_unique_id, internal_group_id, is_diy, buy_price, sell_price, 
                                         hha_base, source, catalog, version_added, tag, style1, style2, 
                                         label_themes, filename, image_url, extra_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, item_data)
                    item_id = cursor.lastrowid
                    self.import_stats["imported"] += 1
                
                # Insert variant record (always created for TI code calculation)
                variant_data = self._map_variant_data(row, item_id)
                cursor.execute("""
                    INSERT INTO item_variants (item_id, variant_id_raw, primary_index, secondary_index,
                                             variation_label, body_title, pattern_label, pattern_title,
                                             color1, color2, body_customizable, pattern_customizable,
                                             cyrus_customizable, pattern_options, internal_id, item_hex,
                                             ti_primary, ti_secondary, ti_customize_str, ti_full_hex,
                                             image_url, image_url_alt)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, variant_data)
                
            except Exception as e:
                print(f"Error processing item row: {e}")
                self.import_stats["errors"] += 1
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} rows for {category}")

    def _import_critters_dataset_from_rows(self, rows: List[Dict[str, str]], critter_type: str):
        """Import critters dataset from API data"""
        # Map critter type
        kind_map = {
            'fish': 'fish',
            'insects': 'insect', 
            'sea-creatures': 'sea'
        }
        kind = kind_map.get(critter_type, critter_type)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for row in rows:
            try:
                self.import_stats["processed"] += 1
                
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                
                # Check if critter already exists using source_unique_id
                critter_data = self._map_critter_data(row, kind)
                source_unique_id = critter_data[2]  # source_unique_id is at index 2
                
                cursor.execute("SELECT id FROM critters WHERE source_unique_id = ?", (source_unique_id,))
                existing_critter = cursor.fetchone()
                
                if existing_critter:
                    # Update existing critter
                    cursor.execute("""
                        UPDATE critters SET name = ?, kind = ?, internal_id = ?, sell_price = ?, item_hex = ?, 
                                          ti_primary = ?, ti_secondary = ?, ti_customize_str = ?, ti_full_hex = ?, location = ?, 
                                          shadow_size = ?, movement_speed = ?, catch_difficulty = ?, vision = ?, total_catches_to_unlock = ?, 
                                          spawn_rates = ?, nh_jan = ?, nh_feb = ?, nh_mar = ?, nh_apr = ?, nh_may = ?, nh_jun = ?, 
                                          nh_jul = ?, nh_aug = ?, nh_sep = ?, nh_oct = ?, nh_nov = ?, nh_dec = ?, sh_jan = ?, sh_feb = ?, 
                                          sh_mar = ?, sh_apr = ?, sh_may = ?, sh_jun = ?, sh_jul = ?, sh_aug = ?, sh_sep = ?, sh_oct = ?, 
                                          sh_nov = ?, sh_dec = ?, time_of_day = ?, weather = ?, rarity = ?, description = ?, catch_phrase = ?, 
                                          hha_base_points = ?, hha_category = ?, color1 = ?, color2 = ?, size = ?, surface = ?, 
                                          icon_url = ?, critterpedia_url = ?, furniture_url = ?, source = ?, 
                                          version_added = ?, extra_json = ?
                        WHERE source_unique_id = ?
                    """, critter_data[0:2] + critter_data[3:] + (source_unique_id,))
                else:
                    # Insert new critter
                    cursor.execute("""
                        INSERT INTO critters (name, kind, source_unique_id, internal_id, sell_price, item_hex, 
                                            ti_primary, ti_secondary, ti_customize_str, ti_full_hex, location, 
                                            shadow_size, movement_speed, catch_difficulty, vision, total_catches_to_unlock, 
                                            spawn_rates, nh_jan, nh_feb, nh_mar, nh_apr, nh_may, nh_jun, 
                                            nh_jul, nh_aug, nh_sep, nh_oct, nh_nov, nh_dec, sh_jan, sh_feb, 
                                            sh_mar, sh_apr, sh_may, sh_jun, sh_jul, sh_aug, sh_sep, sh_oct, 
                                            sh_nov, sh_dec, time_of_day, weather, rarity, description, catch_phrase, 
                                            hha_base_points, hha_category, color1, color2, size, surface, 
                                            icon_url, critterpedia_url, furniture_url, source, 
                                            version_added, extra_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, critter_data)
                    self.import_stats["imported"] += 1
                
            except Exception as e:
                print(f"   Error processing critter {name if 'name' in locals() else 'Unknown'}: {e}")
                self.import_stats["errors"] += 1
                continue
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} rows for {critter_type}")
    
    def _import_fossils_dataset_from_rows(self, rows: List[Dict[str, str]]):
        """Import fossils dataset from API data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for row in rows:
            try:
                self.import_stats["processed"] += 1
                
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                
                # Check if fossil already exists using source_unique_id
                fossil_data = self._map_fossil_data(row)
                source_unique_id = fossil_data[17]  # source_unique_id is at index 17
                
                cursor.execute("SELECT id FROM fossils WHERE source_unique_id = ?", (source_unique_id,))
                existing_fossil = cursor.fetchone()
                
                if existing_fossil:
                    # Update existing fossil
                    cursor.execute("""
                        UPDATE fossils SET name = ?, image_url = ?, image_url_alt = ?, buy_price = ?, sell_price = ?, fossil_group = ?,
                                          description = ?, hha_base_points = ?, color1 = ?, color2 = ?, size = ?, source = ?, museum = ?,
                                          interact = ?, catalog = ?, filename = ?, internal_id = ?, item_hex = ?,
                                          ti_primary = ?, ti_secondary = ?, ti_customize_str = ?, ti_full_hex = ?, extra_json = ?
                        WHERE source_unique_id = ?
                    """, fossil_data[0:17] + fossil_data[18:] + (source_unique_id,))
                else:
                    # Insert new fossil
                    cursor.execute("""
                        INSERT INTO fossils (name, source_unique_id, image_url, image_url_alt, buy_price, sell_price, fossil_group,
                                           description, hha_base_points, color1, color2, size, source, museum,
                                           interact, catalog, filename, internal_id, item_hex,
                                           ti_primary, ti_secondary, ti_customize_str, ti_full_hex, extra_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, fossil_data[0:1] + (source_unique_id,) + fossil_data[1:17] + fossil_data[18:])
                    self.import_stats["imported"] += 1
                
            except Exception as e:
                print(f"   Error processing fossil {name if 'name' in locals() else 'Unknown'}: {e}")
                self.import_stats["errors"] += 1
                continue
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} rows for fossils")
    
    def _import_artwork_dataset_from_rows(self, rows: List[Dict[str, str]]):
        """Import artwork dataset from API data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for row in rows:
            try:
                self.import_stats["processed"] += 1
                
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                
                # Check if artwork already exists using source_unique_id
                source_unique_id = self._get_value(row, ['Unique Entry ID'])
                cursor.execute("SELECT id FROM artwork WHERE source_unique_id = ?", (source_unique_id,))
                existing_artwork = cursor.fetchone()
                
                # Map artwork data
                artwork_data = self._map_artwork_data(row)
                
                if existing_artwork:
                    # Update existing artwork - skip source_unique_id (index 29) since it's in WHERE clause
                    update_params = artwork_data[0:29] + artwork_data[30:]  # all fields except source_unique_id
                    cursor.execute("""
                        UPDATE artwork SET name = ?, image_url = ?, image_url_alt = ?, genuine = ?, art_category = ?, buy_price = ?, sell_price = ?, 
                                         color1 = ?, color2 = ?, size = ?, real_artwork_title = ?, artist = ?, description = ?, source = ?, source_notes = ?, 
                                         hha_base_points = ?, hha_concept1 = ?, hha_concept2 = ?, hha_series = ?, hha_set = ?, interact = ?, 
                                         tag = ?, speaker_type = ?, lighting_type = ?, catalog = ?, version_added = ?, unlocked = ?, filename = ?, 
                                         internal_id = ?, item_hex = ?, ti_primary = ?, ti_secondary = ?, ti_customize_str = ?, ti_full_hex = ?, extra_json = ?
                        WHERE source_unique_id = ?
                    """, update_params + (source_unique_id,))
                else:
                    # Insert new artwork - rearrange to put source_unique_id second
                    insert_params = artwork_data[0:1] + (source_unique_id,) + artwork_data[1:29] + artwork_data[30:]
                    cursor.execute("""
                        INSERT INTO artwork (name, source_unique_id, image_url, image_url_alt, genuine, art_category, buy_price, sell_price, 
                                           color1, color2, size, real_artwork_title, artist, description, source, source_notes, 
                                           hha_base_points, hha_concept1, hha_concept2, hha_series, hha_set, interact, 
                                           tag, speaker_type, lighting_type, catalog, version_added, unlocked, filename, 
                                           internal_id, item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex, extra_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, insert_params)
                    self.import_stats["imported"] += 1
                
            except Exception as e:
                print(f"   Error processing artwork {name if 'name' in locals() else 'Unknown'}: {e}")
                self.import_stats["errors"] += 1
                continue
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} rows for artwork")
    
    def _import_villagers_dataset_from_rows(self, rows: List[Dict[str, str]]):
        """Import villagers dataset from API data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for row in rows:
            try:
                self.import_stats["processed"] += 1
                
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                
                # Check if villager already exists using source_unique_id
                villager_data = self._map_villager_data(row)
                source_unique_id = villager_data[26]  # source_unique_id is at index 26
                
                cursor.execute("SELECT id FROM villagers WHERE source_unique_id = ?", (source_unique_id,))
                existing_villager = cursor.fetchone()
                
                if existing_villager:
                    # Update existing villager
                    cursor.execute("""
                        UPDATE villagers SET name = ?, species = ?, gender = ?, personality = ?, subtype = ?, hobby = ?, birthday = ?,
                                           catchphrase = ?, favorite_song = ?, favorite_saying = ?, style1 = ?, style2 = ?, 
                                           color1 = ?, color2 = ?, default_clothing = ?, default_umbrella = ?, wallpaper = ?,
                                           flooring = ?, furniture_list = ?, furniture_name_list = ?, diy_workbench = ?,
                                           kitchen_equipment = ?, version_added = ?, name_color = ?, bubble_color = ?,
                                           filename = ?, icon_image = ?, photo_image = ?, house_image = ?
                        WHERE source_unique_id = ?
                    """, villager_data[0:26] + villager_data[27:] + (source_unique_id,))
                else:
                    # Insert new villager
                    cursor.execute("""
                        INSERT INTO villagers (name, species, gender, personality, subtype, hobby, birthday,
                                             catchphrase, favorite_song, favorite_saying, style1, style2, 
                                             color1, color2, default_clothing, default_umbrella, wallpaper,
                                             flooring, furniture_list, furniture_name_list, diy_workbench,
                                             kitchen_equipment, version_added, name_color, bubble_color,
                                             filename, source_unique_id, icon_image, photo_image, house_image)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, villager_data)
                    self.import_stats["imported"] += 1
                
            except Exception as e:
                print(f"   Error processing villager {name if 'name' in locals() else 'Unknown'}: {e}")
                self.import_stats["errors"] += 1
                continue
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} rows for villagers")
    
    def _import_recipes_dataset_from_rows(self, rows: List[Dict[str, str]]):
        """Import recipes dataset from API data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for row in rows:
            try:
                self.import_stats["processed"] += 1
                
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                
                # Check if recipe already exists using source_unique_id
                recipe_data = self._map_recipe_data(row)
                source_unique_id = recipe_data[1]  # source_unique_id is at index 1
                
                cursor.execute("SELECT id FROM recipes WHERE source_unique_id = ?", (source_unique_id,))
                existing_recipe = cursor.fetchone()
                
                if existing_recipe:
                    recipe_id = existing_recipe[0]
                    # Update existing recipe
                    cursor.execute("""
                        UPDATE recipes SET name = ?, source_unique_id = ?, category = ?, source = ?, source_notes = ?,
                                         version_added = ?, buy_price = ?, sell_price = ?, hha_base = ?, item_hex = ?,
                                         ti_primary = ?, ti_secondary = ?, ti_customize_str = ?, ti_full_hex = ?, 
                                         internal_id = ?, image_url = ?, image_url_alt = ?, extra_json = ?
                        WHERE source_unique_id = ?
                    """, recipe_data + (source_unique_id,))
                    
                    # Clear existing ingredients for this recipe
                    cursor.execute("DELETE FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,))
                else:
                    # Insert new recipe
                    cursor.execute("""
                        INSERT INTO recipes (name, source_unique_id, category, source, source_notes,
                                           version_added, buy_price, sell_price, hha_base, item_hex,
                                           ti_primary, ti_secondary, ti_customize_str, ti_full_hex, 
                                           internal_id, image_url, image_url_alt, extra_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, recipe_data)
                    recipe_id = cursor.lastrowid
                    self.import_stats["imported"] += 1
                
                # Insert recipe ingredients (for both new and updated recipes)
                ingredients = self._extract_recipe_ingredients(row)
                for ingredient_name, quantity in ingredients:
                    cursor.execute("""
                        INSERT INTO recipe_ingredients (recipe_id, ingredient_name, quantity)
                        VALUES (?, ?, ?)
                    """, (recipe_id, ingredient_name, quantity))
                
            except Exception as e:
                print(f"   Error processing recipe {name if 'name' in locals() else 'Unknown'}: {e}")
                self.import_stats["errors"] += 1
                continue
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} rows for recipes")

    def _import_critters_dataset(self, file_path: pathlib.Path, critter_type: str):
        """Import critters dataset (fish, insects, sea creatures)"""
        rows = self._read_csv_file(file_path)
        
        # Map critter type
        kind_map = {
            'fish': 'fish',
            'insects': 'insect', 
            'sea-creatures': 'sea'
        }
        kind = kind_map.get(critter_type, critter_type)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for row in rows:
            try:
                self.import_stats["processed"] += 1
                
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                
                # Check if critter already exists (use internal_id as unique identifier)
                internal_id = self._get_int_value(row, ['Internal ID'])
                cursor.execute("SELECT id FROM critters WHERE internal_id = ?", (internal_id,))
                if cursor.fetchone():
                    self.import_stats["skipped"] += 1
                    continue
                
                critter_data = self._map_critter_data(row, kind)
                cursor.execute("""
                    INSERT INTO critters (name, kind, internal_id, source_unique_id, sell_price,
                                        item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex,
                                        location, shadow_size, movement_speed, catch_difficulty, vision, 
                                        total_catches_to_unlock, spawn_rates, nh_jan, nh_feb, nh_mar,
                                        nh_apr, nh_may, nh_jun, nh_jul, nh_aug, nh_sep, nh_oct, nh_nov,
                                        nh_dec, sh_jan, sh_feb, sh_mar, sh_apr, sh_may, sh_jun, sh_jul,
                                        sh_aug, sh_sep, sh_oct, sh_nov, sh_dec, time_of_day, weather,
                                        rarity, description, catch_phrase, hha_base_points, hha_category,
                                        color1, color2, size, surface, icon_url, critterpedia_url,
                                        furniture_url, source, version_added, extra_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, critter_data)
                
                self.import_stats["imported"] += 1
                
            except Exception as e:
                print(f"Error processing critter row: {e}")
                self.import_stats["errors"] += 1
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} rows for {critter_type}")

    def _import_fossils_dataset(self, file_path: pathlib.Path):
        """Import fossils dataset"""
        rows = self._read_csv_file(file_path)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for row in rows:
            try:
                self.import_stats["processed"] += 1
                
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                
                # Check if fossil already exists (use internal_id as unique identifier)
                internal_id = self._get_int_value(row, ['Internal ID'])
                cursor.execute("SELECT id FROM fossils WHERE internal_id = ?", (internal_id,))
                if cursor.fetchone():
                    self.import_stats["skipped"] += 1
                    continue
                
                fossil_data = self._map_fossil_data(row)
                cursor.execute("""
                    INSERT INTO fossils (name, image_url, image_url_alt, buy_price, sell_price, fossil_group,
                                       description, hha_base_points, color1, color2, size, source,
                                       museum, interact, catalog, filename, internal_id, source_unique_id,
                                       item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex,
                                       extra_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, fossil_data)
                
                self.import_stats["imported"] += 1
                
            except Exception as e:
                print(f"Error processing fossil row: {e}")
                self.import_stats["errors"] += 1
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} rows for fossils")

    def _import_artwork_dataset(self, file_path: pathlib.Path):
        """Import artwork dataset"""
        rows = self._read_csv_file(file_path)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for row in rows:
            try:
                self.import_stats["processed"] += 1
                
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                
                # Check if artwork already exists (use internal_id as unique identifier)
                internal_id = self._get_int_value(row, ['Internal ID'])
                cursor.execute("SELECT id FROM artwork WHERE internal_id = ?", (internal_id,))
                if cursor.fetchone():
                    self.import_stats["skipped"] += 1
                    continue
                
                artwork_data = self._map_artwork_data(row)
                cursor.execute("""
                    INSERT INTO artwork (name, image_url, image_url_alt, genuine, art_category,
                                       buy_price, sell_price, color1, color2, size, real_artwork_title,
                                       artist, description, source, source_notes, hha_base_points,
                                       hha_concept1, hha_concept2, hha_series, hha_set, interact, tag,
                                       speaker_type, lighting_type, catalog, version_added, unlocked,
                                       filename, internal_id, source_unique_id,
                                       item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex,
                                       extra_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, artwork_data)
                
                self.import_stats["imported"] += 1
                
            except Exception as e:
                print(f"Error processing artwork row: {e}")
                self.import_stats["errors"] += 1
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} rows for artwork")

    def _import_villagers_dataset(self, file_path: pathlib.Path):
        """Import villagers dataset"""
        rows = self._read_csv_file(file_path)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for row in rows:
            try:
                self.import_stats["processed"] += 1
                
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                
                # Check if villager already exists (use internal_id if available, fallback to name)
                internal_id = self._get_int_value(row, ['Internal ID'])
                if internal_id:
                    cursor.execute("SELECT id FROM villagers WHERE internal_id = ?", (internal_id,))
                else:
                    cursor.execute("SELECT id FROM villagers WHERE name = ?", (name,))
                if cursor.fetchone():
                    self.import_stats["skipped"] += 1
                    continue
                
                villager_data = self._map_villager_data(row)
                cursor.execute("""
                    INSERT INTO villagers (name, species, gender, personality, subtype, hobby, birthday,
                                         catchphrase, favorite_song, favorite_saying, style1, style2, 
                                         color1, color2, default_clothing, default_umbrella, wallpaper,
                                         flooring, furniture_list, furniture_name_list, diy_workbench,
                                         kitchen_equipment, version_added, name_color, bubble_color,
                                         filename, source_unique_id, icon_image, photo_image, house_image)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, villager_data)
                
                self.import_stats["imported"] += 1
                
            except Exception as e:
                print(f"Error processing villager row: {e}")
                self.import_stats["errors"] += 1
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} rows for villagers")

    def _import_recipes_dataset(self, file_path: pathlib.Path):
        """Import recipes dataset"""
        rows = self._read_csv_file(file_path)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for row in rows:
            try:
                self.import_stats["processed"] += 1
                
                name = self._get_value(row, ['Name'])
                if not name:
                    self.import_stats["skipped"] += 1
                    continue
                
                # Check if recipe already exists (use internal_id as unique identifier)
                internal_id = self._get_int_value(row, ['Internal ID'])
                cursor.execute("SELECT id FROM recipes WHERE internal_id = ?", (internal_id,))
                if cursor.fetchone():
                    self.import_stats["skipped"] += 1
                    continue
                
                recipe_data = self._map_recipe_data(row)
                cursor.execute("""
                    INSERT INTO recipes (name, internal_id, product_item_id, category, source,
                                       source_notes, is_diy, buy_price, sell_price, hha_base,
                                       version_added, item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex,
                                       image_url, image_url_alt, extra_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, recipe_data)
                
                recipe_id = cursor.lastrowid
                
                # Add ingredients
                ingredients = self._extract_recipe_ingredients(row)
                for ingredient_name, quantity in ingredients:
                    cursor.execute("""
                        INSERT INTO recipe_ingredients (recipe_id, item_id, ingredient_name, quantity)
                        VALUES (?, ?, ?, ?)
                    """, (recipe_id, None, ingredient_name, quantity))
                
                self.import_stats["imported"] += 1
                
            except Exception as e:
                print(f"Error processing recipe row: {e}")
                self.import_stats["errors"] += 1
        
        conn.commit()
        conn.close()
        print(f"   Processed {len(rows)} rows for recipes")

    def _populate_search_index(self):
        """Populate the FTS5 search index"""
        print("\nPopulating search index...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Clear existing search index
            cursor.execute("DELETE FROM search_index")
            
            # Add items to search index
            cursor.execute("SELECT id, name, category FROM items")
            for item_id, name, category in cursor.fetchall():
                cursor.execute("""
                    INSERT INTO search_index (name, category, subcategory, ref_table, ref_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, 'item', category, 'items', str(item_id)))
            
            # Add critters to search index
            cursor.execute("SELECT id, name, kind FROM critters")
            for critter_id, name, kind in cursor.fetchall():
                cursor.execute("""
                    INSERT INTO search_index (name, category, subcategory, ref_table, ref_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, 'critter', kind, 'critters', str(critter_id)))
            
            # Add fossils to search index
            cursor.execute("SELECT id, name FROM fossils")
            for fossil_id, name in cursor.fetchall():
                cursor.execute("""
                    INSERT INTO search_index (name, category, subcategory, ref_table, ref_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, 'fossil', 'fossil', 'fossils', str(fossil_id)))
            
            # Add artwork to search index
            cursor.execute("SELECT id, name FROM artwork")
            for art_id, name in cursor.fetchall():
                cursor.execute("""
                    INSERT INTO search_index (name, category, subcategory, ref_table, ref_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, 'artwork', 'art', 'artwork', str(art_id)))
            
            # Add villagers to search index
            cursor.execute("SELECT id, name FROM villagers")
            for villager_id, name in cursor.fetchall():
                cursor.execute("""
                    INSERT INTO search_index (name, category, subcategory, ref_table, ref_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, 'villager', 'villager', 'villagers', str(villager_id)))
            
            # Add recipes to search index
            cursor.execute("SELECT id, name, category FROM recipes")
            for recipe_id, name, category in cursor.fetchall():
                cursor.execute("""
                    INSERT INTO search_index (name, category, subcategory, ref_table, ref_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, 'recipe', category or 'recipe', 'recipes', str(recipe_id)))
            
            conn.commit()
            print("   Search index populated")
            
        except sqlite3.Error as e:
            print(f"   Error populating search index: {e}")
        
        conn.close()

    def _populate_museum_index(self):
        """Populate the museum index for donations"""
        print("Populating museum index...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Clear existing museum index
            cursor.execute("DELETE FROM museum_index")
            
            # Add fish to museum index
            cursor.execute("SELECT id, name FROM critters WHERE kind = 'fish'")
            for critter_id, name in cursor.fetchall():
                cursor.execute("""
                    INSERT INTO museum_index (name, wing, ref_table, ref_id)
                    VALUES (?, ?, ?, ?)
                """, (name, 'fish', 'critters', critter_id))
            
            # Add insects to museum index
            cursor.execute("SELECT id, name FROM critters WHERE kind = 'insect'")
            for critter_id, name in cursor.fetchall():
                cursor.execute("""
                    INSERT INTO museum_index (name, wing, ref_table, ref_id)
                    VALUES (?, ?, ?, ?)
                """, (name, 'bugs', 'critters', critter_id))
            
            # Add sea creatures to museum index
            cursor.execute("SELECT id, name FROM critters WHERE kind = 'sea'")
            for critter_id, name in cursor.fetchall():
                cursor.execute("""
                    INSERT INTO museum_index (name, wing, ref_table, ref_id)
                    VALUES (?, ?, ?, ?)
                """, (name, 'sea', 'critters', critter_id))
            
            # Add fossils to museum index
            cursor.execute("SELECT id, name FROM fossils")
            for fossil_id, name in cursor.fetchall():
                cursor.execute("""
                    INSERT INTO museum_index (name, wing, ref_table, ref_id)
                    VALUES (?, ?, ?, ?)
                """, (name, 'fossils', 'fossils', fossil_id))
            
            # Add artwork to museum index
            cursor.execute("SELECT id, name FROM artwork")
            for art_id, name in cursor.fetchall():
                cursor.execute("""
                    INSERT INTO museum_index (name, wing, ref_table, ref_id)
                    VALUES (?, ?, ?, ?)
                """, (name, 'art', 'artwork', art_id))
            
            conn.commit()
            print("   Museum index populated")
            
        except sqlite3.Error as e:
            print(f"   Error populating museum index: {e}")
        
        conn.close()

    def build_ti_codes(self, internal_id: int, primary_index: Optional[int], secondary_index: Optional[int]) -> Tuple[str, Optional[int], Optional[int], Optional[str], str]:
        """Build TI codes from internal ID and variant indices"""
        # 1. Base item hex
        item_hex = format(internal_id, "04X")
        
        # 2. TI primary (use 0 if None)
        ti_primary = primary_index if primary_index is not None else 0
        
        # 3. TI secondary (only for 2D items)
        if secondary_index is None:
            ti_secondary = None
        else:
            ti_secondary = secondary_index * 32
        
        # 4. ti_customize_str
        if ti_secondary is None:
            ti_customize_str = f"{ti_primary}"
        else:
            ti_customize_str = f"{ti_primary} {ti_secondary}"
        
        # 5. Full TI drop hex
        if ti_secondary is None:
            # 1D: 000000 + primary(2) + 0000 + item_hex(4) = 16 chars
            ti_full_hex = f"000000{ti_primary:02X}0000{item_hex}"
        else:
            # 2D: 000000 + secondary(2) + 0000 + item_hex(4) = 16 chars
            ti_full_hex = f"000000{ti_secondary:02X}0000{item_hex}"
        
        return item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex

    # Data mapping helper methods
    
    def _map_item_data(self, row: Dict[str, str], category: str, is_base_item: bool = True) -> Tuple:
        """Map CSV row to items table data"""
        # For base items, we don't use the variant-specific source_unique_id
        # Instead, base items represent the general item concept
        base_item_id = None
        if not is_base_item:
            base_item_id = self._get_value(row, ['Unique Entry ID'])
        
        return (
            self._get_value(row, ['Name']),  # name
            category,  # category
            base_item_id,  # source_unique_id - NULL for base items, specific for individual variants
            self._get_int_value(row, ['Internal ID']),  # internal_group_id - Use Internal ID for grouping variants
            1 if self._get_value(row, ['DIY']) == 'Yes' else 0,  # is_diy
            self._get_int_value(row, ['Buy']),  # buy_price
            self._get_int_value(row, ['Sell']),  # sell_price
            self._get_int_value(row, ['HHA Base Points']),  # hha_base
            self._get_value(row, ['Source']),  # source
            self._get_value(row, ['Catalog']),  # catalog
            self._get_value(row, ['Version Added']),  # version_added
            self._get_value(row, ['Tag']),  # tag
            self._get_value(row, ['Style 1']),  # style1
            self._get_value(row, ['Style 2']),  # style2
            self._get_value(row, ['Label Themes']),  # label_themes
            self._get_value(row, ['Filename']),  # filename
            self._get_image_url_columns(row)[0],  # image_url (dynamically detected)
            None  # extra_json
        )

    def _map_variant_data(self, row: Dict[str, str], item_id: int) -> Tuple:
        """Map CSV row to item_variants table data - always creates a variant record"""
        # Get variant-specific data
        variation = self._get_value(row, ['Variation'])
        body_title = self._get_value(row, ['Body Title'])
        pattern = self._get_value(row, ['Pattern'])
        variant_id_raw = self._get_value(row, ['Variant ID'])
        
        # Parse variant ID for primary/secondary indices if available
        primary_index = None
        secondary_index = None
        if variant_id_raw and '_' in variant_id_raw:
            try:
                parts = variant_id_raw.split('_')
                if len(parts) >= 2:
                    primary_index = int(parts[0])
                    secondary_index = int(parts[1])
            except (ValueError, IndexError):
                pass  # Keep as None if parsing fails
        
        # Get internal_id - try variant-specific first, then fall back to item internal_id
        internal_id = self._get_int_value(row, ['Internal ID'])
        if not internal_id:
            # If no internal_id available, we can't calculate TI codes
            # This should be rare, but we'll handle it gracefully
            item_hex = None
            ti_primary = primary_index
            ti_secondary = secondary_index * 32 if secondary_index is not None else None
            ti_customize_str = None
            ti_full_hex = None
        else:
            # Calculate TI codes
            item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex = self.build_ti_codes(
                internal_id, primary_index, secondary_index
            )
        
        # Parse customization flags
        body_customizable = 1 if self._get_value(row, ['Body Customize']) == 'Yes' else 0
        pattern_customizable = 1 if self._get_value(row, ['Pattern Customize']) == 'Yes' else 0
        
        # Check for Cyrus customization (expensive customization)
        cyrus_price = self._get_int_value(row, ['Cyrus Customize Price'])
        cyrus_customizable = 1 if cyrus_price and cyrus_price > 0 else 0
        
        # Clean up variation label - convert "NA" to None for consistency
        clean_variation = variation if variation and variation != 'NA' else None
            
        return (
            item_id,  # item_id
            self._get_value(row, ['Unique Entry ID']),  # source_unique_id
            variant_id_raw,  # variant_id_raw
            primary_index,  # primary_index
            secondary_index,  # secondary_index
            clean_variation,  # variation_label
            body_title,  # body_title
            pattern,  # pattern_label
            self._get_value(row, ['Pattern Title']),  # pattern_title
            self._get_value(row, ['Color 1']),  # color1
            self._get_value(row, ['Color 2']),  # color2
            body_customizable,  # body_customizable
            pattern_customizable,  # pattern_customizable
            cyrus_customizable,  # cyrus_customizable
            self._get_value(row, ['Pattern Customize Options']),  # pattern_options
            internal_id,  # internal_id
            item_hex,  # item_hex (calculated)
            ti_primary,  # ti_primary (calculated)
            ti_secondary,  # ti_secondary (calculated)
            ti_customize_str,  # ti_customize_str (calculated)
            ti_full_hex,  # ti_full_hex (calculated)
            self._get_image_url_columns(row)[0],  # image_url (dynamically detected)
            self._get_image_url_columns(row)[1]   # image_url_alt (dynamically detected)
        )

    def _map_critter_data(self, row: Dict[str, str], kind: str) -> Tuple:
        """Map CSV row to critters table data"""
        # Get internal_id and calculate TI codes
        internal_id = self._get_int_value(row, ['Internal ID'])
        if internal_id:
            item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex = self.build_ti_codes(
                internal_id, None, None  # Critters are typically 1D with no variant indices
            )
        else:
            item_hex = ti_primary = ti_secondary = ti_customize_str = ti_full_hex = None
        
        return (
            self._get_value(row, ['Name']),  # name
            kind,  # kind
            self._get_value(row, ['Unique Entry ID']),  # source_unique_id
            internal_id,  # internal_id
            self._get_int_value(row, ['Sell']),  # sell_price
            item_hex,  # item_hex (calculated)
            ti_primary,  # ti_primary (calculated)
            ti_secondary,  # ti_secondary (calculated)
            ti_customize_str,  # ti_customize_str (calculated)
            ti_full_hex,  # ti_full_hex (calculated)
            self._get_value(row, ['Where/How', 'Location']),  # location
            self._get_value(row, ['Shadow']),  # shadow_size
            self._get_value(row, ['Movement Speed']),  # movement_speed
            self._get_value(row, ['Catch Difficulty']),  # catch_difficulty
            self._get_value(row, ['Vision']),  # vision
            self._get_value(row, ['Total Catches to Unlock']),  # total_catches_to_unlock
            self._get_value(row, ['Spawn Rates']),  # spawn_rates
            self._get_value(row, ['NH Jan']),  # nh_jan
            self._get_value(row, ['NH Feb']),  # nh_feb
            self._get_value(row, ['NH Mar']),  # nh_mar
            self._get_value(row, ['NH Apr']),  # nh_apr
            self._get_value(row, ['NH May']),  # nh_may
            self._get_value(row, ['NH Jun']),  # nh_jun
            self._get_value(row, ['NH Jul']),  # nh_jul
            self._get_value(row, ['NH Aug']),  # nh_aug
            self._get_value(row, ['NH Sep']),  # nh_sep
            self._get_value(row, ['NH Oct']),  # nh_oct
            self._get_value(row, ['NH Nov']),  # nh_nov
            self._get_value(row, ['NH Dec']),  # nh_dec
            self._get_value(row, ['SH Jan']),  # sh_jan
            self._get_value(row, ['SH Feb']),  # sh_feb
            self._get_value(row, ['SH Mar']),  # sh_mar
            self._get_value(row, ['SH Apr']),  # sh_apr
            self._get_value(row, ['SH May']),  # sh_may
            self._get_value(row, ['SH Jun']),  # sh_jun
            self._get_value(row, ['SH Jul']),  # sh_jul
            self._get_value(row, ['SH Aug']),  # sh_aug
            self._get_value(row, ['SH Sep']),  # sh_sep
            self._get_value(row, ['SH Oct']),  # sh_oct
            self._get_value(row, ['SH Nov']),  # sh_nov
            self._get_value(row, ['SH Dec']),  # sh_dec
            None,  # time_of_day (may need custom logic for specific formats)
            self._get_value(row, ['Weather']),  # weather
            None,  # rarity
            self._get_value(row, ['Description']),  # description
            self._get_value(row, ['Catch phrase']),  # catch_phrase
            self._get_int_value(row, ['HHA Base Points']),  # hha_base_points
            self._get_value(row, ['HHA Category']),  # hha_category
            self._get_value(row, ['Color 1']),  # color1
            self._get_value(row, ['Color 2']),  # color2
            self._get_value(row, ['Size']),  # size
            self._get_value(row, ['Surface']),  # surface
            self._get_value(row, ['Icon Image']),  # icon_url
            self._get_value(row, ['Critterpedia Image']),  # critterpedia_url
            self._get_value(row, ['Furniture Image']),  # furniture_url
            self._derive_critter_source(row, kind),  # source
            self._get_critter_version_added(row, kind),  # version_added
            None   # extra_json
        )

    def _map_fossil_data(self, row: Dict[str, str]) -> Tuple:
        """Map CSV row to fossils table data"""
        main_img, alt_img = self._get_image_url_columns(row)
        
        # Get internal_id and calculate TI codes
        internal_id = self._get_int_value(row, ['Internal ID'])
        if internal_id:
            item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex = self.build_ti_codes(
                internal_id, None, None  # Fossils are typically 1D with no variant indices
            )
        else:
            item_hex = ti_primary = ti_secondary = ti_customize_str = ti_full_hex = None
        
        return (
            self._get_value(row, ['Name']),  # name
            main_img,  # image_url (dynamically detected)
            alt_img,   # image_url_alt (dynamically detected)
            self._get_int_value(row, ['Buy']),  # buy_price
            self._get_int_value(row, ['Sell']),  # sell_price
            self._get_value(row, ['Fossil Group']),  # fossil_group
            self._get_value(row, ['Description']),  # description
            self._get_int_value(row, ['HHA Base Points']),  # hha_base_points
            self._get_value(row, ['Color 1']),  # color1
            self._get_value(row, ['Color 2']),  # color2
            self._get_value(row, ['Size']),  # size
            self._get_value(row, ['Source']),  # source
            self._get_value(row, ['Museum']),  # museum
            self._get_value(row, ['Interact']),  # interact
            self._get_value(row, ['Catalog']),  # catalog
            self._get_value(row, ['Filename']),  # filename
            internal_id,  # internal_id
            self._get_value(row, ['Unique Entry ID']),  # source_unique_id
            item_hex,  # item_hex (calculated)
            ti_primary,  # ti_primary (calculated)
            ti_secondary,  # ti_secondary (calculated)
            ti_customize_str,  # ti_customize_str (calculated)
            ti_full_hex,  # ti_full_hex (calculated)
            None  # extra_json
        )

    def _map_artwork_data(self, row: Dict[str, str]) -> Tuple:
        """Map CSV row to artwork table data"""
        main_img, alt_img = self._get_image_url_columns(row)
        
        # Get internal_id and calculate TI codes
        internal_id = self._get_int_value(row, ['Internal ID'])
        if internal_id:
            item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex = self.build_ti_codes(
                internal_id, None, None  # Artwork is typically 1D with no variant indices
            )
        else:
            item_hex = ti_primary = ti_secondary = ti_customize_str = ti_full_hex = None
        
        return (
            self._get_value(row, ['Name']),  # name
            main_img,  # image_url (dynamically detected)
            alt_img,   # image_url_alt (dynamically detected)
            1 if self._get_value(row, ['Genuine']) == 'Yes' else 0,  # genuine
            self._get_value(row, ['Category', 'Art Category']),  # art_category
            self._get_int_value(row, ['Buy']),  # buy_price
            self._get_int_value(row, ['Sell']),  # sell_price
            self._get_value(row, ['Color 1']),  # color1
            self._get_value(row, ['Color 2']),  # color2
            self._get_value(row, ['Size']),  # size
            self._get_value(row, ['Real Artwork Title']),  # real_artwork_title
            self._get_value(row, ['Artist']),  # artist
            self._get_value(row, ['Description']),  # description
            self._get_value(row, ['Source']),  # source
            self._get_value(row, ['Source Notes']),  # source_notes
            self._get_int_value(row, ['HHA Base Points']),  # hha_base_points
            self._get_value(row, ['HHA Concept 1']),  # hha_concept1
            self._get_value(row, ['HHA Concept 2']),  # hha_concept2
            self._get_value(row, ['HHA Series']),  # hha_series
            self._get_value(row, ['HHA Set']),  # hha_set
            self._get_value(row, ['Interact']),  # interact
            self._get_value(row, ['Tag']),  # tag
            self._get_value(row, ['Speaker Type']),  # speaker_type
            self._get_value(row, ['Lighting Type']),  # lighting_type
            self._get_value(row, ['Catalog']),  # catalog
            self._get_value(row, ['Version Added']),  # version_added
            self._get_value(row, ['Unlocked?']),  # unlocked
            self._get_value(row, ['Filename']),  # filename
            internal_id,  # internal_id
            self._get_value(row, ['Unique Entry ID']),  # source_unique_id
            item_hex,  # item_hex (calculated)
            ti_primary,  # ti_primary (calculated)
            ti_secondary,  # ti_secondary (calculated)
            ti_customize_str,  # ti_customize_str (calculated)
            ti_full_hex,  # ti_full_hex (calculated)
            None  # extra_json
        )

    def _map_villager_data(self, row: Dict[str, str]) -> Tuple:
        """Map CSV row to villagers table data"""
        return (
            self._get_value(row, ['Name']),  # name
            self._get_value(row, ['Species']),  # species
            self._get_value(row, ['Gender']),  # gender
            self._get_value(row, ['Personality']),  # personality
            self._get_value(row, ['Subtype']),  # subtype
            self._get_value(row, ['Hobby']),  # hobby
            self._get_value(row, ['Birthday']),  # birthday
            self._get_value(row, ['Catchphrase']),  # catchphrase
            self._get_value(row, ['Favorite Song']),  # favorite_song
            self._get_value(row, ['Favorite Saying']),  # favorite_saying
            self._get_value(row, ['Style 1']),  # style1
            self._get_value(row, ['Style 2']),  # style2
            self._get_value(row, ['Color 1']),  # color1
            self._get_value(row, ['Color 2']),  # color2
            self._get_value(row, ['Default Clothing']),  # default_clothing
            self._get_value(row, ['Default Umbrella']),  # default_umbrella
            self._get_value(row, ['Wallpaper']),  # wallpaper
            self._get_value(row, ['Flooring']),  # flooring
            self._get_value(row, ['Furniture List']),  # furniture_list
            self._get_value(row, ['Furniture Name List']),  # furniture_name_list
            self._get_value(row, ['DIY Workbench']),  # diy_workbench
            self._get_value(row, ['Kitchen Equipment']),  # kitchen_equipment
            self._get_value(row, ['Version Added']),  # version_added
            self._get_value(row, ['Name Color']),  # name_color
            self._get_value(row, ['Bubble Color']),  # bubble_color
            self._get_value(row, ['Filename']),  # filename
            self._get_value(row, ['Unique Entry ID']),  # source_unique_id
            self._get_value(row, ['Icon Image']),  # icon_image
            self._get_value(row, ['Photo Image']),  # photo_image
            self._get_value(row, ['House Image'])   # house_image
        )

    def _map_recipe_data(self, row: Dict[str, str]) -> Tuple:
        """Map CSV row to recipes table data"""
        # Get internal_id and calculate TI codes
        internal_id = self._get_int_value(row, ['Internal ID'])
        if internal_id:
            item_hex, ti_primary, ti_secondary, ti_customize_str, ti_full_hex = self.build_ti_codes(
                internal_id, None, None  # Recipes are typically 1D with no variant indices
            )
        else:
            item_hex = ti_primary = ti_secondary = ti_customize_str = ti_full_hex = None
        
        return (
            self._get_value(row, ['Name']),  # name
            self._get_value(row, ['Unique Entry ID']),  # source_unique_id
            self._get_value(row, ['Category']),  # category
            self._get_value(row, ['Source']),  # source
            self._get_value(row, ['Source Notes']),  # source_notes
            self._get_value(row, ['Version Added']),  # version_added
            None,  # buy_price (recipes don't typically have buy prices)
            self._get_int_value(row, ['Sell']),  # sell_price
            None,  # hha_base
            item_hex,  # item_hex (calculated)
            ti_primary,  # ti_primary (calculated)
            ti_secondary,  # ti_secondary (calculated)
            ti_customize_str,  # ti_customize_str (calculated)
            ti_full_hex,  # ti_full_hex (calculated)
            internal_id,  # internal_id
            self._get_image_url_columns(row)[0],  # image_url (dynamically detected)
            self._get_image_url_columns(row)[1],  # image_url_alt (dynamically detected)
            None  # extra_json
        )

    def _extract_recipe_ingredients(self, row: Dict[str, str]) -> List[Tuple[str, int]]:
        """Extract ingredients from recipe row"""
        ingredients = []
        for i in range(1, 7):  # Up to 6 ingredients
            quantity_key = f'#{i}'
            material_key = f'Material {i}'
            
            quantity = self._get_int_value(row, [quantity_key])
            material = self._get_value(row, [material_key])
            
            if quantity and material:
                ingredients.append((material, quantity))
        
        return ingredients

    def _derive_critter_source(self, row: Dict[str, str], kind: str) -> Optional[str]:
        """Derive source information for critters based on available data"""
        # Check for explicit unlock requirements
        unlock_catches = self._get_int_value(row, ['Total Catches to Unlock'])
        
        # Determine base source based on critter type
        if kind == 'fish':
            base_source = "Fishing"
        elif kind == 'insect':
            base_source = "Bug catching"
        elif kind == 'sea':
            base_source = "Diving"
        else:
            base_source = "Unknown"
        
        # Add unlock requirement if present
        if unlock_catches and unlock_catches > 0:
            return f"{base_source} (unlocked after {unlock_catches} donations)"
        else:
            return base_source

    def _get_critter_version_added(self, row: Dict[str, str], kind: str) -> Optional[str]:
        """Get version added information for critters"""
        # Check for explicit version column (available in sea-creatures)
        version = self._get_value(row, ['Version Added'])
        if version:
            return version
        
        # For fish and insects, most were available at launch
        # But some might have unlock requirements indicating later additions
        unlock_catches = self._get_int_value(row, ['Total Catches to Unlock'])
        
        if unlock_catches and unlock_catches > 0:
            # Critters with unlock requirements were typically added in updates
            return "1.0.0+"  # Indicates base game but may require progression
        else:
            # Most basic critters were available at launch
            return "1.0.0"

    def _get_image_url_columns(self, row: Dict[str, str]) -> Tuple[Optional[str], Optional[str]]:
        """Dynamically determine which columns contain image URLs for this dataset"""
        # Priority order for main image URL
        main_image_candidates = ['Image', 'Inventory Image', 'Closet Image', 'Icon Image', 'Photo Image']
        # Priority order for alternate image URL  
        alt_image_candidates = ['Storage Image', 'High-Res Texture', 'Critterpedia Image', 'Furniture Image']
        
        # Use _get_value which handles IMAGE formula extraction
        main_url = self._get_value(row, main_image_candidates)
        alt_url = self._get_value(row, alt_image_candidates)
                
        return main_url, alt_url

    # Utility methods
    
    def _read_csv_file(self, file_path: pathlib.Path) -> List[Dict[str, str]]:
        """Read CSV file and return list of dictionaries"""
        # Try different encodings
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    # Handle BOM if present
                    content = f.read()
                    if content.startswith('\ufeff'):
                        content = content[1:]
                    
                    # Parse CSV
                    csv_reader = csv.DictReader(content.splitlines())
                    return list(csv_reader)
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail, raise the last error
        raise UnicodeDecodeError(f"Could not decode file {file_path} with any of the attempted encodings: {encodings}")

    def _get_value(self, row: Dict[str, str], possible_keys: List[str]) -> Optional[str]:
        """Get value from row, trying multiple possible column names"""
        for key in possible_keys:
            if key in row and row[key] is not None:
                # Convert to string if it's not already
                raw_value = row[key]
                if isinstance(raw_value, (int, float)):
                    value = str(raw_value)
                else:
                    value = raw_value.strip() if hasattr(raw_value, 'strip') else str(raw_value)
                
                if value and value.upper() not in ['NFS', 'NA', 'N/A', '']:
                    # Clean up corrupted Unicode characters commonly found in time ranges
                    value = self._clean_unicode_characters(value)
                    # Extract URL from IMAGE formula if present
                    value = self._extract_url_from_formula(value)
                    return value
        return None

    def _extract_url_from_formula(self, value: str) -> str:
        """Extract URL from IMAGE formula or return original value"""
        if value.startswith('=IMAGE("') and value.endswith('")'):
            # Extract URL from =IMAGE("url") formula
            return value[8:-2]  # Remove =IMAGE(" and ")
        elif value.startswith('=IMAGE(') and value.endswith(')'):
            # Handle =IMAGE(url) without quotes  
            return value[7:-1]  # Remove =IMAGE( and )
        return value
    
    def _clean_unicode_characters(self, text: str) -> str:
        """Clean up corrupted Unicode characters, especially dash characters in time ranges"""
        if not text:
            return text
        
        # Replace various corrupted dash representations with proper en dash
        # Order matters - do longer patterns first to avoid partial replacements
        replacements = [
            ('–\xa0', '–'),     # En dash + non-breaking space (from cp1252 decoding of 0x96 0xA0)
            ('\x96\xa0', '–'),  # Raw byte corruption (if it somehow gets through)
            ('â��', '–'),       # UTF-8 corruption pattern
            ('â€"', '–'),       # HTML entity corruption
            ('â€"', '–'),       # Another HTML entity pattern
            ('��', '–'),        # Double replacement character
            ('�', '–'),         # Single replacement character  
            ('—', '–'),         # Em dash to en dash for consistency
            (' - ', ' – '),     # Regular hyphen surrounded by spaces
            ('–', '–'),         # Ensure proper en dash (in case of mixed encoding)
        ]
        
        for old, new in replacements:
            text = text.replace(old, new)
        
        return text

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

    def _print_final_stats(self):
        """Print final import statistics"""
        print("\n" + "=" * 60)
        print("FINAL IMPORT STATISTICS")
        print("=" * 60)
        print(f"Total Processed:  {self.import_stats['processed']:,}")
        print(f"Total Imported:   {self.import_stats['imported']:,}")
        print(f"Total Skipped:    {self.import_stats['skipped']:,}")
        print(f"Total Errors:     {self.import_stats['errors']:,}")
        
        if self.import_stats['errors'] == 0:
            print("\nImport completed successfully with no errors!")
        else:
            print(f"\nImport completed with {self.import_stats['errors']} errors")
        
        print(f"\nDatabase created: {self.db_path}")

def main():
    """Main function"""
    print("ACNH Complete Dataset Importer")
    print("=" * 60)
    
    # Initialize importer
    importer = ACNHDatasetImporter()
    
    # Check if datasets directory exists
    if not importer.datasets_dir.exists():
        print(f"Datasets directory not found: {importer.datasets_dir}")
        print("Please ensure the datasets directory exists with CSV files")
        return 1
    
    # Initialize database
    try:
        importer.init_database()
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        return 1
    
    # Import all datasets
    try:
        importer.import_all_datasets()
    except Exception as e:
        print(f"Import failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())