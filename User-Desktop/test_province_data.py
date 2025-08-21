#!/usr/bin/env python3
"""
Test script to add province and region data to the database
"""
import sys
import os

# Add the project directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.database_api import get_api

def add_test_data():
    """Add test province and region data"""
    api = get_api()

    # Connect to database
    if not api.connect():
        print("❌ Failed to connect to database")
        return

    print("✅ Connected to database")

    # Add provinces (record type '01')
    provinces = [
        ('01', '001', 'Iraq', 'Republic of Iraq'),
        ('01', '002', 'Turkey', 'Republic of Turkey'),
        ('01', '003', 'Jordan', 'Hashemite Kingdom of Jordan')
    ]

    print("\n📍 Adding provinces...")
    for recty, code, name, description in provinces:
        result = api.add_main_code(recty, code, name, description)
        if result:
            print(f"✅ Added province: {name} ({code})")
        else:
            print(f"ℹ️  Province may already exist: {name} ({code})")

    # Add regions for Iraq (province code '001')
    iraq_regions = [
        ('02', '00101', 'Baghdad', 'Capital of Iraq'),
        ('02', '00102', 'Basra', 'Southern Iraq'),
        ('02', '00103', 'Mosul', 'Northern Iraq'),
        ('02', '00104', 'Erbil', 'Kurdistan Region'),
        ('02', '00105', 'Najaf', 'Central Iraq')
    ]

    # Add regions for Turkey (province code '002')
    turkey_regions = [
        ('02', '00201', 'Istanbul', 'Largest city in Turkey'),
        ('02', '00202', 'Ankara', 'Capital of Turkey'),
        ('02', '00203', 'Izmir', 'Western Turkey'),
        ('02', '00204', 'Bursa', 'Northwestern Turkey'),
        ('02', '00205', 'Antalya', 'Southern Turkey')
    ]

    # Add regions for Jordan (province code '003')
    jordan_regions = [
        ('02', '00301', 'Amman', 'Capital of Jordan'),
        ('02', '00302', 'Zarqa', 'Industrial center'),
        ('02', '00303', 'Irbid', 'Northern Jordan'),
        ('02', '00304', 'Aqaba', 'Red Sea port'),
        ('02', '00305', 'Madaba', 'Historical city')
    ]

    all_regions = iraq_regions + turkey_regions + jordan_regions

    print("\n🏙️  Adding regions...")
    for recty, code, name, description in all_regions:
        result = api.add_main_code(recty, code, name, description)
        if result:
            print(f"✅ Added region: {name} ({code})")
        else:
            print(f"ℹ️  Region may already exist: {name} ({code})")

    # Test the new API methods
    print("\n🧪 Testing API methods...")

    # Test get_provinces
    provinces = api.get_provinces()
    print(f"📋 Found {len(provinces)} provinces:")
    for province in provinces:
        print(f"   - {province['name']} ({province['code']})")

    # Test get_regions_by_province
    for province_code in ['001', '002', '003']:
        regions = api.get_regions_by_province(province_code)
        if regions:
            province_name = next((p['name'] for p in provinces if p['code'] == province_code), 'Unknown')
            print(f"📋 Found {len(regions)} regions for {province_name} ({province_code}):")
            for region in regions:
                print(f"   - {region['name']} ({region['code']})")
        else:
            print(f"❌ No regions found for province {province_code}")

    api.close()
    print("\n✅ Test data added successfully!")

if __name__ == "__main__":
    add_test_data()
