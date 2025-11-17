#!/usr/bin/env python3
"""Test script to verify clothing variants are properly loaded"""

import asyncio
import sys
from bot.services.acnh_service import NooklookService

async def test_pleather_pants():
    """Test that pleather pants has all variants"""
    service = NooklookService()
    await service.init_database()
    
    # Search for pleather pants
    results = await service.search_all("pleather pants", category_filter="item")
    
    if not results:
        print("❌ ERROR: No results found for 'pleather pants'")
        return False
    
    if len(results) > 1:
        print(f"❌ ERROR: Found {len(results)} items, expected 1 base item with variants")
        for r in results:
            print(f"   - {r.name} (ID: {r.id})")
        return False
    
    item = results[0]
    print(f"✅ Found item: {item.name}")
    print(f"   Category: {item.category}")
    print(f"   Internal Group ID: {item.internal_group_id}")
    print(f"   Variants: {len(item.variants)}")
    
    if len(item.variants) != 6:
        print(f"❌ ERROR: Expected 6 variants, found {len(item.variants)}")
        return False
    
    print("\n   Variant details:")
    for v in item.variants:
        print(f"   - {v.variation_label or 'N/A'}: {v.color1} (Internal ID: {v.internal_id}, Hex: {v.item_hex})")
    
    # Test that the to_discord_embed method works
    embed = item.to_discord_embed()
    print(f"\n✅ Discord embed generated successfully")
    print(f"   Title: {embed.title}")
    print(f"   Has thumbnail: {embed.thumbnail.url if embed.thumbnail else 'No'}")
    
    return True

async def test_other_clothing():
    """Test a few more clothing items"""
    service = NooklookService()
    await service.init_database()
    
    test_items = [
        ("acid-washed jeans", 2),  # Should have 2 variants
        ("cut-pleather skirt", 4),  # Should have 4 variants
        ("pleather flare skirt", 8)  # Should have 8 variants
    ]
    
    for item_name, expected_count in test_items:
        results = await service.search_all(item_name, category_filter="item")
        
        if not results:
            print(f"❌ ERROR: No results found for '{item_name}'")
            return False
        
        if len(results) > 1:
            print(f"❌ ERROR: Found {len(results)} items for '{item_name}', expected 1")
            return False
        
        item = results[0]
        if len(item.variants) != expected_count:
            print(f"❌ ERROR: {item_name} has {len(item.variants)} variants, expected {expected_count}")
            return False
        
        print(f"✅ {item_name}: {len(item.variants)} variants")
    
    return True

async def main():
    """Run all tests"""
    print("="*60)
    print("Testing Clothing Variant Fix")
    print("="*60)
    
    print("\nTest 1: Pleather Pants Variants")
    print("-"*60)
    test1 = await test_pleather_pants()
    
    print("\n" + "="*60)
    print("Test 2: Other Clothing Items")
    print("-"*60)
    test2 = await test_other_clothing()
    
    print("\n" + "="*60)
    if test1 and test2:
        print("✅ ALL TESTS PASSED")
        print("="*60)
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
