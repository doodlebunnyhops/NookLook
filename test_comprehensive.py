#!/usr/bin/env python3
"""Comprehensive test for all clothing categories"""

import asyncio
import sys
from bot.services.acnh_service import NooklookService

async def test_clothing_categories():
    """Test various clothing items across different categories"""
    service = NooklookService()
    await service.init_database()
    
    # Test items from different clothing categories
    test_cases = [
        # (item_name, expected_variants, category)
        ("pleather pants", 6, "bottoms"),
        ("athletic jacket", 6, "tops"),
        ("beret", 6, "headwear"),
        ("flannel shirt", 5, "tops"),
        ("balloon hat", 4, "headwear"),
    ]
    
    all_passed = True
    
    for item_name, expected_variants, expected_category in test_cases:
        results = await service.search_all(item_name, category_filter="item")
        
        # Filter to exact name match
        results = [r for r in results if r.name.lower() == item_name.lower()]
        
        if not results:
            print(f"❌ {item_name}: Not found")
            all_passed = False
            continue
        
        if len(results) > 1:
            print(f"❌ {item_name}: Found {len(results)} separate items (should be 1 with variants)")
            all_passed = False
            continue
        
        item = results[0]
        
        if item.category.lower() != expected_category.lower():
            print(f"⚠️  {item_name}: Category is '{item.category}', expected '{expected_category}'")
        
        if len(item.variants) != expected_variants:
            print(f"❌ {item_name}: Has {len(item.variants)} variants, expected {expected_variants}")
            all_passed = False
            continue
        
        print(f"✅ {item_name}: {len(item.variants)} variants ({item.category})")
    
    return all_passed

async def test_search_index():
    """Test that search index properly returns unique items"""
    service = NooklookService()
    await service.init_database()
    
    # Search for "pleather" which should return items, not individual variants
    results = await service.search_all("pleather", category_filter="item")
    
    # Count items named "pleather pants"
    pleather_pants_items = [r for r in results if r.name == "pleather pants"]
    
    if len(pleather_pants_items) > 1:
        print(f"❌ Search returned {len(pleather_pants_items)} 'pleather pants' items (should be 1)")
        return False
    
    if len(pleather_pants_items) == 0:
        print("❌ Search did not return 'pleather pants'")
        return False
    
    print(f"✅ Search index correctly returns 1 'pleather pants' item with {len(pleather_pants_items[0].variants)} variants")
    
    return True

async def main():
    """Run comprehensive clothing tests"""
    print("="*70)
    print("Comprehensive Clothing Category Tests")
    print("="*70)
    
    print("\nTest 1: Multiple Clothing Items Across Categories")
    print("-"*70)
    test1 = await test_clothing_categories()
    
    print("\n" + "="*70)
    print("Test 2: Search Index Integrity")
    print("-"*70)
    test2 = await test_search_index()
    
    print("\n" + "="*70)
    if test1 and test2:
        print("✅ ALL COMPREHENSIVE TESTS PASSED")
        print("="*70)
        return 0
    else:
        print("❌ SOME COMPREHENSIVE TESTS FAILED")
        print("="*70)
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
