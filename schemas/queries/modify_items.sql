-- Insert and update queries for ACNH items

-- Insert or replace a complete item (main table only - use repository methods for full data)
INSERT OR REPLACE INTO acnh_items 
(name, name_normalized, url, category, item_series, sell_price, last_fetched)
VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP);

-- Update item category
UPDATE acnh_items 
SET category = ?, last_fetched = CURRENT_TIMESTAMP
WHERE id = ?;

-- Update item sell price
UPDATE acnh_items 
SET sell_price = ?, last_fetched = CURRENT_TIMESTAMP
WHERE id = ?;

-- Update item series
UPDATE acnh_items 
SET item_series = ?, last_fetched = CURRENT_TIMESTAMP
WHERE id = ?;

-- Delete old cached items (older than 30 days)
DELETE FROM acnh_items 
WHERE last_fetched < datetime('now', '-30 days');

-- Clear all cache (with cascading deletes for related tables)
DELETE FROM acnh_items;

-- Delete specific item by name (with cascading deletes)
DELETE FROM acnh_items 
WHERE name_normalized = ?;