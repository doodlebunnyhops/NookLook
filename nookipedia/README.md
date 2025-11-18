# Nookipedia Integration

This module provides tools to fetch URLs from the Nookipedia API and integrate them into your NookLook database.

[API Documentation](https://api.nookipedia.com/doc)

## Setup

1. **Get a Nookipedia API key** from [https://forms.gle/wLwtXLerKhfDrRLY8](https://forms.gle/wLwtXLerKhfDrRLY8)

2. **Set your API key** in a .env file:

    ```
    NOOKIPEDIA_API=YOUR-API-KEY
    ```

## Usage

### Option 1: Run Everything at Once

```bash
python nookipedia/sync_urls.py
```

This will:
1. Fetch **complete data** for all categories from Nookipedia (not just URLs!)
2. Save them as JSON files in `nookipedia/data/`
3. Update the database with the Nookipedia URLs (extracted from the full data)

### Option 2: Run Steps Separately

**Step 1: Fetch URLs from Nookipedia**
```bash
python nookipedia/fetch_urls.py
```

This fetches data for:
- Clothing items
- Furniture
- Tools
- Miscellaneous items (materials, fruits, etc.)
- Interior items (flooring, wallpaper, rugs)
- Photos and posters
- Gyroids
- Events (seasonal events, etc.)
- DIY recipes
- Fish
- Bugs
- Sea creatures
- Fossils
- Artwork
- Villagers

**Step 2: Update Database**
```bash
python nookipedia/update_db.py
```

This matches the fetched URLs with items in the database by name and updates the `nookipedia_url` field.

## Files Created

After running `fetch_urls.py`, you'll have JSON files with **full data** in `nookipedia/data/`:
- `nookipedia_clothing_data.json` - Complete clothing data including variants, colors, styles, etc.
- `nookipedia_furniture_data.json` - Complete furniture data including categories, colors, etc.
- `nookipedia_tools_data.json` - Complete tools data
- `nookipedia_items_data.json` - Complete miscellaneous items data (materials, fruits, etc.)
- `nookipedia_interior_data.json` - Complete interior items (flooring, wallpaper, rugs)
- `nookipedia_photos_data.json` - Complete character photos and posters data
- `nookipedia_gyroids_data.json` - Complete gyroid data
- `nookipedia_events_data.json` - Complete events data (seasonal events, etc.)
- `nookipedia_recipes_data.json` - Complete recipe data including materials and sources
- `nookipedia_fish_data.json` - Complete fish data including seasons, times, locations
- `nookipedia_bugs_data.json` - Complete bug data including seasons, times, locations  
- `nookipedia_sea_creatures_data.json` - Complete sea creature data
- `nookipedia_fossils_data.json` - Complete fossil data
- `nookipedia_art_data.json` - Complete artwork data including authenticity info
- `nookipedia_villagers_data.json` - Complete villager data including personality, species, etc.

## Rate Limiting

The client includes a 1.5-second rate limit between API requests to be respectful to the Nookipedia API. This means fetching all categories takes about 15-20 seconds.

## Database Schema Changes

The following tables have been updated with a `nookipedia_url` field:
- `items`
- `recipes`
- `critters`
- `fossils`
- `artwork`
- `villagers`

## Troubleshooting

- **"No data received"**: Check your API key and internet connection
- **Low match rates**: The name matching is case-insensitive but exact. You may need to add fuzzy matching logic if your item names don't match Nookipedia's exactly

