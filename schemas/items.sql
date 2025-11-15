-- Main items table based on Nookipedia API response
CREATE TABLE IF NOT EXISTS acnh_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    name_normalized TEXT NOT NULL,
    url TEXT,                        -- Nookipedia wiki URL
    category TEXT,                   -- e.g. "Housewares"
    item_series TEXT,               -- e.g. "Antique"
    item_set TEXT,                  -- Item set name
    hha_category TEXT,              -- HHA category (e.g. "Dresser")
    hha_base INTEGER,               -- HHA base points
    tag TEXT,                       -- Item tag
    lucky BOOLEAN DEFAULT FALSE,    -- Lucky item flag
    lucky_season TEXT,              -- Lucky season if applicable
    sell_price INTEGER,             -- Sell price in Bells
    variation_total INTEGER DEFAULT 0,
    pattern_total INTEGER DEFAULT 0,
    customizable BOOLEAN DEFAULT FALSE,
    custom_kits INTEGER DEFAULT 0,
    custom_kit_type TEXT,
    custom_body_part TEXT,
    custom_pattern_part TEXT,
    grid_width INTEGER,             -- Grid width
    grid_length INTEGER,            -- Grid length
    height REAL,                    -- Item height
    door_decor BOOLEAN DEFAULT FALSE,
    version_added TEXT,             -- Game version when added
    unlocked BOOLEAN DEFAULT TRUE,
    notes TEXT,
    image_filename TEXT,            -- Image filename for URL generation
    image_url TEXT,                 -- Full image URL
    last_fetched TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Item themes (many-to-many relationship)
CREATE TABLE IF NOT EXISTS acnh_item_themes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    theme TEXT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES acnh_items (id) ON DELETE CASCADE
);

-- Item functions (many-to-many relationship)
CREATE TABLE IF NOT EXISTS acnh_item_functions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    function_name TEXT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES acnh_items (id) ON DELETE CASCADE
);

-- Item buy prices (can have multiple currencies)
CREATE TABLE IF NOT EXISTS acnh_item_buy_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    price INTEGER NOT NULL,
    currency TEXT NOT NULL,         -- e.g. "Bells", "Nook Miles"
    FOREIGN KEY (item_id) REFERENCES acnh_items (id) ON DELETE CASCADE
);

-- Item availability sources
CREATE TABLE IF NOT EXISTS acnh_item_availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    source TEXT NOT NULL,           -- e.g. "Nook's Cranny (Upgraded)"
    note TEXT,                      -- Additional notes about availability
    FOREIGN KEY (item_id) REFERENCES acnh_items (id) ON DELETE CASCADE
);

-- Item variations
CREATE TABLE IF NOT EXISTS acnh_item_variations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    variation TEXT NOT NULL,        -- e.g. "Brown"
    pattern TEXT,                   -- Pattern name if applicable
    image_url TEXT,                 -- Image URL for this variation
    FOREIGN KEY (item_id) REFERENCES acnh_items (id) ON DELETE CASCADE
);

-- Variation colors (many-to-many for each variation)
CREATE TABLE IF NOT EXISTS acnh_variation_colors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    variation_id INTEGER NOT NULL,
    color TEXT NOT NULL,            -- e.g. "Aqua", "Brown"
    FOREIGN KEY (variation_id) REFERENCES acnh_item_variations (id) ON DELETE CASCADE
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_acnh_items_name_norm ON acnh_items (name_normalized);
CREATE INDEX IF NOT EXISTS idx_acnh_items_category ON acnh_items (category);
CREATE INDEX IF NOT EXISTS idx_acnh_items_series ON acnh_items (item_series);
CREATE INDEX IF NOT EXISTS idx_acnh_items_tag ON acnh_items (tag);
CREATE INDEX IF NOT EXISTS idx_acnh_item_themes_item_id ON acnh_item_themes (item_id);
CREATE INDEX IF NOT EXISTS idx_acnh_item_themes_theme ON acnh_item_themes (theme);
CREATE INDEX IF NOT EXISTS idx_acnh_item_functions_item_id ON acnh_item_functions (item_id);
CREATE INDEX IF NOT EXISTS idx_acnh_item_buy_prices_item_id ON acnh_item_buy_prices (item_id);
CREATE INDEX IF NOT EXISTS idx_acnh_item_availability_item_id ON acnh_item_availability (item_id);
CREATE INDEX IF NOT EXISTS idx_acnh_item_variations_item_id ON acnh_item_variations (item_id);
CREATE INDEX IF NOT EXISTS idx_acnh_variation_colors_variation_id ON acnh_variation_colors (variation_id);
