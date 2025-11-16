#!/usr/bin/env python3
"""
Complete ACNH Dataset Importer
Imports all CSV datasets into the nooklook.db SQLite database using the nooklook_schema.sql structure
"""
import sqlite3
import csv
import pathlib
import sys
import os
import json
from typing import List, Dict, Any, Optional, Tuple

class ACNHDatasetImporter:
    """Imports all ACNH datasets from CSV files into the database"""
    
    def __init__(self, db_path: str = "nooklook.db", datasets_dir: str = "datasets"):
        self.db_path = db_path
        self.datasets_dir = pathlib.Path(datasets_dir)
        self.import_stats = {
            "processed": 0,
            "imported": 0,
            "skipped": 0,
            "errors": 0
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
            file_path = self.datasets_dir / filename
            if file_path.exists():
                print(f"\nProcessing {filename}")
                try:
                    if table_type == 'items':
                        self._import_items_dataset(file_path, category)
                    elif table_type == 'critters':
                        self._import_critters_dataset(file_path, category)
                    elif table_type == 'fossils':
                        self._import_fossils_dataset(file_path)
                    elif table_type == 'artwork':
                        self._import_artwork_dataset(file_path)
                    elif table_type == 'villagers':
                        self._import_villagers_dataset(file_path)
                    elif table_type == 'recipes':
                        self._import_recipes_dataset(file_path)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    self.import_stats["errors"] += 1
            else:
                print(f"File not found: {filename}")
        
        # Populate search index and museum index
        self._populate_search_index()
        self._populate_museum_index()
        
        self._print_final_stats()

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
                
                # Check if item already exists (use internal_group_id + category as unique identifier)
                internal_group_id = self._get_int_value(row, ['ClothGroup ID', 'Internal ID'])
                cursor.execute("SELECT id FROM items WHERE internal_group_id = ? AND category = ?", (internal_group_id, category))
                existing_item = cursor.fetchone()
                
                if existing_item:
                    item_id = existing_item[0]
                else:
                    # Insert base item
                    item_data = self._map_item_data(row, category)
                    cursor.execute("""
                        INSERT INTO items (name, category, internal_group_id, is_diy, buy_price, sell_price, 
                                         hha_base, source, catalog, version_added, tag, style1, style2, 
                                         label_themes, filename, image_url, extra_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    INSERT INTO critters (name, kind, internal_id, unique_entry_id, sell_price,
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
                                       museum, interact, catalog, filename, internal_id, unique_entry_id,
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
                                       filename, internal_id, unique_entry_id,
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
                                         filename, unique_entry_id, icon_image, photo_image, house_image)
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
    
    def _map_item_data(self, row: Dict[str, str], category: str) -> Tuple:
        """Map CSV row to items table data"""
        return (
            self._get_value(row, ['Name']),  # name
            category,  # category
            self._get_int_value(row, ['ClothGroup ID', 'Internal ID']),  # internal_group_id
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
            internal_id,  # internal_id
            self._get_value(row, ['Unique Entry ID']),  # unique_entry_id
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
            self._get_value(row, ['Unique Entry ID']),  # unique_entry_id
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
            self._get_value(row, ['Unique Entry ID']),  # unique_entry_id
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
            self._get_value(row, ['Unique Entry ID']),  # unique_entry_id
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
            internal_id,  # internal_id
            None,  # product_item_id (would need to lookup)
            self._get_value(row, ['Category']),  # category
            self._get_value(row, ['Source']),  # source
            self._get_value(row, ['Source Notes']),  # source_notes
            1,  # is_diy (all recipes are DIY by default)
            None,  # buy_price (NFS)
            self._get_int_value(row, ['Sell']),  # sell_price
            None,  # hha_base
            self._get_value(row, ['Version Added']),  # version_added
            item_hex,  # item_hex (calculated)
            ti_primary,  # ti_primary (calculated)
            ti_secondary,  # ti_secondary (calculated)
            ti_customize_str,  # ti_customize_str (calculated)
            ti_full_hex,  # ti_full_hex (calculated)
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
        
        main_url = None
        alt_url = None
        
        # Find main image URL
        for candidate in main_image_candidates:
            if candidate in row and row[candidate] and row[candidate].strip() and row[candidate].strip().upper() not in ['NA', 'NFS', 'N/A']:
                main_url = row[candidate].strip()
                break
        
        # Find alternate image URL  
        for candidate in alt_image_candidates:
            if candidate in row and row[candidate] and row[candidate].strip() and row[candidate].strip().upper() not in ['NA', 'NFS', 'N/A']:
                alt_url = row[candidate].strip()
                break
                
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
            if key in row and row[key] and row[key].strip():
                value = row[key].strip()
                if value.upper() not in ['NFS', 'NA', 'N/A', '']:
                    # Clean up corrupted Unicode characters commonly found in time ranges
                    value = self._clean_unicode_characters(value)
                    return value
        return None

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