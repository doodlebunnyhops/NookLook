-- =========================================================
-- TRANSLATIONS SCHEMA
-- Run this after nooklook_schema.sql
-- =========================================================

PRAGMA foreign_keys = ON;

-- =========================================================
-- USER_SETTINGS: per-user preferences (language, hemisphere)
-- =========================================================

CREATE TABLE IF NOT EXISTS user_settings (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id             TEXT NOT NULL UNIQUE,       -- Discord user ID
    preferred_language  TEXT NOT NULL DEFAULT 'en', -- Language code (en, ja, zh, ko, fr, de, es, it, nl, ru)
    hemisphere          TEXT DEFAULT 'north',       -- 'north' or 'south' for critter availability
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_settings_user_id ON user_settings(user_id);

-- Trigger to update timestamp
CREATE TRIGGER IF NOT EXISTS update_user_settings_timestamp 
    AFTER UPDATE ON user_settings
    FOR EACH ROW
BEGIN
    UPDATE user_settings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- =========================================================
-- ITEM_TRANSLATIONS: localized names for items
-- Links to existing tables via ref_table + ref_id
-- =========================================================

CREATE TABLE IF NOT EXISTS item_translations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ref_table       TEXT NOT NULL,          -- 'items', 'villagers', etc.
    ref_id          INTEGER NOT NULL,       -- ID in the referenced table
    en_name         TEXT NOT NULL,          -- English (canonical, for matching)
    ja_name         TEXT,                   -- Japanese 日本語
    zh_name         TEXT,                   -- Chinese (Simplified) 简体中文
    ko_name         TEXT,                   -- Korean 한국어
    fr_name         TEXT,                   -- French Français
    de_name         TEXT,                   -- German Deutsch
    es_name         TEXT,                   -- Spanish Español
    it_name         TEXT,                   -- Italian Italiano
    nl_name         TEXT,                   -- Dutch Nederlands
    ru_name         TEXT,                   -- Russian Русский
    UNIQUE(ref_table, ref_id)
);

-- Indexes for searching in each language
CREATE INDEX IF NOT EXISTS idx_translations_ref ON item_translations(ref_table, ref_id);
CREATE INDEX IF NOT EXISTS idx_translations_en ON item_translations(en_name);
CREATE INDEX IF NOT EXISTS idx_translations_ja ON item_translations(ja_name);
CREATE INDEX IF NOT EXISTS idx_translations_zh ON item_translations(zh_name);
CREATE INDEX IF NOT EXISTS idx_translations_ko ON item_translations(ko_name);
CREATE INDEX IF NOT EXISTS idx_translations_fr ON item_translations(fr_name);
CREATE INDEX IF NOT EXISTS idx_translations_de ON item_translations(de_name);
CREATE INDEX IF NOT EXISTS idx_translations_es ON item_translations(es_name);
CREATE INDEX IF NOT EXISTS idx_translations_it ON item_translations(it_name);
CREATE INDEX IF NOT EXISTS idx_translations_nl ON item_translations(nl_name);
CREATE INDEX IF NOT EXISTS idx_translations_ru ON item_translations(ru_name);
