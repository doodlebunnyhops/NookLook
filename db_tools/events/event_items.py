#!/usr/bin/env python3
"""
Event Items Import

Imports event-related items (Nook Shopping items) from Nookipedia.
Links items to events in the database.

Source: Nookipedia events HTML page (parsed to JSON)
Does NOT create tables - uses schemas/events_schema.sql
"""

import sqlite3
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from html.parser import HTMLParser
from urllib.parse import unquote


class EventItemParser(HTMLParser):
    """Parse Nookipedia events HTML table to extract event-item mappings."""
    
    def __init__(self):
        super().__init__()
        self.events = []
        self.current_event = None
        self.current_cell = None
        self.in_table = False
        self.in_row = False
        self.cell_index = 0
        self.current_text = ""
        self.rowspan_event = None
        self.rowspan_count = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'table' and 'color-event' in attrs_dict.get('class', ''):
            self.in_table = True
            
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.cell_index = 0
            self.current_event = {
                'name': '',
                'wiki_url': None,
                'dates_2025': '',
                'items': [],
                'description': ''
            }
            if self.rowspan_count > 0:
                self.current_event['name'] = self.rowspan_event['name']
                self.current_event['wiki_url'] = self.rowspan_event['wiki_url']
                self.current_event['dates_2025'] = self.rowspan_event['dates_2025']
                self.rowspan_count -= 1
                self.cell_index = 2
            
        elif tag == 'td' and self.in_row:
            self.current_cell = self.cell_index
            self.current_text = ""
            if 'rowspan' in attrs_dict and self.cell_index == 0:
                self.rowspan_count = int(attrs_dict['rowspan']) - 1
            
        elif tag == 'th' and self.in_row:
            self.current_cell = -1
            
        elif tag == 'a' and self.current_cell is not None:
            href = attrs_dict.get('href', '')
            title = attrs_dict.get('title', '')
            
            if self.current_cell == 0 and href.startswith('/wiki/') and not href.startswith('/wiki/Item:'):
                self.current_event['wiki_url'] = f"https://nookipedia.com{href}"
                
            elif self.current_cell == 2 and '/wiki/Item:' in href:
                item_name = title.replace(' (New Horizons)', '') if title else unquote(href.split(':')[1].split('_(')[0])
                self.current_event['items'].append({
                    'name': item_name,
                    'wiki_url': f"https://nookipedia.com{href}",
                    'image_url': None
                })
                
        elif tag == 'img' and self.current_cell == 2:
            src = attrs_dict.get('src', '')
            if src and self.current_event['items']:
                if '/thumb/' in src:
                    parts = src.split('/thumb/')
                    if len(parts) == 2:
                        base = parts[0]
                        rest = parts[1].rsplit('/', 1)[0]
                        src = f"{base}/{rest}"
                self.current_event['items'][-1]['image_url'] = src
                
    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
            
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            if self.current_event and self.current_event['name']:
                self.events.append(self.current_event)
                if self.rowspan_count > 0:
                    pass
                else:
                    self.rowspan_event = self.current_event
            self.current_event = None
            
        elif tag == 'td' and self.current_cell is not None:
            text = self.current_text.strip()
            
            if self.current_cell == 0 and text:
                self.current_event['name'] = text
                if self.rowspan_count > 0:
                    self.rowspan_event = self.current_event
                    
            elif self.current_cell == 1:
                self.current_event['dates_2025'] = text
                
            elif self.current_cell == 5:
                self.current_event['description'] = text
                
            self.cell_index += 1
            self.current_cell = None
            self.current_text = ""
            
    def handle_data(self, data):
        if self.current_cell is not None:
            self.current_text += data


class EventItemsImporter:
    """
    Imports event items into the database.
    
    Parses HTML from Nookipedia events page to extract items.
    Links items to events in the database.
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize the importer.
        
        Args:
            db_path: Path to SQLite database
        """
        if db_path is None:
            db_path = self._resolve_path("data/nooklook.db")
        self.db_path = str(db_path)
        
        self.html_path = self._resolve_path("nookipedia/data/events.html")
        self.json_path = self._resolve_path("nookipedia/data/event_items.json")
        
        self.stats = {
            "items_imported": 0,
            "events_matched": 0,
            "items_linked": 0,
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
    
    def parse_html(self) -> List[Dict[str, Any]]:
        """
        Parse the events HTML file to extract event-item data.
        
        Returns:
            List of event dictionaries with items
        """
        if not self.html_path.exists():
            print(f"  HTML file not found: {self.html_path}")
            return []
        
        print(f"  Parsing HTML: {self.html_path}")
        
        with open(self.html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        parser = EventItemParser()
        parser.feed(html_content)
        
        # Filter and deduplicate
        seen = set()
        unique_events = []
        for event in parser.events:
            if event['name'] and event['items']:
                key = (event['name'], tuple(i['name'] for i in event['items']))
                if key not in seen:
                    seen.add(key)
                    unique_events.append(event)
        
        print(f"  Parsed {len(unique_events)} events with items")
        return unique_events
    
    def save_json(self, events: List[Dict[str, Any]]) -> None:
        """Save parsed events to JSON for caching."""
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        
        print(f"  Saved to {self.json_path}")
    
    def load_json(self) -> List[Dict[str, Any]]:
        """Load events from cached JSON file."""
        if not self.json_path.exists():
            return []
        
        with open(self.json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def import_items(self, force_parse: bool = False) -> Dict[str, int]:
        """
        Import event items into the database.
        
        Args:
            force_parse: If True, re-parse HTML even if JSON cache exists
            
        Returns:
            Stats dictionary with import results
        """
        print("\n" + "-" * 60)
        print("Importing Event Items")
        print("-" * 60)
        
        # Get event data
        events_data = []
        
        if force_parse or not self.json_path.exists():
            events_data = self.parse_html()
            if events_data:
                self.save_json(events_data)
        else:
            print(f"  Loading from cache: {self.json_path}")
            events_data = self.load_json()
            print(f"  Loaded {len(events_data)} events from cache")
        
        if not events_data:
            print("  No event items data available.")
            return self.stats
        
        # Connect to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Verify table exists (should be created by schema)
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='event_items'
            """)
            if not cursor.fetchone():
                raise RuntimeError(
                    "event_items table does not exist. "
                    "Run schema initialization first."
                )
            
            # Clear existing items for fresh import
            cursor.execute("DELETE FROM event_items")
            
            # Get events for matching
            cursor.execute("SELECT id, name FROM events")
            db_events = {name.lower(): id for id, name in cursor.fetchall()}
            
            # Import items
            events_matched = set()
            
            for event in events_data:
                event_name = event['name']
                description = event.get('description', '')
                
                # Match to database event
                event_id = self._match_event(event_name, db_events)
                
                if event_id:
                    events_matched.add(event_id)
                
                # Insert items
                for item in event['items']:
                    try:
                        cursor.execute("""
                            INSERT OR REPLACE INTO event_items 
                            (event_id, event_name, item_name, nookipedia_url, image_url, description)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            event_id,
                            event_name,
                            item['name'],
                            item.get('wiki_url'),
                            item.get('image_url'),
                            description
                        ))
                        self.stats["items_imported"] += 1
                        if event_id:
                            self.stats["items_linked"] += 1
                    except Exception as e:
                        print(f"  Error importing {item['name']}: {e}")
                        self.stats["errors"] += 1
            
            self.stats["events_matched"] = len(events_matched)
            conn.commit()
            
        finally:
            conn.close()
        
        print(f"\n  Items imported: {self.stats['items_imported']}")
        print(f"  Items linked to events: {self.stats['items_linked']}")
        print(f"  Events matched: {self.stats['events_matched']}")
        
        return self.stats
    
    def _match_event(self, event_name: str, db_events: Dict[str, int]) -> Optional[int]:
        """Match an event name to a database event ID."""
        event_name_lower = event_name.lower()
        
        # Direct match
        if event_name_lower in db_events:
            return db_events[event_name_lower]
        
        # Partial match
        for db_name, db_id in db_events.items():
            if event_name_lower in db_name or db_name in event_name_lower:
                return db_id
        
        return None
