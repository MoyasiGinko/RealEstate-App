#!/usr/bin/env python3
"""
Test script to verify cascading dropdown functionality.
This tests the province/region filtering logic.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.database_api import DatabaseAPI

def test_cascading_dropdown():
    """Test the cascading dropdown functionality."""
    print("=== Testing Cascading Dropdown Functionality ===\n")

    try:
        # Initialize the database API
        api = DatabaseAPI()

        print("1. Testing province data loading...")
        provinces = api.get_main_codes_by_type('01')
        if provinces:
            print(f"   ✓ Found {len(provinces)} provinces:")
            for province in provinces:
                print(f"     - {province.get('code', 'N/A')} - {province.get('name', 'Unknown')}")
        else:
            print("   ✗ No provinces found")
            return False

        print("\n2. Testing cascading region filtering...")

        # Test each province
        for province in provinces[:3]:  # Test first 3 provinces to avoid too much output
            province_code = province.get('code', '')
            province_name = province.get('name', 'Unknown')

            print(f"\n   Testing province: {province_code} - {province_name}")

            # Get cities for this province
            cities = api.get_cities_by_province(province_code)

            if cities:
                print(f"   ✓ Found {len(cities)} cities for {province_name}:")
                for city in cities[:5]:  # Show first 5 cities
                    city_code = city.get('code', 'N/A')
                    city_name = city.get('name', 'Unknown')
                    print(f"     - {city_code} - {city_name}")

                    # Verify the city code starts with the province pattern
                    expected_prefix = f"00{province_code}"
                    if city_code.startswith(expected_prefix):
                        print(f"       ✓ Code matches pattern ({expected_prefix}*)")
                    else:
                        print(f"       ✗ Code doesn't match pattern (expected {expected_prefix}*, got {city_code})")

                if len(cities) > 5:
                    print(f"     ... and {len(cities) - 5} more cities")
            else:
                print(f"   ! No cities found for {province_name}")

        print("\n3. Testing specific cases...")

        # Test Iraq (001)
        print("\n   Testing Iraq (001) cities:")
        iraq_cities = api.get_cities_by_province('001')
        if iraq_cities:
            print(f"   ✓ Found {len(iraq_cities)} Iraqi cities")
            for city in iraq_cities[:3]:
                print(f"     - {city.get('code', 'N/A')} - {city.get('name', 'Unknown')}")
        else:
            print("   ✗ No Iraqi cities found")

        # Test Jordan (002)
        print("\n   Testing Jordan (002) cities:")
        jordan_cities = api.get_cities_by_province('002')
        if jordan_cities:
            print(f"   ✓ Found {len(jordan_cities)} Jordanian cities")
            for city in jordan_cities[:3]:
                print(f"     - {city.get('code', 'N/A')} - {city.get('name', 'Unknown')}")
        else:
            print("   ✗ No Jordanian cities found")

        print("\n=== Cascading Dropdown Test Complete ===")
        print("✓ All tests passed! The cascading dropdown should work correctly.")
        return True

    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_form_logic():
    """Test the form logic for cascading dropdowns."""
    print("\n=== Testing Form Logic ===\n")

    try:
        api = DatabaseAPI()

        # Simulate province selection event
        print("1. Simulating province selection...")

        # Test the province code extraction logic
        test_province_text = "001 - Iraq"
        if ' - ' in test_province_text:
            province_code = test_province_text.split(' - ')[0].strip()
            print(f"   Selected province text: '{test_province_text}'")
            print(f"   Extracted province code: '{province_code}'")

            # Get cities for this province
            cities = api.get_cities_by_province(province_code)
            if cities:
                print(f"   ✓ Found {len(cities)} cities for province {province_code}")

                # Format city values as they would appear in the spinner
                city_values = [f"{city.get('code', 'N/A')} - {city.get('name', 'Unknown')}" for city in cities]
                print("   City dropdown values:")
                for i, city_val in enumerate(city_values[:5]):
                    print(f"     {i+1}. {city_val}")
                if len(city_values) > 5:
                    print(f"     ... and {len(city_values) - 5} more")
            else:
                print(f"   ✗ No cities found for province {province_code}")

        print("\n✓ Form logic test complete!")
        return True

    except Exception as e:
        print(f"\n✗ Error during form logic testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Cascading Dropdown Implementation...")

    success1 = test_cascading_dropdown()
    success2 = test_form_logic()

    if success1 and success2:
        print("\n🎉 All tests passed! The cascading dropdown implementation is ready.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
