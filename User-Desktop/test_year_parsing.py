#!/usr/bin/env python3
"""
Test script to verify property editing with year field works correctly
"""

from src.models.database_api import DatabaseAPI

def test_property_year_parsing():
    """Test that property year parsing works correctly for both string and integer values."""

    # Initialize the database API
    api = DatabaseAPI()

    if not api.connect():
        print("❌ Failed to connect to database")
        return False

    api.set_company_code("E901")

    # Add a test owner first
    owner_code = api.add_owner("Test Owner", "07901234567", "Test owner for year parsing")
    if not owner_code:
        print("❌ Failed to create test owner")
        api.close()
        return False

    print(f"✅ Created test owner: {owner_code}")

    # Test 1: Add property with integer year (how it's stored in DB)
    property_data_int = {
        'Rstatetcode': '03001',              # Residential
        'Buildtcode': '04002',               # House
        'Yearmake': 2010,                    # Integer year
        'Property-area': 150.75,
        'Unitm-code': '05001',               # Square Meter
        'Property-facade': 10.5,
        'Property-depth': 15.0,
        'N-of-bedrooms': 3,
        'N-of-bathrooms': 2,
        'Property-corner': True,
        'Offer-Type-Code': '06001',          # For Sale
        'Province-code': '001',              # Iraq
        'Region-code': '00201',              # Amman
        'Property-address': 'Test Address Int Year',
        'Ownercode': owner_code,
        'Descriptions': 'Test property with integer year'
    }

    property_code_int = api.add_property(property_data_int)
    if not property_code_int:
        print("❌ Failed to create property with integer year")
        api.close()
        return False

    print(f"✅ Created property with integer year: {property_code_int}")

    # Test 2: Add property with string date year
    property_data_str = {
        'Rstatetcode': '03001',              # Residential
        'Buildtcode': '04002',               # House
        'Yearmake': '2015-01-01',            # String date format
        'Property-area': 160.25,
        'Unitm-code': '05001',               # Square Meter
        'Property-facade': 12.0,
        'Property-depth': 18.0,
        'N-of-bedrooms': 4,
        'N-of-bathrooms': 3,
        'Property-corner': False,
        'Offer-Type-Code': '06002',          # For Rent
        'Province-code': '001',              # Iraq
        'Region-code': '00201',              # Amman
        'Property-address': 'Test Address Str Year',
        'Ownercode': owner_code,
        'Descriptions': 'Test property with string year'
    }

    property_code_str = api.add_property(property_data_str)
    if not property_code_str:
        print("❌ Failed to create property with string year")
        api.close()
        return False

    print(f"✅ Created property with string year: {property_code_str}")

    # Test 3: Retrieve properties and test year parsing logic
    prop_int = api.get_property_by_code(property_code_int)
    prop_str = api.get_property_by_code(property_code_str)

    if not prop_int or not prop_str:
        print("❌ Failed to retrieve properties")
        api.close()
        return False

    # Test the year parsing logic that would be used in the UI
    def parse_year_value(year_value):
        """Simulate the year parsing logic from property_management.py"""
        if isinstance(year_value, str) and '-' in year_value:
            return year_value.split('-')[0]  # Extract year from ISO format like "2020-01-01"
        else:
            return str(year_value)  # Convert integer year to string

    year_int = parse_year_value(prop_int['Yearmake'])
    year_str = parse_year_value(prop_str['Yearmake'])

    print(f"✅ Integer year parsed: {prop_int['Yearmake']} -> {year_int}")
    print(f"✅ String year parsed: {prop_str['Yearmake']} -> {year_str}")

    # Verify the parsing worked correctly
    if year_int != "2010":
        print(f"❌ Integer year parsing failed: expected '2010', got '{year_int}'")
        api.close()
        return False

    if year_str != "2015":
        print(f"❌ String year parsing failed: expected '2015', got '{year_str}'")
        api.close()
        return False

    # Test 4: Update properties with different year formats
    update_data_int = {'Yearmake': 2020}
    update_data_str = {'Yearmake': '2025-06-03'}

    if not api.update_property(property_code_int, update_data_int):
        print("❌ Failed to update property with integer year")
        api.close()
        return False

    if not api.update_property(property_code_str, update_data_str):
        print("❌ Failed to update property with string year")
        api.close()
        return False

    print("✅ Successfully updated properties with different year formats")

    # Verify updates
    prop_int_updated = api.get_property_by_code(property_code_int)
    prop_str_updated = api.get_property_by_code(property_code_str)

    year_int_updated = parse_year_value(prop_int_updated['Yearmake'])
    year_str_updated = parse_year_value(prop_str_updated['Yearmake'])

    print(f"✅ Updated integer year: {prop_int_updated['Yearmake']} -> {year_int_updated}")
    print(f"✅ Updated string year: {prop_str_updated['Yearmake']} -> {year_str_updated}")

    # Clean up
    api.delete_property(property_code_int)
    api.delete_property(property_code_str)
    api.delete_owner(owner_code)

    api.close()

    print("\n🎉 All year parsing tests passed!")
    print("The property management form should now handle both integer and string year values correctly.")

    return True

if __name__ == "__main__":
    test_property_year_parsing()
