#!/usr/bin/env python3
"""Integration test to verify the variant selector works properly"""

import asyncio
import sys
from bot.services.acnh_service import NooklookService
from bot.models.acnh_item import Item
from bot.ui.pagination import VariantSelectView

# Mock Discord objects for testing
class MockUser:
    def __init__(self):
        self.id = 12345

class MockThumbnail:
    def __init__(self, url):
        self.url = url

async def test_variant_view():
    """Test that VariantSelectView is properly created for pleather pants"""
    service = NooklookService()
    await service.init_database()
    
    # Search for pleather pants
    results = await service.search_all("pleather pants", category_filter="item")
    
    if not results:
        print("❌ ERROR: No results found for 'pleather pants'")
        return False
    
    item = results[0]
    print(f"Testing VariantSelectView for: {item.name}")
    print(f"   Variants: {len(item.variants)}")
    
    # Create a VariantSelectView
    mock_user = MockUser()
    view = VariantSelectView(item, mock_user)
    
    # Check that the view has components
    if not view.children:
        print("❌ ERROR: VariantSelectView has no children/components")
        return False
    
    print(f"✅ VariantSelectView has {len(view.children)} component(s)")
    
    # Check that it's a select menu
    from discord.ui import Select
    selects = [c for c in view.children if isinstance(c, Select)]
    if not selects:
        print("❌ ERROR: No Select component found in VariantSelectView")
        return False
    
    select = selects[0]
    print(f"✅ Found Select component with {len(select.options)} options")
    
    # Verify all variants are in the select
    if len(select.options) != len(item.variants):
        print(f"❌ ERROR: Select has {len(select.options)} options but item has {len(item.variants)} variants")
        return False
    
    print("\n   Select options:")
    for i, option in enumerate(select.options):
        print(f"   {i+1}. {option.label}")
    
    # Test creating an embed
    embed = item.to_discord_embed()
    print(f"\n✅ Discord embed created")
    print(f"   Title: {embed.title}")
    print(f"   Has description: {bool(embed.description)}")
    print(f"   Has thumbnail: {bool(embed.thumbnail)}")
    
    # Check if the embed shows variant information
    if embed.description:
        if "variant" in embed.description.lower() or "color" in embed.description.lower():
            print("✅ Embed mentions variants/colors")
    
    return True

async def test_furniture_with_variants():
    """Test a furniture item with variants to ensure the fix doesn't break furniture"""
    service = NooklookService()
    await service.init_database()
    
    # Search for an item with variants (e.g., "simple panel")
    results = await service.search_all("simple panel", category_filter="item")
    
    if not results:
        print("⚠️  WARNING: Could not test furniture variants (simple panel not found)")
        return True  # Not a failure, just skip
    
    item = results[0]
    if len(item.variants) <= 1:
        print(f"⚠️  WARNING: {item.name} has {len(item.variants)} variant(s), expected more for testing")
        return True
    
    print(f"\n✅ Furniture item '{item.name}' has {len(item.variants)} variants")
    
    # Create view
    mock_user = MockUser()
    view = VariantSelectView(item, mock_user)
    
    if not view.children:
        print("❌ ERROR: Furniture VariantSelectView has no components")
        return False
    
    print(f"✅ Furniture VariantSelectView has {len(view.children)} component(s)")
    
    return True

async def main():
    """Run all integration tests"""
    print("="*60)
    print("Integration Tests: Variant Selector")
    print("="*60)
    
    print("\nTest 1: Pleather Pants Variant Selector")
    print("-"*60)
    test1 = await test_variant_view()
    
    print("\n" + "="*60)
    print("Test 2: Furniture with Variants")
    print("-"*60)
    test2 = await test_furniture_with_variants()
    
    print("\n" + "="*60)
    if test1 and test2:
        print("✅ ALL INTEGRATION TESTS PASSED")
        print("="*60)
        return 0
    else:
        print("❌ SOME INTEGRATION TESTS FAILED")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
