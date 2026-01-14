"""
ACNH Events Import System

A structured process for creating event-related tables and importing data.

Primary source: Google Sheets API (required)
Secondary source: Nookipedia API (optional enrichment)

Usage:
    python -m db_tools.events              # Full import with Nookipedia if available
    python -m db_tools.events --no-enrich  # Import from Google Sheets only

Guidelines:
    - Scripts do not create tables/indexes - they use schemas/events_schema.sql
    - Google Sheets API is required for baseline data
    - Nookipedia API enrichment is optional (uses nookipedia/client.py if token exists)
    - Data from Google Sheets is the source of truth
"""

from .importer import EventImporter
from .nookipedia_enricher import NookipediaEnricher
from .event_items import EventItemsImporter
from .url_mappings import apply_manual_url_mappings

__all__ = [
    'EventImporter',
    'NookipediaEnricher', 
    'EventItemsImporter',
    'apply_manual_url_mappings',
]
