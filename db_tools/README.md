# Database Tools

This directory contains all database import, export, and management utilities for the ACNH Lookup Bot.

## Scripts

### Core Import Scripts

- **`import_all_datasets.py`** - Main dataset importer with Google Sheets API integration
  - Smart import (only imports when data changes)
  - Supports all ACNH data categories (items, villagers, recipes, etc.)
  - Automatic duplicate detection and handling
  - Progress tracking and statistics

- **`run_full_import.py`** - Entry point for initial database setup
  - Runs smart import (recommended for most uses)
  - Creates database from scratch if needed
  - Good for first-time setup

- **`force_import.py`** - Force import regardless of modification times
  - Bypasses smart checking
  - Useful for troubleshooting or when you know data changed
  - Always imports everything

### Testing and Development

- **`mock_sheet_update.py`** - Testing utility for simulating data updates
  - Creates fake "sheet updated" scenarios for testing
  - Includes duplicate detection checks
  - Useful for testing bot update logic

## Usage

### First-time setup:
```bash
# From project root
python db_tools/run_full_import.py

# Or from within db_tools directory
cd db_tools
python run_full_import.py
```

### Force refresh:
```bash
# From project root
python db_tools/force_import.py

# Or from within db_tools directory
cd db_tools  
python force_import.py
```

### Test update detection:
```bash
# From project root
python db_tools/mock_sheet_update.py --full-test

# Or from within db_tools directory
cd db_tools
python mock_sheet_update.py --full-test
```

## Database Location

The database is created at `data/nooklook.db` in the project root. This keeps all data files organized in a dedicated directory.

## Requirements

All scripts require:
- Google Sheets API key in `.env` file
- Required Python packages from `requirements.txt`
- Internet connection for Google Sheets access

## Integration

The bot (`bot/bot.py`) automatically uses `ACNHDatasetImporter` for:
- 6-hour periodic update checks
- Automatic database backups before updates
- Smart import only when data has changed