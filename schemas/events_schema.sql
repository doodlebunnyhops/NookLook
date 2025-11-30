-- =========================================================
-- EVENTS: seasonal events, holidays, special occasions
-- Primary source: Google Sheets CSV (seasons_and_events)
-- Secondary source: Nookipedia API (optional enrichment)
-- =========================================================

CREATE TABLE IF NOT EXISTS events (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    name                TEXT NOT NULL,              -- Event name (e.g., "Turkey Day", "Festivale")
    display_name        TEXT,                       -- Display Name from CSV (if different)
    event_type          TEXT NOT NULL,              -- 'Event', 'Nook Shopping', 'Recipes', 'Birthday', 'Calendar season'
    
    -- Unique identifier from source Google Sheets
    source_unique_id    TEXT UNIQUE,                -- "Unique Entry ID" from sheets
    internal_label      TEXT,                       -- Internal Label from CSV
    
    -- Timing info (not year-specific)
    date_varies_by_year INTEGER NOT NULL DEFAULT 0, -- 0=fixed, 1=varies (lunar, Easter-based, etc.)
    start_time          TEXT,                       -- e.g., "5:00 AM"
    end_time            TEXT,                       -- e.g., "5:00 AM" (next day)
    next_day_overlap    INTEGER DEFAULT 0,          -- 0/1 - event continues past midnight
    
    -- Metadata
    version_added       TEXT,
    version_last_updated TEXT,
    nookipedia_url      TEXT,                       -- URL to Nookipedia page (optional enrichment)
    
    -- Extra data
    extra_json          TEXT                        -- For any additional fields
);

CREATE INDEX IF NOT EXISTS idx_events_name ON events(name);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_source_unique_id ON events(source_unique_id);


-- =========================================================
-- EVENT_DATES: per-year, per-hemisphere date instances
-- Stores actual dates from CSV for each year/hemisphere
-- =========================================================

CREATE TABLE IF NOT EXISTS event_dates (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id            INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    year                INTEGER NOT NULL,           -- 2024, 2025, etc.
    hemisphere          TEXT NOT NULL DEFAULT 'NH', -- 'NH' or 'SH'
    start_date          TEXT NOT NULL,              -- ISO date: '2025-11-27'
    end_date            TEXT,                       -- NULL for single-day events
    date_string         TEXT,                       -- Original string from CSV (e.g., "Nov 27" or "May 22 – May 31")
    source              TEXT DEFAULT 'csv',         -- 'csv', 'nookipedia', 'calculated'
    
    UNIQUE(event_id, year, hemisphere)
);

CREATE INDEX IF NOT EXISTS idx_event_dates_event ON event_dates(event_id);
CREATE INDEX IF NOT EXISTS idx_event_dates_year ON event_dates(year);
CREATE INDEX IF NOT EXISTS idx_event_dates_hemisphere ON event_dates(hemisphere);
CREATE INDEX IF NOT EXISTS idx_event_dates_start ON event_dates(start_date);


-- =========================================================
-- VIEW: upcoming_events - convenient view for queries
-- =========================================================

CREATE VIEW IF NOT EXISTS upcoming_events AS
SELECT 
    e.name,
    e.display_name,
    e.event_type,
    ed.year,
    ed.hemisphere,
    ed.start_date,
    ed.end_date,
    e.start_time,
    e.end_time,
    e.nookipedia_url
FROM events e
JOIN event_dates ed ON e.id = ed.event_id
ORDER BY ed.start_date;

-- =========================================================
-- EVENT_ITEMS: items available during events (Nook Shopping)
-- Source: Nookipedia events page
-- =========================================================

CREATE TABLE IF NOT EXISTS event_items (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id            INTEGER REFERENCES events(id) ON DELETE CASCADE,
    event_name          TEXT NOT NULL,              -- Event name (for matching when event_id is NULL)
    item_name           TEXT NOT NULL,              -- Item name (e.g., 'Chocolate heart')
    nookipedia_url      TEXT,                       -- Nookipedia item page URL
    image_url           TEXT,                       -- Item icon image URL
    description         TEXT,                       -- Item/event description
    
    UNIQUE(event_name, item_name)
);

CREATE INDEX IF NOT EXISTS idx_event_items_event ON event_items(event_id);
CREATE INDEX IF NOT EXISTS idx_event_items_event_name ON event_items(event_name);
CREATE INDEX IF NOT EXISTS idx_event_items_item_name ON event_items(item_name);
