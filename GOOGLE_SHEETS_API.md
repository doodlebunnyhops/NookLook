# Google Sheets API Integration

## Overview

The ACNH dataset importer pulls data directly from the comprehensive Animal Crossing: New Horizons dataset maintained by the ACNH Community (ACNH Sheets Discord). The bot automatically checks for source updates every 6 hours and refreshes the database when changes are detected. This provides several benefits:

- **Always up-to-date data**: Bot automatically syncs with source data every 6 hours
- **Automatic updates**: No manual intervention required for data updates
- **Reduced maintenance**: Bot handles all data synchronization automatically
- **Real-time data**: Changes in the community sheet are detected and imported within 6 hours
- **Community-driven**: Data sourced from the dedicated ACNH Sheets Discord community

## Quick Start Guide

### 1. Get a Google Cloud API Key

You'll need a Google Cloud Platform API key to access the Google Sheets API:

1. **Go to Google Cloud Console**: Visit [console.cloud.google.com](https://console.cloud.google.com)
2. **Create or Select Project**: Create a new project or select an existing one
3. **Enable Required APIs**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API" and click "Enable"
   - Search for "Google Drive API" and click "Enable" (needed for sheet modification timestamps)
4. **Create API Key**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key (keep it secure!)
5. **Restrict API Key** (Recommended):
   - Click on your API key to edit it
   - Under "API restrictions", select "Restrict key"
   - Choose both "Google Sheets API" AND "Google Drive API" from the list
   - Save your changes

### 2. Setup Environment Variables

Copy the example environment file and configure your API key:

```bash
# Copy the example file
cp .env.example .env
```

Then edit `.env` and add your API key:

```env
GOOGLE_SHEETS_API_KEY=your_google_cloud_api_key_here
```

Replace `your_google_cloud_api_key_here` with the API key you created in step 1.

> **Note**: The `.env.example` file contains all available configuration options including Discord bot settings.

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install requests python-dotenv
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

### 4. Run the Import

Create your ACNH database with a single command:

```bash
python run_full_import.py
```

This will:
- Connect to the ACNH Community Google Sheet
- Download all dataset categories (items, critters, villagers, etc.)
- Extract image URLs from Google Sheets IMAGE formulas
- Build TI (Treasure Island) codes for all items
- Create a complete `nooklook.db` SQLite database
- Populate search and museum indexes

**That's it!** You now have a complete ACNH database ready to use.

## Data Source

The data comes from the comprehensive ACNH dataset maintained by the **ACNH Sheets Discord community**. This community-driven project provides one of the most complete and up-to-date Animal Crossing: New Horizons databases available.

**Google Sheet**: [ACNH Community Dataset](https://docs.google.com/spreadsheets/d/13d_LAJPlxMa_DubPTuirkIV4DERBMXbrWQsmSh8ReK4)  
**Discord Community**: [Join ACNH Sheets Discord](https://discord.gg/8jNFHxG)

### Sheet Categories

The bot automatically imports data from all these Google Sheet categories:

| Category | Google Sheet Title | Database Table |
|----------|-------------------|----------------|
| Accessories | `Accessories` | `items` |
| Bags | `Bags` | `items` |
| Bottoms | `Bottoms` | `items` |
| Ceiling Decor | `Ceiling Decor` | `items` |
| Clothing Other | `Clothing Other` | `items` |
| Dress-Up | `Dress-Up` | `items` |
| Fencing | `Fencing` | `items` |
| Floors | `Floors` | `items` |
| Gyroids | `Gyroids` | `items` |
| Headwear | `Headwear` | `items` |
| Housewares | `Housewares` | `items` |
| Interior Structures | `Interior Structures` | `items` |
| Miscellaneous | `Miscellaneous` | `items` |
| Music | `Music` | `items` |
| Other | `Other` | `items` |
| Photos | `Photos` | `items` |
| Posters | `Posters` | `items` |
| Rugs | `Rugs` | `items` |
| Shoes | `Shoes` | `items` |
| Socks | `Socks` | `items` |
| Tools/Goods | `Tools/Goods` | `items` |
| Tops | `Tops` | `items` |
| Umbrellas | `Umbrellas` | `items` |
| Wall-mounted | `Wall-mounted` | `items` |
| Wallpaper | `Wallpaper` | `items` |
| Fish | `Fish` | `critters` |
| Insects | `Insects` | `critters` |
| Sea Creatures | `Sea Creatures` | `critters` |
| Fossils | `Fossils` | `fossils` |
| Artwork | `Artwork` | `artwork` |
| Villagers | `Villagers` | `villagers` |
| Recipes | `Recipes` | `recipes` |

## Automatic Updates

Once the bot is running, it automatically:
- **Checks for updates every 6 hours**: The bot monitors the Google Sheet for changes
- **Detects modifications**: Uses Google Drive API to check sheet modification timestamps
- **Imports new data**: Automatically updates the database when changes are found
- **Logs update activity**: All update checks and imports are logged for monitoring

## What Gets Imported

Running `python run_full_import.py` creates a complete database with:

### 📦 **Items & Variants** (24,000+ records)
- All furniture, clothing, and decorative items
- Multiple variants and customization options
- Complete image URLs for icons and storage displays
- TI (Treasure Island) codes for item spawning

### 🐟 **Critters** (200 records)  
- Fish, insects, and sea creatures
- Seasonal availability and spawn conditions
- Catch difficulty and location data
- Museum donation tracking

### 🏛️ **Museum Collections** (143 records)
- Fossils with scientific information
- Artwork with authenticity data
- Complete museum wing organization

### 🏘️ **Villagers** (413 records)
- All villager personalities and species  
- Birthdays, catchphrases, and preferences
- House layouts and default items

### 🔨 **DIY Recipes** (924 records)
- All craftable recipes and materials
- Ingredient lists and quantities
- Source information and availability

### 🔍 **Search & Organization**
- Full-text search index across all content
- Museum donation tracking system
- Category-based organization

## Usage Examples

### Initial Database Setup
```bash
# One-time setup: Create initial database
python run_full_import.py
```

### Start the Bot (with Auto-Updates)
```bash
# Start the Discord bot with automatic 6-hour update checks
python start_bot.py
```

### Manual Force Update
```bash
# Force immediate update (bypass 6-hour timer)
python force_import.py
```

## Expected Output

A successful import will show:

```
Starting full ACNH dataset import from Google Sheets API
======================================================================
Importer initialized successfully

Initializing database...
Database initialized successfully

Starting dataset import...
Processing sheet 'Accessories'
   Successfully fetched 280 rows
   Processed 280 rows for accessories

[... processing all categories ...]

============================================================
FINAL IMPORT STATISTICS
============================================================
Total Processed:  26,240
Total Imported:   11,543
Total Skipped:    0
Total Errors:     0

Import completed successfully with no errors!

Database created: nooklook.db
```

## Troubleshooting

### ❌ API Key Issues
**Problem**: `ERROR: GOOGLE_SHEETS_API_KEY not found` or `401 Unauthorized`

**Solutions**:
- Check your `.env` file exists and contains `GOOGLE_SHEETS_API_KEY=your_key`
- Verify your API key is valid in [Google Cloud Console](https://console.cloud.google.com)
- Ensure both Google Sheets API AND Google Drive API are enabled for your project
- Make sure API key isn't restricted from accessing Google Sheets API or Google Drive API
- Both APIs are required: Sheets API for data access, Drive API for modification timestamps

### ❌ Import Errors
**Problem**: `404 Client Error` or `403 Forbidden`

**Solutions**:
- Check your internet connection
- Verify the Google Sheet is publicly accessible
- Try running again (temporary network issues)

### ❌ Database Issues  
**Problem**: `SQLite error` or `no such column`

**Solutions**:
- Delete existing `nooklook.db` file and re-run import
- Check that you're using the latest version of the schema files

### ❌ Missing Dependencies
**Problem**: `ModuleNotFoundError: No module named 'requests'`

**Solution**:
```bash
pip install -r requirements.txt
```

## Support

- **ACNH Community**: [Join the ACNH Sheets Discord](https://discord.gg/8jNFHxG) for dataset questions and updates
- **Technical Issues**: Check the GitHub repository for bug reports and feature requests
- **API Documentation**: [Google Sheets API v4 Reference](https://developers.google.com/sheets/api/reference/rest)

## Credits

Special thanks to the **ACNH Sheets Discord community** ([discord.gg/8jNFHxG](https://discord.gg/8jNFHxG)) for maintaining the comprehensive Animal Crossing dataset that powers this tool. Their dedication to keeping the data accurate and up-to-date makes projects like this possible.