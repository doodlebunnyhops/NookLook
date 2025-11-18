PRAGMA foreign_keys = ON;

-- =========================================================
-- ITEMS: base objects (furniture, clothing, tools, misc...)
-- =========================================================

CREATE TABLE items (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    name                TEXT NOT NULL,              -- In-game name
    category            TEXT NOT NULL,              -- 'misc', 'tools', 'tops', 'bottoms', 'dress-up', etc.

    -- Unique identifier from source Google Sheets
    source_unique_id    TEXT UNIQUE,                -- "Unique Entry ID" from sheets - true unique identifier
    
    -- Group identity across variants (Internal ID for misc/tools, ClothGroup ID for clothing, etc.)
    internal_group_id   INTEGER,                    -- Same for all variants of an item group

    -- Common item-level fields
    is_diy              INTEGER NOT NULL DEFAULT 0, -- 0/1
    buy_price           INTEGER,
    sell_price          INTEGER,
    hha_base            INTEGER,
    source              TEXT,
    catalog             TEXT,
    version_added       TEXT,
    tag                 TEXT,
    style1              TEXT,
    style2              TEXT,
    label_themes        TEXT,

    -- Image base
    filename            TEXT,                       -- Base filename from CSV
    image_url           TEXT,                       -- generic icon for the whole item group, set to default variant if needed
    nookipedia_url      TEXT,                       -- URL to Nookipedia page for this item

    -- Extra JSON for category-specific oddities if needed
    extra_json          TEXT
);

CREATE INDEX idx_items_name ON items(name);
CREATE INDEX idx_items_category ON items(category);
CREATE INDEX idx_items_internal_group ON items(internal_group_id);
CREATE INDEX idx_items_source_unique_id ON items(source_unique_id);


-- =========================================================
-- ITEM_VARIANTS: per-color/pattern variants and TI info
-- =========================================================

CREATE TABLE item_variants (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id                 INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,

    -- Unique identifier from source Google Sheets
    source_unique_id        TEXT UNIQUE,   -- "Unique Entry ID" from sheets for variants
    
    -- From "Variant ID" column (# or #_#) when present
    variant_id_raw          TEXT,          -- e.g. '3', '0_4', or NULL

    -- Parsed indices:
    -- For '3'         => primary_index = 3, secondary_index = NULL
    -- For '0_4'       => primary_index = 0, secondary_index = 4
    -- For clothing w/o Variant ID, you can use row order as primary_index (0,1,2,...)
    primary_index           INTEGER,
    secondary_index         INTEGER,

    -- Human-facing labels
    variation_label         TEXT,          -- Variation (primary color name)
    body_title              TEXT,          -- More verbose description of body
    pattern_label           TEXT,          -- Pattern name (secondary)
    pattern_title           TEXT,          -- More verbose description of pattern
    color1                  TEXT,
    color2                  TEXT,

    -- Customization flags (from Body Customize / Pattern Customize / Cyrus Customize)
    body_customizable       INTEGER NOT NULL DEFAULT 0,  -- 0/1
    pattern_customizable    INTEGER NOT NULL DEFAULT 0,  -- 0/1
    cyrus_customizable      INTEGER NOT NULL DEFAULT 0,  -- 0/1
    pattern_options         TEXT,                        -- Pattern Customize Options raw text

    -- Internal ID for this specific variant (used for hex on TI)
    internal_id             INTEGER,
    item_hex                TEXT,                        -- 4-char hex (e.g. '0E06')

    -- TI-specific customize mapping
    -- For 1D:  TI uses   !customize <item_hex> <ti_primary>
    -- For 2D:  TI uses   !customize <item_hex> <ti_primary> <ti_secondary>
    ti_primary              INTEGER,                     -- Mostly same as primary_index
    ti_secondary            INTEGER,                     -- NULL for 1D items; calculated value for 2D
    ti_customize_str        TEXT,                        -- E.g. '3' or '0 128'

    -- Optional: precomputed 16-char TI drop hex, e.g. '00000003000002E3'
    ti_full_hex             TEXT,

    -- Per-variant image handling
    image_url               TEXT,                        -- Fully resolved URL if you choose to store it
    image_url_alt           TEXT                         -- Alternate image URL if item has multiple images
);

CREATE INDEX idx_item_variants_item ON item_variants(item_id);
CREATE INDEX idx_item_variants_internal_id ON item_variants(internal_id);
CREATE INDEX idx_item_variants_variant_raw ON item_variants(variant_id_raw);
CREATE INDEX idx_item_variants_source_unique_id ON item_variants(source_unique_id);


-- =========================================================
-- RECIPES: DIY / cooking recipes
-- =========================================================

CREATE TABLE recipes (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    name                TEXT NOT NULL,
    
    -- Unique identifier from source Google Sheets
    source_unique_id    TEXT UNIQUE,       -- "Unique Entry ID" from sheets
    
    internal_id         INTEGER,           -- From Recipes CSV, if present
    product_item_id     INTEGER,           -- FK to items.id for the crafted item (nullable if you can't map it)
    category            TEXT,             -- E.g. 'Furniture', 'Wall-mounted', 'Food', etc.
    source              TEXT,             -- Where you get the recipe
    source_notes        TEXT,             -- Extra notes
    is_diy              INTEGER NOT NULL DEFAULT 1, -- Recipes are usually DIY, but keep flexible
    buy_price           INTEGER,
    sell_price          INTEGER,
    hha_base            INTEGER,
    version_added       TEXT,
    
    -- TI-related fields (calculated from internal_id)
    item_hex            TEXT,             -- 4-char hex (e.g. '0E06')
    ti_primary          INTEGER,          -- For TI customize commands (default 0)
    ti_secondary        INTEGER,          -- NULL for 1D items (recipes are typically 1D)
    ti_customize_str    TEXT,             -- E.g. '0' for most recipes
    ti_full_hex         TEXT,             -- 16-char TI drop hex
    
    image_url           TEXT,             -- Recipe card image or icon URL
    image_url_alt       TEXT,             -- Alternate image URL if applicable
    nookipedia_url      TEXT,             -- URL to Nookipedia page for this recipe
    extra_json          TEXT,             -- For future specialty fields
    FOREIGN KEY (product_item_id) REFERENCES items(id) ON DELETE SET NULL
);

CREATE INDEX idx_recipes_name ON recipes(name);
CREATE INDEX idx_recipes_category ON recipes(category);
CREATE INDEX idx_recipes_source_unique_id ON recipes(source_unique_id);


-- Ingredients for recipes
CREATE TABLE recipe_ingredients (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id           INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    item_id             INTEGER,          -- FK to items.id if you can map the ingredient to an item
    ingredient_name     TEXT NOT NULL,    -- fallback text if not mapped
    quantity            INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE SET NULL
);

CREATE INDEX idx_recipe_ingredients_recipe ON recipe_ingredients(recipe_id);
CREATE INDEX idx_recipe_ingredients_item ON recipe_ingredients(item_id);


-- =========================================================
-- CRITTERS: insects, fish, sea creatures (museum wing: bugs/fish/sea)
-- =========================================================

DROP TABLE IF EXISTS critters;

CREATE TABLE critters (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    name                    TEXT NOT NULL,
    kind                    TEXT NOT NULL,
    
    -- Unique identifier from source Google Sheets
    source_unique_id        TEXT UNIQUE,   -- "Unique Entry ID" from sheets
    
    internal_id             INTEGER,
    sell_price              INTEGER,
    
    -- TI-related fields (calculated from internal_id)
    item_hex                TEXT,             -- 4-char hex (e.g. '02E3')
    ti_primary              INTEGER,          -- For TI customize commands (default 0)
    ti_secondary            INTEGER,          -- NULL for 1D items (critters are typically 1D)
    ti_customize_str        TEXT,             -- E.g. '0' for most critters
    ti_full_hex             TEXT,             -- 16-char TI drop hex
    
    location                TEXT,
    shadow_size             TEXT,
    movement_speed          TEXT,
    catch_difficulty        TEXT,
    vision                  TEXT,
    total_catches_to_unlock TEXT,
    spawn_rates             TEXT,
    nh_jan                  TEXT,
    nh_feb                  TEXT,
    nh_mar                  TEXT,
    nh_apr                  TEXT,
    nh_may                  TEXT,
    nh_jun                  TEXT,
    nh_jul                  TEXT,
    nh_aug                  TEXT,
    nh_sep                  TEXT,
    nh_oct                  TEXT,
    nh_nov                  TEXT,
    nh_dec                  TEXT,
    sh_jan                  TEXT,
    sh_feb                  TEXT,
    sh_mar                  TEXT,
    sh_apr                  TEXT,
    sh_may                  TEXT,
    sh_jun                  TEXT,
    sh_jul                  TEXT,
    sh_aug                  TEXT,
    sh_sep                  TEXT,
    sh_oct                  TEXT,
    sh_nov                  TEXT,
    sh_dec                  TEXT,
    time_of_day             TEXT,
    weather                 TEXT,
    rarity                  TEXT,
    description             TEXT,
    catch_phrase            TEXT,
    hha_base_points         INTEGER,
    hha_category            TEXT,
    color1                  TEXT,
    color2                  TEXT,
    size                    TEXT,
    surface                 TEXT,
    icon_url                TEXT,
    critterpedia_url        TEXT,
    furniture_url           TEXT,
    nookipedia_url          TEXT,             -- URL to Nookipedia page for this critter
    source                  TEXT,
    version_added           TEXT,
    extra_json              TEXT
);

CREATE INDEX idx_critters_name ON critters(name);
CREATE INDEX idx_critters_kind ON critters(kind);
CREATE INDEX idx_critters_internal_id ON critters(internal_id);
CREATE INDEX idx_critters_source_unique_id ON critters(source_unique_id);


-- =========================================================
-- FOSSILS (museum wing: fossils)
-- =========================================================

DROP TABLE IF EXISTS fossils;

CREATE TABLE fossils (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    name                    TEXT NOT NULL,
    
    -- Unique identifier from source Google Sheets
    source_unique_id        TEXT UNIQUE,   -- "Unique Entry ID" from sheets
    
    image_url               TEXT,
    image_url_alt           TEXT,
    buy_price               INTEGER,
    sell_price              INTEGER,
    fossil_group            TEXT,
    description             TEXT,
    hha_base_points         INTEGER,
    color1                  TEXT,
    color2                  TEXT,
    size                    TEXT,
    source                  TEXT,
    museum                  TEXT,
    interact                TEXT,
    catalog                 TEXT,
    filename                TEXT,
    internal_id             INTEGER,
    
    -- TI-related fields (calculated from internal_id)
    item_hex                TEXT,             -- 4-char hex (e.g. '02E3')
    ti_primary              INTEGER,          -- For TI customize commands (default 0)
    ti_secondary            INTEGER,          -- NULL for 1D items (fossils are typically 1D)
    ti_customize_str        TEXT,             -- E.g. '0' for most fossils
    ti_full_hex             TEXT,             -- 16-char TI drop hex
    nookipedia_url          TEXT,             -- URL to Nookipedia page for this fossil
    
    extra_json              TEXT
);

CREATE INDEX idx_fossils_name ON fossils(name);
CREATE INDEX idx_fossils_internal_id ON fossils(internal_id);
CREATE INDEX idx_fossils_source_unique_id ON fossils(source_unique_id);


-- =========================================================
-- ARTWORK (museum wing: art)
-- =========================================================

DROP TABLE IF EXISTS artwork;

CREATE TABLE artwork (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    name                    TEXT NOT NULL,
    
    -- Unique identifier from source Google Sheets
    source_unique_id        TEXT UNIQUE,   -- "Unique Entry ID" from sheets
    
    image_url               TEXT,
    image_url_alt           TEXT,
    genuine                 INTEGER,
    art_category            TEXT,
    buy_price               INTEGER,
    sell_price              INTEGER,
    color1                  TEXT,
    color2                  TEXT,
    size                    TEXT,
    real_artwork_title      TEXT,
    artist                  TEXT,
    description             TEXT,
    source                  TEXT,
    source_notes            TEXT,
    hha_base_points         INTEGER,
    hha_concept1            TEXT,
    hha_concept2            TEXT,
    hha_series              TEXT,
    hha_set                 TEXT,
    interact                TEXT,
    tag                     TEXT,
    speaker_type            TEXT,
    lighting_type           TEXT,
    catalog                 TEXT,
    version_added           TEXT,
    unlocked                TEXT,
    filename                TEXT,
    internal_id             INTEGER,
    
    -- TI-related fields (calculated from internal_id)
    item_hex                TEXT,             -- 4-char hex (e.g. '02E3')
    ti_primary              INTEGER,          -- For TI customize commands (default 0)
    ti_secondary            INTEGER,          -- NULL for 1D items (artwork is typically 1D)
    ti_customize_str        TEXT,             -- E.g. '0' for most artwork
    ti_full_hex             TEXT,             -- 16-char TI drop hex
    nookipedia_url          TEXT,             -- URL to Nookipedia page for this artwork
    
    extra_json              TEXT
);

CREATE INDEX idx_artwork_name ON artwork(name);
CREATE INDEX idx_artwork_internal_id ON artwork(internal_id);
CREATE INDEX idx_artwork_source_unique_id ON artwork(source_unique_id);


-- =========================================================
-- MUSEUM_INDEX: unified view of "things you can donate"
-- =========================================================

DROP TABLE IF EXISTS museum_index;

CREATE TABLE museum_index (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    wing            TEXT NOT NULL,
    ref_table       TEXT NOT NULL,
    ref_id          INTEGER NOT NULL
);

CREATE INDEX idx_museum_index_name ON museum_index(name);
CREATE INDEX idx_museum_index_wing ON museum_index(wing);


-- =========================================================
-- VILLAGERS
-- =========================================================

CREATE TABLE villagers (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    name                TEXT NOT NULL,
    species             TEXT,
    gender              TEXT,
    personality         TEXT,
    subtype             TEXT,
    hobby               TEXT,
    birthday            TEXT,
    catchphrase         TEXT,
    favorite_song       TEXT,
    favorite_saying     TEXT,
    style1              TEXT,
    style2              TEXT,
    color1              TEXT,
    color2              TEXT,
    default_clothing    TEXT,
    default_umbrella    TEXT,
    wallpaper           TEXT,
    flooring            TEXT,
    furniture_list      TEXT,
    furniture_name_list TEXT,
    diy_workbench       TEXT,
    kitchen_equipment   TEXT,
    version_added       TEXT,
    name_color          TEXT,
    bubble_color        TEXT,
    filename            TEXT,
    
    -- Unique identifier from source Google Sheets
    source_unique_id    TEXT UNIQUE,   -- "Unique Entry ID" from sheets
    
    icon_image          TEXT,
    photo_image         TEXT,
    house_image         TEXT,
    nookipedia_url      TEXT             -- URL to Nookipedia page for this villager
);

CREATE INDEX idx_villagers_name ON villagers(name);
CREATE INDEX idx_villagers_species ON villagers(species);
CREATE INDEX idx_villagers_personality ON villagers(personality);
CREATE INDEX idx_villagers_source_unique_id ON villagers(source_unique_id);


-- =========================================================
-- SEARCH INDEX (FTS5): unified name search
-- =========================================================

CREATE VIRTUAL TABLE search_index USING fts5(
    name,               -- Display name as shown in-game
    category,           -- 'item', 'recipe', 'villager', 'critter', etc.
    subcategory,        -- More specific type within category
    ref_table,          -- Which table this refers to
    ref_id              -- The id in that table
);