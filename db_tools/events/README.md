# ACNH Events Import System

A structured process for importing and enriching Animal Crossing: New Horizons event data.

## Overview

This module handles:
- **Event import** from Google Sheets (source of truth)
- **URL enrichment** from Nookipedia API (optional)
- **Manual URL mappings** for edge cases (zodiac, blooming seasons, etc.)
- **Event items import** from Nookipedia HTML data

## Requirements

### Required
- Google Sheets API access
- Environment variables:
  - `GOOGLE_SHEET` - Sheet ID containing "Seasons and Events" tab
  - `GCP_API_KEY` - Google Cloud API key

### Optional (for enrichment)
- Nookipedia API access
- Environment variable:
  - `NOOKIPEDIA_API` - Nookipedia API token

## Usage

```bash
# Full import (events + enrichment + items)
python -m db_tools.events

# Google Sheets only (skip Nookipedia enrichment)
python -m db_tools.events --no-enrich

# Skip event items
python -m db_tools.events --no-items

# Only import event items (assumes events exist)
python -m db_tools.events --items-only

# Check current database state
python -m db_tools.events --check

# Custom database path
python -m db_tools.events --db path/to/database.db
```

## Module Structure

```
db_tools/events/
├── __init__.py          # Package exports
├── __main__.py          # CLI entry point
├── importer.py          # EventImporter - Google Sheets import
├── nookipedia_enricher.py  # NookipediaEnricher - URL enrichment
├── event_items.py       # EventItemsImporter - Event items
├── url_mappings.py      # Manual URL mappings for edge cases
└── README.md            # This file
```

## Classes

### EventImporter
Core importer that reads from Google Sheets and writes to the database.
- Initializes schema from `schemas/events_schema.sql`
- Parses event dates and handles year columns (2000-2060)
- Upserts events and event_dates tables

### NookipediaEnricher
Optional enricher that adds Nookipedia URLs to events.
- Uses `nookipedia/client.py` if API token exists
- Falls back to cached JSON data otherwise
- Caches API results for future runs

### EventItemsImporter
Imports event items from Nookipedia HTML.
- Parses `nookipedia/data/events.html`
- Links items to events by name matching
- Caches parsed data to JSON

## Database Schema

The schema is defined in `schemas/events_schema.sql`. This module does NOT create tables directly - it uses the schema file.

### Tables
- `events` - Main events table with Nookipedia URLs
- `event_dates` - Year-specific dates for each event
- `event_items` - Items associated with events

## URL Mappings

Some events require manual URL mappings because:
- Zodiac seasons link to zodiac fragment item pages
- Blooming seasons link to bush start pages
- Some events have non-standard wiki page names

These are defined in `url_mappings.py`.

## Data Flow

```
Google Sheets (source of truth)
        │
        ▼
    EventImporter
        │
        ▼
   events + event_dates tables
        │
        ▼
   NookipediaEnricher (optional)
        │
        ▼
   Manual URL Mappings
        │
        ▼
   EventItemsImporter (optional)
        │
        ▼
   event_items table
```

## Examples

### Programmatic Usage

```python
from db_tools.events import EventImporter, NookipediaEnricher, EventItemsImporter

# Import from Google Sheets
importer = EventImporter(db_path="data/nooklook.db")
stats = importer.import_events()

# Enrich with Nookipedia URLs
enricher = NookipediaEnricher(db_path="data/nooklook.db")
enricher.enrich_events()

# Import event items
items = EventItemsImporter(db_path="data/nooklook.db")
items.import_items()
```

### Check Status

```python
# Check which events are missing URLs
python -m db_tools.events --check
```

## Notes

- Google Sheets is the **source of truth** for event data
- Nookipedia provides supplementary URLs and item data
- The module is designed to be idempotent - running it multiple times is safe
- Scripts do NOT create tables - use the schema file with `init_schema()`
