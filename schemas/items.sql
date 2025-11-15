-- Main items table for ACNH with comprehensive data from community spreadsheets
CREATE TABLE IF NOT EXISTS acnh_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    name_normalized TEXT NOT NULL,
    category TEXT,                   -- e.g. "Bottoms", "Housewares", etc.
    color_variant TEXT,             -- Color variant (e.g. "Brown", "Red")
    hex_id TEXT,                    -- Hex ID from ACNH data
    
    -- Display and gameplay data
    sell_price INTEGER,             -- Sell price in Bells
    hha_base INTEGER,               -- HHA base points
    hha_category TEXT,              -- HHA category
    grid_width INTEGER,             -- Grid width (size)
    grid_length INTEGER,            -- Grid length (size)
    
    -- Series and classification
    item_series TEXT,               -- e.g. "Antique", "Cute"
    item_set TEXT,                  -- Item set name
    tag TEXT,                       -- Item tag
    
    -- Customization
    customizable BOOLEAN DEFAULT FALSE,
    custom_kits INTEGER DEFAULT 0,
    custom_kit_type TEXT,
    
    -- Additional metadata from CSV imports
    interact TEXT,                  -- Interaction type
    outdoor TEXT,                   -- Outdoor usability
    speaker_type TEXT,              -- Speaker type for audio items
    lighting_type TEXT,             -- Lighting type
    catalog TEXT,                   -- Catalog availability
    version_added TEXT,             -- Game version when added
    unlocked TEXT,                  -- Unlock requirements
    filename TEXT,                  -- Original filename
    variant_id TEXT,                -- Variant ID from spreadsheet
    internal_id TEXT,               -- Internal game ID
    unique_entry_id TEXT,           -- Unique entry ID
    
    -- Images
    image_filename TEXT,            -- Image filename for URL generation
    image_url TEXT,                 -- Full image URL
    
    -- Metadata
    notes TEXT,
    last_fetched TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_acnh_items_name_norm ON acnh_items (name_normalized);
CREATE INDEX IF NOT EXISTS idx_acnh_items_category ON acnh_items (category);
