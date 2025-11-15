-- Common select queries for ACNH items

-- Get item by exact normalized name with basic info
SELECT * FROM acnh_items 
WHERE name_normalized = ?;

-- Search items by name pattern
SELECT * FROM acnh_items 
WHERE name_normalized LIKE ? 
ORDER BY name
LIMIT 10;

-- Get all item names for fuzzy matching
SELECT name, name_normalized FROM acnh_items 
ORDER BY name;

-- Get items by category
SELECT * FROM acnh_items 
WHERE category = ?
ORDER BY name;

-- Get items by series
SELECT * FROM acnh_items 
WHERE item_series = ?
ORDER BY name;

-- Get items by theme
SELECT DISTINCT i.* FROM acnh_items i
JOIN acnh_item_themes t ON i.id = t.item_id
WHERE t.theme = ?
ORDER BY i.name;

-- Get items by price range
SELECT * FROM acnh_items 
WHERE sell_price BETWEEN ? AND ?
ORDER BY sell_price;

-- Get customizable items
SELECT * FROM acnh_items 
WHERE customizable = TRUE
ORDER BY name;

-- Get items with variations
SELECT * FROM acnh_items 
WHERE variation_total > 0
ORDER BY variation_total DESC, name;

-- Get recently cached items
SELECT * FROM acnh_items 
ORDER BY last_fetched DESC
LIMIT 20;

-- Count items by category
SELECT category, COUNT(*) as count 
FROM acnh_items 
GROUP BY category 
ORDER BY count DESC;

-- Count items by series
SELECT item_series, COUNT(*) as count 
FROM acnh_items 
WHERE item_series IS NOT NULL AND item_series != ''
GROUP BY item_series 
ORDER BY count DESC;

-- Most expensive items
SELECT name, sell_price FROM acnh_items 
WHERE sell_price IS NOT NULL
ORDER BY sell_price DESC
LIMIT 10;