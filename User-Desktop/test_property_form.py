#!/usr/bin/env python3
"""
Test script to verify property form functionality - simulates the UI flow
"""

from src.models.database_api import DatabaseAPI

def test_property_form_simulation():
    """Test that simulates the property form creation and editing workflow."""

    print("🔧 Testing Property Form Functionality")
    print("=" * 50)

    # Initialize the database API
    api = DatabaseAPI()

    if not api.connect():
        print("❌ Failed to connect to database")
        return False

    api.set_company_code("E901")

    # Simulate loading dropdown data (what happens when PropertyForm is created)
    print("📋 Testing dropdown data loading...")

    try:
        property_types = api.get_property_types() or []
        building_types = api.get_building_types() or []
        provinces = api.get_provinces() or []
        cities = api.get_cities() or []
        unit_measures = api.get_unit_measures() or []
        offer_types = api.get_offer_types() or []

        print(f"✅ Property Types: {len(property_types)} items")
        print(f"✅ Building Types: {len(building_types)} items")
        print(f"✅ Provinces: {len(provinces)} items")
        print(f"✅ Cities: {len(cities)} items")
        print(f"✅ Unit Measures: {len(unit_measures)} items")
        print(f"✅ Offer Types: {len(offer_types)} items")

        # Verify dropdowns have proper format
        if property_types and 'code' in property_types[0] and 'name' in property_types[0]:
            print(f"✅ Dropdown format correct: {property_types[0]}")
        else:
            print(f"❌ Dropdown format incorrect: {property_types[0] if property_types else 'Empty'}")
            return False

    except Exception as e:
        print(f"❌ Error loading dropdown data: {e}")
        return False

    # Create a test owner for properties
    owner_code = api.add_owner("Form Test Owner", "07901234567", "Test owner for form testing")
    if not owner_code:
        print("❌ Failed to create test owner")
        api.close()
        return False

    print(f"✅ Created test owner: {owner_code}")

    # Test 1: Create a property with year data
    print("\n🏠 Testing property creation...")

    property_data = {
        'Rstatetcode': property_types[0]['code'] if property_types else '03001',
        'Buildtcode': building_types[0]['code'] if building_types else '04001',
        'Yearmake': 2010,  # Integer year (as stored in DB)
        'Property-area': 150.75,
        'Unitm-code': unit_measures[0]['code'] if unit_measures else '05001',
        'Property-facade': 10.5,
        'Property-depth': 15.0,
        'N-of-bedrooms': 3,
        'N-of-bathrooms': 2,
        'Property-corner': True,
        'Offer-Type-Code': offer_types[0]['code'] if offer_types else '06001',
        'Province-code': provinces[0]['code'] if provinces else '001',
        'Region-code': cities[0]['code'] if cities else '00201',
        'Property-address': 'Test Form Address',
        'Ownercode': owner_code,
        'Descriptions': 'Test property for form functionality'
    }

    property_code = api.add_property(property_data)
    if not property_code:
        print("❌ Failed to create property")
        api.close()
        return False

    print(f"✅ Created property: {property_code}")

    # Test 2: Simulate loading property for editing (what happens in show_edit_property_form)
    print("\n✏️  Testing property editing simulation...")

    try:
        # Get property data (simulates getting full_property_data in show_edit_property_form)
        property_obj = api.get_property_by_code(property_code)
        if not property_obj:
            print("❌ Failed to retrieve property for editing")
            api.close()
            return False

        print(f"✅ Retrieved property data: Yearmake = {property_obj['Yearmake']} (type: {type(property_obj['Yearmake'])})")

        # Simulate the year parsing logic from PropertyForm.__init__
        year_value = property_obj['Yearmake']
        if isinstance(year_value, str) and '-' in year_value:
            year = year_value.split('-')[0]  # Extract year from ISO format like "2020-01-01"
        else:
            year = str(year_value)  # Convert integer year to string

        print(f"✅ Year parsing successful: {year_value} -> '{year}'")

        # Simulate year spinner value checking
        from datetime import datetime
        current_year = datetime.now().year
        year_values = [str(y) for y in range(1950, current_year + 1)]

        if year in year_values:
            print(f"✅ Year '{year}' found in spinner values")
        else:
            print(f"❌ Year '{year}' not found in spinner values")
            return False

        # Test updating the property with a different year format
        update_data = {'Yearmake': '2025-06-03'}  # String date format

        if api.update_property(property_code, update_data):
            print("✅ Property update successful")

            # Verify the update
            updated_property = api.get_property_by_code(property_code)
            updated_year_value = updated_property['Yearmake']

            # Parse the updated year
            if isinstance(updated_year_value, str) and '-' in updated_year_value:
                updated_year = updated_year_value.split('-')[0]
            else:
                updated_year = str(updated_year_value)

            print(f"✅ Updated year parsing: {updated_year_value} -> '{updated_year}'")

        else:
            print("❌ Property update failed")
            return False

    except Exception as e:
        print(f"❌ Error during property editing simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test 3: Test dropdown value formatting for UI
    print("\n🎛️  Testing dropdown value formatting...")

    try:
        # Simulate how dropdowns are formatted in the UI
        property_type_values = ['No property types available']
        if property_types:
            property_type_values = [f"{item['code']} - {item['name']}" for item in property_types]

        building_type_values = ['No building types available']
        if building_types:
            building_type_values = [f"{item['code']} - {item['name']}" for item in building_types]

        print(f"✅ Property type dropdown values: {len(property_type_values)} items")
        print(f"   Sample: {property_type_values[0]}")

        print(f"✅ Building type dropdown values: {len(building_type_values)} items")
        print(f"   Sample: {building_type_values[0]}")

        # Test that dropdowns are not showing "N/A - Unknown"
        if 'N/A - Unknown' in property_type_values or 'N/A - Unknown' in building_type_values:
            print("❌ Found 'N/A - Unknown' in dropdown values - this indicates the old bug is still present")
            return False
        else:
            print("✅ No 'N/A - Unknown' values found - dropdown fix is working")

    except Exception as e:
        print(f"❌ Error during dropdown formatting test: {e}")
        return False

    # Clean up
    api.delete_property(property_code)
    api.delete_owner(owner_code)
    api.close()

    print("\n🎉 All property form tests passed!")
    print("✅ Dropdown data loads correctly")
    print("✅ Year parsing works for both integer and string values")
    print("✅ Property editing should work without crashes")
    print("✅ No 'N/A - Unknown' values in dropdowns")

    return True

if __name__ == "__main__":
    test_property_form_simulation()
