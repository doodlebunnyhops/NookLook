#!/usr/bin/env python3
"""
Nookipedia URL Enrichment

Enriches events with Nookipedia URLs using the Nookipedia API client.
This is optional supplementary data - Google Sheets remains the source of truth.

Uses nookipedia/client.py for API access if NOOKIPEDIA_API token exists.
Falls back to cached JSON data if API is unavailable.
"""

import sqlite3
import json
import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv


class NookipediaEnricher:
    """
    Enriches events with Nookipedia wiki URLs.
    
    Uses the Nookipedia API client if available, otherwise falls back to cached JSON.
    This is optional enrichment - the bot works without Nookipedia data.
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize the enricher.
        
        Args:
            db_path: Path to SQLite database
        """
        load_dotenv()
        
        if db_path is None:
            db_path = self._resolve_path("data/nooklook.db")
        self.db_path = str(db_path)
        
        # Nookipedia API token (optional)
        self.api_key = os.getenv('NOOKIPEDIA_API')
        
        # Paths
        self.json_cache_path = self._resolve_path("nookipedia/data/nookipedia_events_data.json")
        
        # Stats
        self.stats = {
            "urls_added": 0,
            "urls_from_api": 0,
            "urls_from_cache": 0,
            "parent_matches": 0,
            "errors": 0
        }
    
    def _resolve_path(self, relative_path: str) -> Path:
        """Resolve a path relative to the project root."""
        path = Path(relative_path)
        if path.exists():
            return path
        
        for parent in [Path(".."), Path("../.."), Path("../../..")]:
            test_path = parent / relative_path
            if test_path.exists():
                return test_path
        
        return path
    
    def _get_nookipedia_client(self):
        """Get Nookipedia API client if token exists."""
        if not self.api_key:
            return None
        
        try:
            # Add nookipedia module to path if needed
            nookipedia_path = self._resolve_path("nookipedia")
            if nookipedia_path.exists() and str(nookipedia_path.parent) not in sys.path:
                sys.path.insert(0, str(nookipedia_path.parent))
            
            from nookipedia.client import NookipediaClient
            return NookipediaClient(self.api_key)
        except ImportError as e:
            print(f"  Warning: Could not import NookipediaClient: {e}")
            return None
    
    def _fetch_events_from_api(self) -> List[Dict[str, Any]]:
        """Fetch events data from Nookipedia API."""
        client = self._get_nookipedia_client()
        if not client:
            return []
        
        print("  Fetching events from Nookipedia API...")
        try:
            events = client.get_events_urls()
            print(f"  Fetched {len(events)} events from API")
            
            # Cache the data for future use
            self._cache_events_data(events)
            
            return events
        except Exception as e:
            print(f"  Error fetching from API: {e}")
            return []
    
    def _cache_events_data(self, events: List[Dict[str, Any]]) -> None:
        """Cache events data to JSON file."""
        try:
            cache_path = self._resolve_path("nookipedia/data")
            cache_path.mkdir(parents=True, exist_ok=True)
            
            output_file = cache_path / "nookipedia_events_data.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=2, ensure_ascii=False)
            print(f"  Cached {len(events)} events to {output_file}")
        except Exception as e:
            print(f"  Warning: Could not cache events data: {e}")
    
    def _load_events_from_cache(self) -> List[Dict[str, Any]]:
        """Load events data from cached JSON file."""
        if not self.json_cache_path.exists():
            print(f"  No cached data found at {self.json_cache_path}")
            return []
        
        print(f"  Loading events from cache: {self.json_cache_path}")
        with open(self.json_cache_path, 'r', encoding='utf-8') as f:
            events = json.load(f)
        print(f"  Loaded {len(events)} events from cache")
        return events
    
    def _normalize_event_name(self, name: str) -> str:
        """
        Normalize an event name for matching.
        
        Removes hemisphere indicators, numbered occurrences, common suffixes.
        """
        normalized = name.lower().strip()
        
        # Remove hemisphere indicators
        normalized = re.sub(r'\s*\(northern hemisphere\)', '', normalized)
        normalized = re.sub(r'\s*\(southern hemisphere\)', '', normalized)
        
        # Remove numbered occurrences like (1), (2)
        normalized = re.sub(r'\s*\(\d+\)', '', normalized)
        
        # Remove common suffixes
        suffixes = [
            ' nook shopping event begins', ' nook shopping event ends',
            ' nook shopping event', ' recipes become available',
            ' become available', ' preparation days begin',
            ' preparation days end', ' begins', ' ends',
            ' days before', ' days after', ' weeks before',
            ' (shopping)', ' petals', ' shells',
            ' and pine cones', ' leaves',
        ]
        for suffix in suffixes:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)]
        
        # Remove remaining parenthetical content
        normalized = re.sub(r'\s*\([^)]*\)\s*$', '', normalized)
        
        # Normalize hyphens and spaces
        normalized = normalized.replace('-', ' ')
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized.strip()
    
    def _build_nookipedia_mapping(self, events: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Build a mapping from normalized event names to Nookipedia data.
        
        Returns:
            Dict of normalized_name -> {'url': str, 'dates': [...]}
        """
        mapping = {}
        
        for event in events:
            event_name = event.get('event', '')
            event_type = event.get('type', '')
            url = event.get('url', '')
            event_date = event.get('date', '')
            
            # Skip birthdays - handled separately
            if event_type == 'Birthday':
                continue
            
            if not event_name or not url:
                continue
            
            base_name = self._normalize_event_name(event_name)
            
            # Determine hemisphere from event name
            hemisphere = 'NH'
            if 'southern hemisphere' in event_name.lower():
                hemisphere = 'SH'
            
            # Extract year from date
            year = None
            if event_date and len(event_date) >= 4:
                try:
                    year = int(event_date[:4])
                except ValueError:
                    pass
            
            if base_name not in mapping:
                mapping[base_name] = {'url': url, 'dates': []}
            
            if year and event_date:
                mapping[base_name]['dates'].append({
                    'year': year,
                    'hemisphere': hemisphere,
                    'date': event_date
                })
        
        return mapping
    
    def enrich_events(self, use_api: bool = True) -> Dict[str, int]:
        """
        Enrich events with Nookipedia URLs.
        
        Args:
            use_api: If True and API token exists, fetch from API. Otherwise use cache.
            
        Returns:
            Stats dictionary with enrichment results
        """
        print("\n" + "-" * 60)
        print("Enriching with Nookipedia URLs (optional)")
        print("-" * 60)
        
        # Try API first if available and requested
        events_data = []
        if use_api and self.api_key:
            events_data = self._fetch_events_from_api()
            if events_data:
                self.stats["urls_from_api"] = len(events_data)
        
        # Fall back to cache
        if not events_data:
            events_data = self._load_events_from_cache()
            if events_data:
                self.stats["urls_from_cache"] = len(events_data)
        
        if not events_data:
            print("  No Nookipedia data available. Skipping enrichment.")
            return self.stats
        
        # Build mapping
        nookipedia_mapping = self._build_nookipedia_mapping(events_data)
        print(f"  Built mapping with {len(nookipedia_mapping)} unique events")
        
        # Connect to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # First pass: direct name matching
            updated = self._match_by_name(cursor, nookipedia_mapping)
            
            # Second pass: parent-to-child URL inheritance
            parent_updated = self._inherit_parent_urls(cursor)
            
            conn.commit()
            
            print(f"\n  URLs added: {self.stats['urls_added']}")
            print(f"  Parent matches: {self.stats['parent_matches']}")
            
        finally:
            conn.close()
        
        return self.stats
    
    def _match_by_name(self, cursor: sqlite3.Cursor, 
                       nookipedia_mapping: Dict[str, Dict[str, Any]]) -> int:
        """Match events by normalized name."""
        cursor.execute("""
            SELECT id, name FROM events 
            WHERE nookipedia_url IS NULL
        """)
        events = cursor.fetchall()
        
        updated = 0
        for event_id, db_name in events:
            normalized_db = self._normalize_event_name(db_name)
            
            # Try to find a match
            matched_url = None
            for nook_name, nook_data in nookipedia_mapping.items():
                if (normalized_db == nook_name or
                    normalized_db in nook_name or
                    nook_name in normalized_db):
                    matched_url = nook_data['url']
                    break
            
            if matched_url:
                cursor.execute(
                    "UPDATE events SET nookipedia_url = ? WHERE id = ?",
                    (matched_url, event_id)
                )
                updated += 1
                self.stats["urls_added"] += 1
        
        return updated
    
    def _inherit_parent_urls(self, cursor: sqlite3.Cursor) -> int:
        """
        Inherit URLs from parent events to sub-events.
        
        e.g., "Toy Day (weeks before)" gets URL from "Toy Day"
        """
        print("  Matching sub-events to parent URLs...")
        
        cursor.execute("""
            SELECT id, name FROM events 
            WHERE nookipedia_url IS NULL
        """)
        remaining = cursor.fetchall()
        
        updated = 0
        for event_id, db_name in remaining:
            # Extract base name by removing parenthetical suffixes
            base_name = re.sub(r'\s*\([^)]*\)\s*$', '', db_name).strip()
            
            if base_name != db_name:
                # This is a sub-event, try to find parent URL
                cursor.execute(
                    "SELECT nookipedia_url FROM events WHERE name = ? AND nookipedia_url IS NOT NULL",
                    (base_name,)
                )
                parent = cursor.fetchone()
                if parent and parent[0]:
                    cursor.execute(
                        "UPDATE events SET nookipedia_url = ? WHERE id = ?",
                        (parent[0], event_id)
                    )
                    updated += 1
                    self.stats["urls_added"] += 1
                    self.stats["parent_matches"] += 1
        
        return updated
