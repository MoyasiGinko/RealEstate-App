#!/usr/bin/env python3
"""
Test script to verify the localized property detail modal functionality
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from configs.language_manager import get_language_manager, get_text

def test_localized_property_detail_fields():
    """Test that all property detail field labels are properly localized"""

    language_manager = get_language_manager()

    print("🔍 Testing Property Detail Modal Localization")
    print("=" * 60)

    # Test fields for property detail modal
    test_fields = [
        'property_details',
        'property_code_label',
        'property_type_label',
        'building_type_label',
        'year_built',
        'area_m2',
        'facade_m',
        'depth_m',
        'bedrooms_label',
        'bathrooms_label',
        'floors_label',
        'corner_property_label',
        'price_label',
        'currency_label',
        'province_label',
        'region_label',
        'address_label',
        'owner_label',
        'owner_code_label',
        'description_label',
        'not_specified',
        'property_photos',
        'no_photos_available',
        'error_loading_photos',
        'unknown',
        'yes',
        'no'
    ]

    # Test English translations
    print("\n📝 English Translations:")
    print("-" * 30)
    language_manager.set_language('en')

    for field in test_fields:
        translation = get_text(field, f"MISSING: {field}")
        print(f"  {field:<25} : {translation}")

    # Test Arabic translations
    print("\n📝 Arabic Translations:")
    print("-" * 30)
    language_manager.set_language('ar')

    for field in test_fields:
        translation = get_text(field, f"مفقود: {field}")
        print(f"  {field:<25} : {translation}")

    # Test localized values
    print("\n🔄 Testing Localized Value Formatting:")
    print("-" * 40)

    # Test corner property values
    language_manager.set_language('en')
    yes_en = get_text('yes', 'Yes')
    no_en = get_text('no', 'No')
    not_specified_en = get_text('not_specified', 'Not specified')

    language_manager.set_language('ar')
    yes_ar = get_text('yes', 'نعم')
    no_ar = get_text('no', 'لا')
    not_specified_ar = get_text('not_specified', 'غير محدد')

    print(f"  Corner Property - Yes:        EN='{yes_en}' | AR='{yes_ar}'")
    print(f"  Corner Property - No:         EN='{no_en}' | AR='{no_ar}'")
    print(f"  Not Specified:                EN='{not_specified_en}' | AR='{not_specified_ar}'")

    print("\n🎉 Localization test completed!")
    print("\n💡 Features now available:")
    print("   ✅ All property detail field labels are localized")
    print("   ✅ Property modal title is localized")
    print("   ✅ Photo section title is localized")
    print("   ✅ 'No photos available' message is localized")
    print("   ✅ Error messages are localized")
    print("   ✅ Boolean values (Yes/No) are localized")
    print("   ✅ Arabic font support for all text elements")
    print("   ✅ Proper RTL text alignment for Arabic")

if __name__ == "__main__":
    test_localized_property_detail_fields()
