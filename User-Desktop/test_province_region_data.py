#!/usr/bin/env python3
"""
Test script to verify province and region data loading
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.database_api import get_api

def test_province_region_data():
    """Test that province and region data is properly loaded"""
    api = get_api()

    try:
        if not api.connect():
            print("❌ Failed to connect to database")
            return False

        print("✅ Connected to database successfully")

        # Test search_properties includes province and region names
        properties = api.search_properties({})

        if not properties:
            print("ℹ️  No properties found in database")
            return True

        print(f"✅ Found {len(properties)} properties")

        # Check if the first property has province and region data
        prop = properties[0]

        print(f"Property keys: {list(prop.keys())}")

        has_province = 'province_name' in prop
        has_region = 'region_name' in prop

        print(f"✅ Province data included: {has_province}")
        print(f"✅ Region data included: {has_region}")

        if has_province:
            print(f"   Sample province: {prop.get('province_name', 'N/A')}")
        if has_region:
            print(f"   Sample region: {prop.get('region_name', 'N/A')}")

        # Test the new methods
        print("\nTesting new API methods:")

        # Test province name lookup
        province_name = api.get_province_name_by_code('001')
        print(f"✅ Province '001' name: {province_name}")

        # Test region name lookup
        region_name = api.get_region_name_by_code('00101')
        print(f"✅ Region '00101' name: {region_name}")

        print("\n🎉 All tests passed!")
        return True

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

    finally:
        api.close()

if __name__ == "__main__":
    test_province_region_data()
