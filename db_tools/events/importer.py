#!/usr/bin/env python3
"""
Core Event Importer

Imports event data from Google Sheets API (required).
This is the baseline source of truth for event data.

Does NOT create tables - uses schemas/events_schema.sql
"""

import sqlite3
import re
from datetime import date
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import os
import requests
import urllib.parse
from dotenv import load_dotenv


class EventImporter:
    """
    Imports ACNH events from Google Sheets API.
    
    Google Sheets is the required primary source of truth.
    Tables must be created via schemas/events_schema.sql before import.
    """
    
    # Month name to number mapping
    MONTHS = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    
    def __init__(self, db_path: str = None):
        """
        Initialize the importer.
        
        Args:
            db_path: Path to SQLite database. Defaults to data/nooklook.db
        """
        load_dotenv()
        
        # Resolve database path
        if db_path is None:
            db_path = self._resolve_path("data/nooklook.db")
        self.db_path = str(db_path)
        
        # Ensure data directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Google Sheets API configuration (required)
        self.google_sheet_url = os.getenv('GOOGLE_SHEET')
        self.gcp_api_key = os.getenv('GCP_API_KEY')
        
        if not self.google_sheet_url or not self.gcp_api_key:
            raise ValueError(
                "GOOGLE_SHEET and GCP_API_KEY environment variables are required. "
                "Google Sheets is the primary source of truth for event data."
            )
        
        # Stats tracking
        self.stats = {
            "events_imported": 0,
            "events_updated": 0,
            "dates_imported": 0,
            "errors": 0
        }
    
    def _resolve_path(self, relative_path: str) -> Path:
        """Resolve a path relative to the project root."""
        # Try from current directory
        path = Path(relative_path)
        if path.exists() or path.parent.exists():
            return path
        
        # Try from parent (if running from db_tools/)
        parent_path = Path("..") / relative_path
        if parent_path.exists() or parent_path.parent.exists():
            return parent_path
        
        # Try from db_tools/events/
        grandparent_path = Path("../..") / relative_path
        if grandparent_path.exists() or grandparent_path.parent.exists():
            return grandparent_path
        
        return path
    
    def _extract_spreadsheet_id(self, url: str) -> str:
        """Extract spreadsheet ID from Google Sheets URL."""
        if '/spreadsheets/' in url:
            if '/spreadsheets/d/' in url:
                return url.split('/spreadsheets/d/')[1].split('/')[0]
            else:
                return url.split('/spreadsheets/')[1].split('/')[0].split('?')[0]
        raise ValueError(f"Invalid Google Sheets URL: {url}")
    
    def _fetch_sheet_data(self, sheet_name: str) -> List[Dict[str, Any]]:
        """
        Fetch data from a Google Sheet tab.
        
        Args:
            sheet_name: Name of the sheet tab to fetch
            
        Returns:
            List of row dictionaries with header keys
        """
        spreadsheet_id = self._extract_spreadsheet_id(self.google_sheet_url)
        encoded_sheet = urllib.parse.quote(sheet_name)
        
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_sheet}"
        params = {'key': self.gcp_api_key}
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        values = data.get('values', [])
        
        if not values:
            return []
        
        # First row is headers
        headers = values[0]
        rows = []
        
        for row in values[1:]:
            # Pad row to match headers length
            while len(row) < len(headers):
                row.append('')
            row_dict = dict(zip(headers, row))
            rows.append(row_dict)
        
        return rows
    
    def _get_year_columns(self, headers: List[str]) -> Dict[int, Dict[str, str]]:
        """
        Extract year columns from headers.
        
        Returns:
            Dict of year -> {'NH': column_name, 'SH': column_name}
        """
        year_cols = {}
        year_pattern = re.compile(r'^(\d{4})\s+(NH|SH)$')
        
        for header in headers:
            match = year_pattern.match(header)
            if match:
                year = int(match.group(1))
                hemisphere = match.group(2)
                
                if year not in year_cols:
                    year_cols[year] = {'NH': None, 'SH': None}
                year_cols[year][hemisphere] = header
        
        return year_cols
    
    def _parse_date_string(self, date_str: str, year: int) -> Tuple[Optional[date], Optional[date]]:
        """
        Parse a date string like 'Nov 27' or 'May 22 – May 31' into date objects.
        
        Returns:
            Tuple of (start_date, end_date). end_date is None for single-day events.
        """
        if not date_str or date_str.strip() == '':
            return None, None
        
        # Clean up the string
        date_str = date_str.strip()
        date_str = date_str.replace('–', '-').replace('—', '-')  # Normalize dashes
        
        # Check if it's a range
        if ' - ' in date_str:
            parts = date_str.split(' - ')
            if len(parts) == 2:
                start = self._parse_single_date(parts[0].strip(), year)
                end = self._parse_single_date(parts[1].strip(), year)
                
                # Handle year wrap (e.g., Dec 1 - Feb 29)
                if start and end and end < start:
                    # Need to parse the end date for the next year
                    # Can't just use replace() as it may fail for Feb 29 in non-leap years
                    end = self._parse_single_date(parts[1].strip(), year + 1)
                
                return start, end
        
        # Single date
        single = self._parse_single_date(date_str, year)
        return single, None
    
    def _parse_single_date(self, date_str: str, year: int) -> Optional[date]:
        """Parse a single date like 'Nov 27' or 'May 22'."""
        import calendar
        
        match = re.match(r'(\w+)\s+(\d+)', date_str.strip())
        if match:
            month_str = match.group(1)
            day = int(match.group(2))
            
            if month_str in self.MONTHS:
                month = self.MONTHS[month_str]
                
                # Get the last valid day for this month/year
                _, last_day = calendar.monthrange(year, month)
                
                # Clamp day to valid range for this month
                if day > last_day:
                    day = last_day
                
                try:
                    return date(year, month, day)
                except ValueError:
                    # Shouldn't happen after clamping, but just in case
                    return None
        return None
    
    def init_schema(self, schema_path: str = None) -> None:
        """
        Initialize events tables from schema file.
        
        Args:
            schema_path: Path to schema SQL file. Defaults to schemas/events_schema.sql
        """
        if schema_path is None:
            schema_path = self._resolve_path("schemas/events_schema.sql")
        else:
            schema_path = Path(schema_path)
        
        if not schema_path.exists():
            raise FileNotFoundError(
                f"Schema file not found: {schema_path}. "
                "Tables must be created via schemas/events_schema.sql"
            )
        
        print(f"Initializing schema from: {schema_path}")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        conn = sqlite3.connect(self.db_path)
        try:
            conn.executescript(schema_sql)
            conn.commit()
            print("  Schema initialized successfully")
        except sqlite3.Error as e:
            print(f"  Error executing schema: {e}")
            raise
        finally:
            conn.close()
    
    def import_events(self, sheet_name: str = "Seasons and Events") -> Dict[str, int]:
        """
        Import events from Google Sheets API.
        
        Args:
            sheet_name: Name of the sheet tab to import from
            
        Returns:
            Stats dictionary with import results
        """
        print("\n" + "=" * 60)
        print("ACNH Events Import (Google Sheets)")
        print("=" * 60)
        
        # Fetch data from Google Sheets
        print(f"Fetching events from Google Sheets API...")
        rows = self._fetch_sheet_data(sheet_name)
        print(f"  Fetched {len(rows)} rows from '{sheet_name}'")
        
        if not rows:
            print("  No event data found!")
            return self.stats
        
        # Initialize schema
        self.init_schema()
        
        # Get headers to find year columns
        headers = list(rows[0].keys()) if rows else []
        year_cols = self._get_year_columns(headers)
        
        if year_cols:
            print(f"  Found {len(year_cols)} years of data: {min(year_cols.keys())}-{max(year_cols.keys())}")
        
        # Import events
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for row in rows:
                try:
                    result = self._import_event(cursor, row, year_cols)
                    if result == 'inserted':
                        self.stats["events_imported"] += 1
                    elif result == 'updated':
                        self.stats["events_updated"] += 1
                except Exception as e:
                    event_name = row.get('Name', 'unknown')
                    print(f"  Error importing event '{event_name}': {e}")
                    self.stats["errors"] += 1
            
            conn.commit()
        finally:
            conn.close()
        
        print(f"\nImport complete:")
        print(f"  Events imported: {self.stats['events_imported']}")
        print(f"  Events updated: {self.stats['events_updated']}")
        print(f"  Dates imported: {self.stats['dates_imported']}")
        print(f"  Errors: {self.stats['errors']}")
        
        return self.stats
    
    def _import_event(self, cursor: sqlite3.Cursor, row: Dict[str, Any],
                      year_cols: Dict[int, Dict[str, str]]) -> Optional[str]:
        """
        Import a single event and its dates.
        
        Returns:
            'inserted', 'updated', or None
        """
        name = row.get('Name', '').strip()
        if not name:
            return None
        
        # Map CSV Type to event_type
        csv_type = row.get('Type', '').strip()
        event_type = csv_type if csv_type else 'Event'
        
        # Check if event already exists
        source_id = row.get('Unique Entry ID', '')
        cursor.execute("SELECT id FROM events WHERE source_unique_id = ?", (source_id,))
        existing = cursor.fetchone()
        
        if existing:
            event_id = existing[0]
            # Update existing event
            cursor.execute("""
                UPDATE events SET
                    name = ?,
                    display_name = ?,
                    event_type = ?,
                    internal_label = ?,
                    date_varies_by_year = ?,
                    start_time = ?,
                    end_time = ?,
                    next_day_overlap = ?,
                    version_added = ?,
                    version_last_updated = ?
                WHERE id = ?
            """, (
                name,
                row.get('Display Name', ''),
                event_type,
                row.get('Internal Label', ''),
                1 if row.get('Date Varies by Year', 'No') == 'Yes' else 0,
                row.get('Start Time', ''),
                row.get('End Time', ''),
                1 if row.get('Next Day Overlap', 'No') == 'Yes' else 0,
                row.get('Version Added', ''),
                row.get('Version Last Updated', ''),
                event_id
            ))
            result = 'updated'
        else:
            # Insert new event
            cursor.execute("""
                INSERT INTO events (
                    name, display_name, event_type, source_unique_id, internal_label,
                    date_varies_by_year, start_time, end_time, next_day_overlap,
                    version_added, version_last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                row.get('Display Name', ''),
                event_type,
                source_id,
                row.get('Internal Label', ''),
                1 if row.get('Date Varies by Year', 'No') == 'Yes' else 0,
                row.get('Start Time', ''),
                row.get('End Time', ''),
                1 if row.get('Next Day Overlap', 'No') == 'Yes' else 0,
                row.get('Version Added', ''),
                row.get('Version Last Updated', '')
            ))
            event_id = cursor.lastrowid
            result = 'inserted'
        
        # Import dates for each year/hemisphere
        for year, hemi_cols in year_cols.items():
            for hemisphere, col_name in hemi_cols.items():
                if col_name and col_name in row:
                    date_str = row[col_name].strip()
                    if date_str:
                        self._import_event_date(cursor, event_id, year, hemisphere, date_str)
        
        return result
    
    def _import_event_date(self, cursor: sqlite3.Cursor, event_id: int,
                           year: int, hemisphere: str, date_str: str) -> None:
        """Import a single event date entry."""
        start_date, end_date = self._parse_date_string(date_str, year)
        
        if not start_date:
            return
        
        start_iso = start_date.isoformat()
        end_iso = end_date.isoformat() if end_date else None
        
        # Upsert the date
        cursor.execute("""
            INSERT INTO event_dates (event_id, year, hemisphere, start_date, end_date, date_string, source)
            VALUES (?, ?, ?, ?, ?, ?, 'csv')
            ON CONFLICT(event_id, year, hemisphere) DO UPDATE SET
                start_date = excluded.start_date,
                end_date = excluded.end_date,
                date_string = excluded.date_string,
                source = 'csv'
        """, (event_id, year, hemisphere, start_iso, end_iso, date_str))
        
        self.stats["dates_imported"] += 1
