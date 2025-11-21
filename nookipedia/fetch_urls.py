#!/usr/bin/env python3
"""
Fetch URLs from Nookipedia API for all New Horizons categories.
This script will fetch all the URLs and save them as JSON files.
"""

import os
import sys
from pathlib import Path

# Try to load dotenv, but don't fail if not available
try:
    from dotenv import load_dotenv
    load_dotenv()  # This will automatically look for .env file
except ImportError:
    print("Note: python-dotenv not installed. Install with: pip install python-dotenv")
    print("Falling back to system environment variables only.")

# Add the project root to the path so we can import our modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from nookipedia.client import NookipediaClient, save_urls_to_json

def main():
    """Fetch all URLs from Nookipedia and save as JSON files."""
    
    # Get API key from environment variable
    api_key = os.getenv('NOOKIPEDIA_API')
    if not api_key:
        print("Error: NOOKIPEDIA_API environment variable not set")
        print("Please either:")
        print("1. Set it as a system environment variable")
        print("2. Create a .env file in the project root with: NOOKIPEDIA_API=your-key-here")
        return 1
    
    print("Initializing Nookipedia client with 1.5 second rate limit...")
    client = NookipediaClient(api_key, rate_limit_seconds=1.5)
    
    # Create data directory
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Define all the categories to fetch (matching Nookipedia's structure)
    categories = [
        ('clothing', client.get_clothing_urls),
        ('furniture', client.get_furniture_urls), 
        ('tools', client.get_tools_urls),
        ('items', client.get_items_urls),  # Miscellaneous items
        ('interior', client.get_interior_urls),  # Flooring, wallpaper, rugs
        ('photos', client.get_photos_urls),  # Character photos and posters
        ('gyroids', client.get_gyroids_urls),
        ('events', client.get_events_urls),
        ('recipes', client.get_recipes_urls),
        ('fish', client.get_fish_urls),
        ('bugs', client.get_bugs_urls),
        ('sea_creatures', client.get_sea_creatures_urls),
        ('fossils', client.get_fossils_urls),
        ('art', client.get_art_urls),
        ('villagers', client.get_villagers_urls)
    ]
    
    print(f"Fetching data for {len(categories)} categories...")
    
    for category_name, fetch_function in categories:
        try:
            print(f"\\nFetching {category_name}...")
            data = fetch_function()
            
            if data:
                filename = f"nookipedia_{category_name}_data.json"
                save_urls_to_json(data, filename, str(data_dir))
                print(f"✓ Saved {len(data)} {category_name} items")
            else:
                print(f"✗ No data received for {category_name}")
                
        except Exception as e:
            print(f"✗ Error fetching {category_name}: {e}")
            continue
    
    print("\\n🎉 Data fetching completed!")
    print(f"Check the {data_dir} directory for JSON files.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())