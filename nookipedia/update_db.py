#!/usr/bin/env python3
"""
Update database with Nookipedia URLs.
This script reads the JSON files created by fetch_urls.py and updates the database.
"""

import sqlite3
import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from nookipedia.client import load_urls_from_json

class NookipediaDBUpdater:
    """
    Updates the database with Nookipedia URLs by matching names.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the updater.
        
        Args:
            db_path: Path to the SQLite database
        """
        self.db_path = db_path
        self.conn = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable dict-like access
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
    
    def normalize_name(self, name: str) -> str:
        """
        Normalize a name for matching (lowercase, strip spaces).
        
        Args:
            name: Original name
            
        Returns:
            Normalized name
        """
        return name.lower().strip()
    
    def update_items_urls(self, urls_data: List[Dict[str, str]], categories: List[str] = None) -> Tuple[int, int]:
        """
        Update items table with Nookipedia URLs.
        
        Args:
            urls_data: List of dicts with 'name' and 'url' keys
            categories: List of categories to filter by (optional)
            
        Returns:
            Tuple of (updated_count, total_items)
        """
        cursor = self.conn.cursor()
        
        # Build query with optional category filter
        where_clause = ""
        params = []
        if categories:
            placeholders = ",".join("?" * len(categories))
            where_clause = f" WHERE category IN ({placeholders})"
            params = categories
        
        # Get all items from database
        cursor.execute(f"SELECT id, name, category FROM items{where_clause}", params)
        db_items = cursor.fetchall()
        
        # Create lookup dict for Nookipedia URLs (normalized name -> url)
        url_lookup = {self.normalize_name(item['name']): item['url'] for item in urls_data}
        
        updated_count = 0
        total_items = len(db_items)
        
        for db_item in db_items:
            normalized_db_name = self.normalize_name(db_item['name'])
            
            if normalized_db_name in url_lookup:
                nookipedia_url = url_lookup[normalized_db_name]
                cursor.execute(
                    "UPDATE items SET nookipedia_url = ? WHERE id = ?",
                    (nookipedia_url, db_item['id'])
                )
                updated_count += 1
                logger.debug(f"Updated item '{db_item['name']}' with URL: {nookipedia_url}")
        
        self.conn.commit()
        return updated_count, total_items
    
    def update_recipes_urls(self, urls_data: List[Dict[str, str]]) -> Tuple[int, int]:
        """
        Update recipes table with Nookipedia URLs.
        
        Args:
            urls_data: List of dicts with 'name' and 'url' keys
            
        Returns:
            Tuple of (updated_count, total_recipes)
        """
        cursor = self.conn.cursor()
        
        # Get all recipes from database
        cursor.execute("SELECT id, name FROM recipes")
        db_recipes = cursor.fetchall()
        
        # Create lookup dict for Nookipedia URLs
        url_lookup = {self.normalize_name(item['name']): item['url'] for item in urls_data}
        
        updated_count = 0
        total_recipes = len(db_recipes)
        
        for db_recipe in db_recipes:
            normalized_db_name = self.normalize_name(db_recipe['name'])
            
            if normalized_db_name in url_lookup:
                nookipedia_url = url_lookup[normalized_db_name]
                cursor.execute(
                    "UPDATE recipes SET nookipedia_url = ? WHERE id = ?",
                    (nookipedia_url, db_recipe['id'])
                )
                updated_count += 1
                logger.debug(f"Updated recipe '{db_recipe['name']}' with URL: {nookipedia_url}")
        
        self.conn.commit()
        return updated_count, total_recipes
    
    def update_critters_urls(self, urls_data: List[Dict[str, str]], kind: str) -> Tuple[int, int]:
        """
        Update critters table with Nookipedia URLs.
        
        Args:
            urls_data: List of dicts with 'name' and 'url' keys
            kind: Type of critter ('fish', 'bug', 'sea')
            
        Returns:
            Tuple of (updated_count, total_critters)
        """
        cursor = self.conn.cursor()
        
        # Get critters of specified kind from database
        cursor.execute("SELECT id, name FROM critters WHERE kind = ?", (kind,))
        db_critters = cursor.fetchall()
        
        # Create lookup dict for Nookipedia URLs
        url_lookup = {self.normalize_name(item['name']): item['url'] for item in urls_data}
        
        updated_count = 0
        total_critters = len(db_critters)
        
        for db_critter in db_critters:
            normalized_db_name = self.normalize_name(db_critter['name'])
            
            if normalized_db_name in url_lookup:
                nookipedia_url = url_lookup[normalized_db_name]
                cursor.execute(
                    "UPDATE critters SET nookipedia_url = ? WHERE id = ?",
                    (nookipedia_url, db_critter['id'])
                )
                updated_count += 1
                logger.debug(f"Updated {kind} '{db_critter['name']}' with URL: {nookipedia_url}")
        
        self.conn.commit()
        return updated_count, total_critters
    
    def update_fossils_urls(self, urls_data: List[Dict[str, str]]) -> Tuple[int, int]:
        """
        Update fossils table with Nookipedia URLs.
        
        Args:
            urls_data: List of dicts with 'name' and 'url' keys
            
        Returns:
            Tuple of (updated_count, total_fossils)
        """
        cursor = self.conn.cursor()
        
        # Get all fossils from database
        cursor.execute("SELECT id, name FROM fossils")
        db_fossils = cursor.fetchall()
        
        # Create lookup dict for Nookipedia URLs
        url_lookup = {self.normalize_name(item['name']): item['url'] for item in urls_data}
        
        updated_count = 0
        total_fossils = len(db_fossils)
        
        for db_fossil in db_fossils:
            normalized_db_name = self.normalize_name(db_fossil['name'])
            
            if normalized_db_name in url_lookup:
                nookipedia_url = url_lookup[normalized_db_name]
                cursor.execute(
                    "UPDATE fossils SET nookipedia_url = ? WHERE id = ?",
                    (nookipedia_url, db_fossil['id'])
                )
                updated_count += 1
                logger.debug(f"Updated fossil '{db_fossil['name']}' with URL: {nookipedia_url}")
        
        self.conn.commit()
        return updated_count, total_fossils
    
    def update_artwork_urls(self, urls_data: List[Dict[str, str]]) -> Tuple[int, int]:
        """
        Update artwork table with Nookipedia URLs.
        
        Args:
            urls_data: List of dicts with 'name' and 'url' keys
            
        Returns:
            Tuple of (updated_count, total_artwork)
        """
        cursor = self.conn.cursor()
        
        # Get all artwork from database
        cursor.execute("SELECT id, name FROM artwork")
        db_artwork = cursor.fetchall()
        
        # Create lookup dict for Nookipedia URLs
        url_lookup = {self.normalize_name(item['name']): item['url'] for item in urls_data}
        
        updated_count = 0
        total_artwork = len(db_artwork)
        
        for db_art in db_artwork:
            normalized_db_name = self.normalize_name(db_art['name'])
            
            if normalized_db_name in url_lookup:
                nookipedia_url = url_lookup[normalized_db_name]
                cursor.execute(
                    "UPDATE artwork SET nookipedia_url = ? WHERE id = ?",
                    (nookipedia_url, db_art['id'])
                )
                updated_count += 1
                logger.debug(f"Updated artwork '{db_art['name']}' with URL: {nookipedia_url}")
        
        self.conn.commit()
        return updated_count, total_artwork
    
    def update_villagers_urls(self, urls_data: List[Dict[str, str]]) -> Tuple[int, int]:
        """
        Update villagers table with Nookipedia URLs and house images.
        
        Args:
            urls_data: List of dicts with villager data including NH details
            
        Returns:
            Tuple of (updated_count, total_villagers)
        """
        cursor = self.conn.cursor()
        
        # Get all villagers from database
        cursor.execute("SELECT id, name, house_image, house_interior_image, photo_image, icon_image FROM villagers")
        db_villagers = cursor.fetchall()
        
        # Create lookup dict for Nookipedia villager data
        villager_lookup = {self.normalize_name(item['name']): item for item in urls_data}
        
        updated_count = 0
        total_villagers = len(db_villagers)
        
        for db_villager in db_villagers:
            normalized_db_name = self.normalize_name(db_villager['name'])
            
            if normalized_db_name in villager_lookup:
                villager_data = villager_lookup[normalized_db_name]
                
                # Extract data to update
                nookipedia_url = villager_data.get('url')
                house_exterior_url = None
                house_interior_url = None
                photo_url = None
                icon_url = None
                
                # Extract images from NH details if available
                nh_details = villager_data.get('nh_details')
                if nh_details and isinstance(nh_details, dict):
                    house_exterior_url = nh_details.get('house_exterior_url')
                    house_interior_url = nh_details.get('house_interior_url')
                    photo_url = nh_details.get('image_url')
                    icon_url = nh_details.get('icon_url')
                
                # Prepare update fields and values
                update_fields = []
                update_values = []
                
                if nookipedia_url:
                    update_fields.append("nookipedia_url = ?")
                    update_values.append(nookipedia_url)
                
                # Update house_image (exterior) if missing or if we have a new one
                if house_exterior_url and (not db_villager['house_image'] or db_villager['house_image'] != house_exterior_url):
                    update_fields.append("house_image = ?")
                    update_values.append(house_exterior_url)
                
                # Update house_interior_image if we have one
                if house_interior_url and (not db_villager['house_interior_image'] or db_villager['house_interior_image'] != house_interior_url):
                    update_fields.append("house_interior_image = ?")
                    update_values.append(house_interior_url)
                
                # Always update photo_image with Nookipedia data (overwrite existing for better quality)
                if photo_url:
                    update_fields.append("photo_image = ?")
                    update_values.append(photo_url)
                
                # Always update icon_image with Nookipedia data (overwrite existing)
                if icon_url:
                    update_fields.append("icon_image = ?")
                    update_values.append(icon_url)
                
                # Execute update if we have fields to update
                if update_fields:
                    update_sql = f"UPDATE villagers SET {', '.join(update_fields)} WHERE id = ?"
                    update_values.append(db_villager['id'])
                    cursor.execute(update_sql, update_values)
                    updated_count += 1
                    
                    updates_made = []
                    if nookipedia_url:
                        updates_made.append("URL")
                    if house_exterior_url:
                        updates_made.append("exterior image")
                    if house_interior_url:
                        updates_made.append("interior image")
                    if photo_url:
                        updates_made.append("photo image")
                    if icon_url:
                        updates_made.append("icon image")
                    
                    logger.debug(f"Updated villager '{db_villager['name']}' with: {', '.join(updates_made)}")
        
        self.conn.commit()
        return updated_count, total_villagers


def main():
    """Update database with Nookipedia URLs from JSON files."""
    
    # Path to database (adjust as needed)
    db_path = project_root / "data" / "nooklook.db"  # Adjust this path as needed
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        print("Please check the database path and try again.")
        return 1
    
    # Path to JSON data directory
    data_dir = Path(__file__).parent / "data"
    
    if not data_dir.exists():
        print(f"Error: Data directory not found at {data_dir}")
        print("Please run fetch_urls.py first to download the data.")
        return 1
    
    print(f"Updating database: {db_path}")
    print(f"Using data from: {data_dir}")
    
    with NookipediaDBUpdater(str(db_path)) as updater:
        total_updated = 0
        
        # Update items (combining multiple Nookipedia categories into your custom "items" grouping)
        # Each tuple is (nookipedia_json_name, your_db_categories)
        item_category_mappings = [
            ("clothing", ["accessories", "bags", "bottoms", "clothing-other", "dress-up", "headwear", "shoes", "socks", "tops", "umbrellas"]),
            ("furniture", ["housewares", "miscellaneous", "wall-mounted", "ceiling-decor"]),
            ("tools", ["tools-goods"]),
            ("items", ["other", "music", "fencing", "interior-structures"]),  # Nookipedia's miscellaneous items
            ("interior", ["floors", "wallpaper", "rugs"]),  # Interior items
            ("photos", ["photos", "posters"]),  # Character photos and posters (Nookipedia combines these)
            ("gyroids", ["gyroids"]),  # Gyroids
        ]
        
        for json_name, db_categories in item_category_mappings:
            json_file = f"nookipedia_{json_name}_data.json"
            full_data = load_urls_from_json(json_file, str(data_dir))
            
            if full_data:
                try:
                    # Extract URLs from full data
                    urls_data = [{'name': item['name'], 'url': item['url']} for item in full_data]
                    updated, total = updater.update_items_urls(urls_data, db_categories)
                    print(f"Items ({json_name}): Updated {updated}/{total} entries")
                    total_updated += updated
                except Exception as e:
                    print(f"Error updating {json_name}: {e}")
        
        # Update events (if you have an events table, otherwise skip)
        try:
            full_data = load_urls_from_json("nookipedia_events_data.json", str(data_dir))
            if full_data:
                # Events might not map to your items table, so handle separately if needed
                print(f"Events: Loaded {len(full_data)} events (not mapped to items table)")
        except Exception as e:
            print(f"Note: Events not processed - {e}")
        
        # Update recipes
        full_data = load_urls_from_json("nookipedia_recipes_data.json", str(data_dir))
        if full_data:
            try:
                # Extract URLs from full data
                urls_data = [{'name': item['name'], 'url': item['url']} for item in full_data]
                updated, total = updater.update_recipes_urls(urls_data)
                print(f"Recipes: Updated {updated}/{total} entries")
                total_updated += updated
            except Exception as e:
                print(f"Error updating recipes: {e}")
        
        # Update critters
        critter_mappings = [
            ("fish", "fish"),
            ("bugs", "insect"),  # Your DB uses "insect" not "bug"
            ("sea_creatures", "sea")
        ]
        
        for json_name, db_kind in critter_mappings:
            json_file = f"nookipedia_{json_name}_data.json"
            full_data = load_urls_from_json(json_file, str(data_dir))
            
            if full_data:
                try:
                    # Extract URLs from full data
                    urls_data = [{'name': item['name'], 'url': item['url']} for item in full_data]
                    updated, total = updater.update_critters_urls(urls_data, db_kind)
                    print(f"Critters ({json_name}): Updated {updated}/{total} entries")
                    total_updated += updated
                except Exception as e:
                    print(f"Error updating {json_name}: {e}")
        
        # Update fossils
        full_data = load_urls_from_json("nookipedia_fossils_data.json", str(data_dir))
        if full_data:
            try:
                # Extract URLs from full data
                urls_data = [{'name': item['name'], 'url': item['url']} for item in full_data]
                updated, total = updater.update_fossils_urls(urls_data)
                print(f"Fossils: Updated {updated}/{total} entries")
                total_updated += updated
            except Exception as e:
                print(f"Error updating fossils: {e}")
        
        # Update artwork
        full_data = load_urls_from_json("nookipedia_art_data.json", str(data_dir))
        if full_data:
            try:
                # Extract URLs from full data
                urls_data = [{'name': item['name'], 'url': item['url']} for item in full_data]
                updated, total = updater.update_artwork_urls(urls_data)
                print(f"Artwork: Updated {updated}/{total} entries")
                total_updated += updated
            except Exception as e:
                print(f"Error updating artwork: {e}")
        
        # Update villagers
        full_data = load_urls_from_json("nookipedia_villagers_data.json", str(data_dir))
        if full_data:
            try:
                # Use full data instead of just URLs for villagers to get house images
                updated, total = updater.update_villagers_urls(full_data)
                print(f"Villagers: Updated {updated}/{total} entries")
                total_updated += updated
            except Exception as e:
                print(f"Error updating villagers: {e}")

    print(f"\nDatabase update completed!")
    print(f"Total entries updated: {total_updated}")
    
    # Note: All villager images (house, photo, icon) are now updated above from JSON data
    # No need for additional API calls since we have all the data in the JSON files
    print("\n✅ All villager images updated from JSON data (no API calls needed)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())