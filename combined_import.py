#!/usr/bin/env python3
"""
Combined Import Script for ACNH Items
1. Imports comprehensive item data with variants from CSV (including image URLs)
2. Applies color-aware hex code matching for correct hex IDs
"""
import asyncio
import sys
import os

# Add the bot directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from import_csv_variants import VariantAwareCSVImporter
from import_hex_color_aware import ColorAwareHexImporter

async def combined_import():
    """Run the complete import process"""
    print("🚀 Starting Combined ACNH Import Process")
    print("=" * 60)
    
    # Step 1: Import CSV data with variants and comprehensive fields (including image URLs)
    print("\n📊 STEP 1: Importing CSV data with color variants and comprehensive fields")
    print("-" * 60)
    
    csv_importer = VariantAwareCSVImporter()
    # await csv_importer.import_csv_file("data/csv/housewares.csv", "Housewares")
    # await csv_importer.import_csv_file("data/csv/tops_v2.csv", "Tops")
    # await csv_importer.import_csv_file("data/csv/bottoms.csv", "Bottoms")
    await csv_importer.import_csv_file("data/csv/accessories.csv", "Accessories")
    await csv_importer.import_csv_file("data/csv/Dress-Up.csv", "Dress-Up")
    await csv_importer.import_csv_file("data/csv/Headwear.csv", "Headwear")

    
    print(f"\n✅ CSV import complete!")
    print(f"   Imported items with comprehensive data including image URLs")
    
    # Step 2: Apply color-aware hex code matching
    print("\n🎯 STEP 2: Applying color-aware hex code matching")
    print("-" * 60)
    
    hex_importer = ColorAwareHexImporter()
    await hex_importer.import_hex_codes("data/csv/acnh_hex_codes.csv")
    
    print(f"\n✅ Hex code import complete!")
    print(f"   Applied color-specific hex codes to variants")
    
    # Step 3: Verification
    print("\n🔍 STEP 3: Verification")
    print("-" * 60)
    
    from bot.repos.database import Database
    db = Database("data/acnh_cache.db")
    
    # Check total items
    total_result = await db.execute_query("SELECT COUNT(*) as count FROM acnh_items")
    total_items = total_result[0]['count']
    
    # Check items with hex codes
    hex_result = await db.execute_query("SELECT COUNT(*) as count FROM acnh_items WHERE hex_id IS NOT NULL AND hex_id != ''")
    hex_items = hex_result[0]['count']
    
    # Check items with image URLs
    image_result = await db.execute_query("SELECT COUNT(*) as count FROM acnh_items WHERE image_url IS NOT NULL AND image_url != ''")
    image_items = image_result[0]['count']
    
    # Check pleather pants specifically
    pleather_result = await db.execute_query("""
        SELECT name, color_variant, hex_id, image_url 
        FROM acnh_items 
        WHERE name LIKE '%pleather pants%' 
        ORDER BY name
    """)
    
    print(f"📦 Total items in database: {total_items}")
    print(f"🎯 Items with hex codes: {hex_items} ({hex_items/total_items*100:.1f}%)")
    print(f"🖼️  Items with image URLs: {image_items} ({image_items/total_items*100:.1f}%)")
    
    print(f"\n🩱 Pleather Pants Verification:")
    for item in pleather_result:
        color = f" ({item['color_variant']})" if item['color_variant'] else ""
        hex_display = item['hex_id'] if item['hex_id'] else "NO HEX"
        image_display = "✅" if item['image_url'] else "❌"
        print(f"   {item['name']}{color}: {hex_display} | Image: {image_display}")
    
    print("\n🎉 Combined import process complete!")
    print("=" * 60)
    print("Your Discord bot now has:")
    print("  ✅ Comprehensive item data from CSV")
    print("  ✅ Color-specific hex codes for variants")
    print("  ✅ Image URLs for display")
    print("  ✅ All the fields you wanted (sell price, HHA points, size, etc.)")

if __name__ == "__main__":
    asyncio.run(combined_import())