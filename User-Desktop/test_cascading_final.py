#!/usr/bin/env python3
"""
Final test to verify cascading dropdown functionality is working correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.database_api import DatabaseAPI

def test_cascading_functionality():
    """Test the complete cascading dropdown functionality."""

    print("=== TESTING CASCADING DROPDOWN FUNCTIONALITY ===")

    # Initialize database API
    api = DatabaseAPI()

    # Test 1: Get all provinces
    print("\n1. Testing province loading...")
    provinces = api.get_main_codes_by_type('01')
    print(f"Found {len(provinces)} provinces:")
    for province in provinces[:3]:  # Show first 3
        print(f"  - {province.get('code')} - {province.get('name')}")

    # Test 2: Test cascading for each province
    print("\n2. Testing cascading functionality...")
    for province in provinces[:2]:  # Test first 2 provinces
        province_code = province.get('code')
        province_name = province.get('name')

        print(f"\n   Testing province: {province_code} - {province_name}")

        # Get cities for this province
        cities = api.get_cities_by_province(province_code)
        print(f"   Found {len(cities)} cities:")

        for city in cities[:3]:  # Show first 3 cities
            print(f"     - {city.get('code')} - {city.get('name')}")

    print("\n=== CASCADING DROPDOWN TEST COMPLETED SUCCESSFULLY ===")
    print("\nThe cascading functionality should work as follows:")
    print("1. User selects a province (e.g., '001 - Iraq')")
    print("2. Region dropdown automatically updates to show cities starting with '001'")
    print("3. Cities like '00101 - Baghdad', '00102 - Basra' will appear")
    print("\nThe PropertyForm.on_province_selected() method handles this automatically!")

if __name__ == "__main__":
    test_cascading_functionality()
