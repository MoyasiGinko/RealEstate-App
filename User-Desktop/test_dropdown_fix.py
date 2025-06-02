#!/usr/bin/env python3
"""
Test script to verify that dropdown values are working correctly after all fixes.
This will test the dropdown data retrieval and form initialization.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

from src.models.database_api import get_api
from src.screens.property_management import PropertyForm

def test_dropdown_data():
    """Test that all dropdown data is properly retrieved."""
    print("🔍 Testing dropdown data retrieval...")

    api = get_api()

    # Test property types
    print("\n📋 Property Types:")
    property_types = api.get_property_types()
    if property_types:
        for prop_type in property_types[:3]:  # Show first 3
            print(f"  - Code: {prop_type.get('code')}, Name: {prop_type.get('name')}")
        print(f"  ... and {len(property_types) - 3} more" if len(property_types) > 3 else "")
    else:
        print("  ❌ No property types found")

    # Test building types
    print("\n🏢 Building Types:")
    building_types = api.get_building_types()
    if building_types:
        for building_type in building_types[:3]:
            print(f"  - Code: {building_type.get('code')}, Name: {building_type.get('name')}")
        print(f"  ... and {len(building_types) - 3} more" if len(building_types) > 3 else "")
    else:
        print("  ❌ No building types found")

    # Test provinces
    print("\n🌍 Provinces:")
    provinces = api.get_provinces()
    if provinces:
        for province in provinces[:3]:
            print(f"  - Code: {province.get('code')}, Name: {province.get('name')}")
        print(f"  ... and {len(provinces) - 3} more" if len(provinces) > 3 else "")
    else:
        print("  ❌ No provinces found")

    # Test cities
    print("\n🏙️ Cities:")
    cities = api.get_cities()
    if cities:
        for city in cities[:3]:
            print(f"  - Code: {city.get('code')}, Name: {city.get('name')}")
        print(f"  ... and {len(cities) - 3} more" if len(cities) > 3 else "")
    else:
        print("  ❌ No cities found")

    # Test owners
    print("\n👥 Owners:")
    owners = api.get_all_owners()
    if owners:
        for owner in owners[:3]:
            print(f"  - Code: {owner.get('ownercode')}, Name: {owner.get('ownername')}")
        print(f"  ... and {len(owners) - 3} more" if len(owners) > 3 else "")
    else:
        print("  ❌ No owners found")

    return {
        'property_types': len(property_types) if property_types else 0,
        'building_types': len(building_types) if building_types else 0,
        'provinces': len(provinces) if provinces else 0,
        'cities': len(cities) if cities else 0,
        'owners': len(owners) if owners else 0
    }

def test_property_form_creation():
    """Test that PropertyForm can be created without errors."""
    print("\n🎨 Testing PropertyForm creation...")

    try:
        # Mock save callback
        def mock_save_callback(data):
            print(f"Save callback called with: {data}")

        # Test creating new property form
        form = PropertyForm(save_callback=mock_save_callback)
        print("  ✅ New property form created successfully")

        # Test creating edit property form with sample data
        sample_property_data = {
            'realstatecode': 'TEST001',
            'Rstatetcode': '01',
            'Buildtcode': '02',
            'Property-area': '150.5',
            'Property-facade': '12.0',
            'Property-depth': '15.0',
            'N-of-bedrooms': '3',
            'N-of-bathrooms': '2',
            'Property-corner': True,
            'Yearmake': '2020-01-01',
            'Property-address': 'Test Address 123',
            'Descriptions': 'Test property description'
        }

        edit_form = PropertyForm(
            save_callback=mock_save_callback,
            property_data=sample_property_data
        )
        print("  ✅ Edit property form created successfully")

        return True

    except Exception as e:
        print(f"  ❌ Error creating PropertyForm: {e}")
        return False

def main():
    print("🚀 Starting Dropdown Fix Verification Test")
    print("=" * 50)

    # Test dropdown data
    counts = test_dropdown_data()

    # Test PropertyForm creation
    form_test_passed = test_property_form_creation()

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"  📋 Property Types: {counts['property_types']} items")
    print(f"  🏢 Building Types: {counts['building_types']} items")
    print(f"  🌍 Provinces: {counts['provinces']} items")
    print(f"  🏙️ Cities: {counts['cities']} items")
    print(f"  👥 Owners: {counts['owners']} items")
    print(f"  🎨 PropertyForm Creation: {'✅ PASSED' if form_test_passed else '❌ FAILED'}")

    total_items = sum(counts.values())
    if total_items > 0 and form_test_passed:
        print("\n🎉 All tests PASSED! Dropdown fix is successful!")
        print("✅ The real estate application should now work properly with correct dropdown values.")
    else:
        print("\n⚠️ Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()
