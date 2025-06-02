"""
Test script for database API functions.
"""
from src.models.database_api import get_api

def test_main_codes():
    api = get_api()
    api.connect()

    print("Testing property types:")
    property_types = api.get_property_types()
    if property_types:
        for t in property_types:
            print(f"Code: {t.get('Code')}, Name: {t.get('Name')}")
    else:
        print("No property types found")

    print("\nTesting building types:")
    building_types = api.get_building_types()
    if building_types:
        for t in building_types:
            print(f"Code: {t.get('Code')}, Name: {t.get('Name')}")
    else:
        print("No building types found")

if __name__ == "__main__":
    test_main_codes()
