#!/usr/bin/env python3
"""
Test script to verify dropdown data is being loaded correctly
"""

from src.models.database_api import DatabaseAPI

def test_dropdown_data():
    """Test that dropdown data is being loaded correctly."""

    # Initialize the database API
    api = DatabaseAPI()

    if not api.connect():
        print("❌ Failed to connect to database")
        return False

    api.set_company_code("E901")  # Set a test company code

    # Test each dropdown data source
    tests = [
        ("Provinces", api.get_provinces),
        ("Cities", api.get_cities),
        ("Property Types", api.get_property_types),
        ("Building Types", api.get_building_types),
        ("Unit Measures", api.get_unit_measures),
        ("Offer Types", api.get_offer_types),
    ]

    all_passed = True

    for name, method in tests:
        try:
            data = method()
            if data and len(data) > 0:
                print(f"✅ {name}: Found {len(data)} items")
                # Show first few items as examples
                for i, item in enumerate(data[:3]):
                    print(f"   - {item}")
                if len(data) > 3:
                    print(f"   ... and {len(data) - 3} more")
            else:
                print(f"❌ {name}: No data found (returned: {data})")
                all_passed = False
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            all_passed = False
        print()

    # Also test the underlying get_main_codes_by_type method directly
    print("Testing get_main_codes_by_type method directly:")
    try:
        # Test with known record types from our seed data
        for recty, name in [('01', 'Provinces'), ('02', 'Cities'), ('03', 'Property Types'),
                           ('04', 'Building Types'), ('05', 'Unit Measures'), ('06', 'Offer Types')]:
            data = api.get_main_codes_by_type(recty)
            print(f"  {name} (recty={recty}): {len(data) if data else 0} items")
            if data and len(data) > 0:
                print(f"    Sample: {data[0]}")
    except Exception as e:
        print(f"  Error testing get_main_codes_by_type: {e}")
        all_passed = False

    api.close()

    if all_passed:
        print("\n🎉 All dropdown data tests passed!")
    else:
        print("\n⚠️  Some dropdown data tests failed!")

    return all_passed

if __name__ == "__main__":
    test_dropdown_data()
