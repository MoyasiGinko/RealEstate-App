"""
Final verification script for dropdown values.
"""
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.database_api import get_api

def verify_dropdowns():
    """Verify all dropdown values are correctly retrieved from the database."""
    api = get_api()
    api.connect()

    print("\n=== Property Types ===")
    property_types = api.get_property_types()
    if property_types:
        for t in property_types:
            print(f"  {t.get('code')} - {t.get('name')}")
    else:
        print("  No property types found")

    print("\n=== Building Types ===")
    building_types = api.get_building_types()
    if building_types:
        for t in building_types:
            print(f"  {t.get('code')} - {t.get('name')}")
    else:
        print("  No building types found")

    print("\n=== Offer Types ===")
    offer_types = api.get_offer_types()
    if offer_types:
        for t in offer_types:
            print(f"  {t.get('code')} - {t.get('name')}")
    else:
        print("  No offer types found")

    print("\n=== Provinces ===")
    provinces = api.get_provinces()
    if provinces:
        for p in provinces:
            print(f"  {p.get('code')} - {p.get('name')}")
    else:
        print("  No provinces found")

    print("\n=== Cities ===")
    cities = api.get_cities()
    if cities:
        for c in cities:
            print(f"  {c.get('code')} - {c.get('name')}")
    else:
        print("  No cities found")

if __name__ == "__main__":
    verify_dropdowns()
