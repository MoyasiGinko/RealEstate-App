#!/usr/bin/env python3
"""
Script to add test province and region data to the database.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.database_api import get_api

def add_test_data():
    """Add test provinces and regions to the database."""
    api = get_api()

    # Connect to database
    if not api.connect():
        print("Failed to connect to database")
        return

    # Test data - Iraq provinces and regions
    test_data = [
        # Provinces (Record Type '01')
        ('01', '001', 'Iraq', 'Republic of Iraq'),
        ('01', '002', 'Syria', 'Syrian Arab Republic'),
        ('01', '003', 'Jordan', 'Hashemite Kingdom of Jordan'),

        # Regions for Iraq (Record Type '02')
        ('02', '00101', 'Baghdad', 'Capital of Iraq'),
        ('02', '00102', 'Basra', 'Southern Iraq'),
        ('02', '00103', 'Mosul', 'Northern Iraq'),
        ('02', '00104', 'Erbil', 'Kurdistan Region'),
        ('02', '00105', 'Najaf', 'Holy city'),
        ('02', '00106', 'Karbala', 'Holy city'),

        # Regions for Syria (Record Type '02')
        ('02', '00201', 'Damascus', 'Capital of Syria'),
        ('02', '00202', 'Aleppo', 'Northern Syria'),
        ('02', '00203', 'Homs', 'Central Syria'),

        # Regions for Jordan (Record Type '02')
        ('02', '00301', 'Amman', 'Capital of Jordan'),
        ('02', '00302', 'Zarqa', 'Northern Jordan'),
        ('02', '00303', 'Irbid', 'Northern Jordan'),

        # Property Types (Record Type '03')
        ('03', '1', 'House', 'Residential house'),
        ('03', '2', 'Apartment', 'Residential apartment'),
        ('03', '3', 'Land', 'Empty land'),
        ('03', '4', 'Commercial', 'Commercial property'),
        ('03', '5', 'Industrial', 'Industrial property'),

        # Building Types (Record Type '04')
        ('04', '1', 'Concrete', 'Concrete construction'),
        ('04', '2', 'Brick', 'Brick construction'),
        ('04', '3', 'Steel', 'Steel frame construction'),
        ('04', '4', 'Mixed', 'Mixed materials'),

        # Unit Measures (Record Type '05')
        ('05', '1', 'Square Meter', 'm²'),
        ('05', '2', 'Square Foot', 'ft²'),
        ('05', '3', 'Acre', 'acre'),

        # Offer Types (Record Type '06')
        ('06', '1', 'Sale', 'For sale'),
        ('06', '2', 'Rent', 'For rent'),
        ('06', '3', 'Lease', 'For lease'),
    ]

    print("Adding test data to database...")

    added_count = 0
    for record_type, code, name, description in test_data:
        try:
            success = api.add_main_code(record_type, code, name, description)
            if success:
                print(f"✓ Added {record_type}-{code}: {name}")
                added_count += 1
            else:
                print(f"✗ Failed to add {record_type}-{code}: {name}")
        except Exception as e:
            print(f"✗ Error adding {record_type}-{code}: {name} - {str(e)}")

    print(f"\nCompleted! Added {added_count} records out of {len(test_data)} total.")

    # Test queries
    print("\n=== Testing Province/Region Queries ===")

    provinces = api.get_provinces()
    print(f"\nProvinces found: {len(provinces)}")
    for p in provinces:
        print(f"  - {p.get('code')}: {p.get('name')}")

        regions = api.get_regions_by_province(p.get('code'))
        print(f"    Regions: {len(regions)}")
        for r in regions:
            print(f"      - {r.get('code')}: {r.get('name')}")

    # Add test company and owner data
    print("\n=== Adding Test Company and Owner ===")

    # Set a default company code
    api.set_company_code('TEST')

    # Add test company info
    company_data = {
        'Companyco': 'TEST',
        'Companyna': 'Test Real Estate Company',
        'Cityco': '00101',  # Baghdad
        'Caddress': 'Test Address, Baghdad',
        'Cophoneno': '1234567890',
        'Username': 'testuser',
        'Password': 'test123',
        'SubscriptionTCode': '1',
        'Subscriptionduration': '1',
        'Descriptions': 'Test company for development'
    }

    try:
        api.set_company_info(company_data)
        print("✓ Added test company")
    except Exception as e:
        print(f"✗ Error adding company: {e}")

    # Add test owners
    test_owners = [
        ('Ahmed Ali', '0791234567', 'Property owner in Baghdad'),
        ('Sara Hassan', '0787654321', 'Property investor'),
        ('Omar Khalil', '0779876543', 'Real estate developer')
    ]

    for name, phone, note in test_owners:
        try:
            owner_code = api.add_owner(name, phone, note)
            if owner_code:
                print(f"✓ Added owner {owner_code}: {name}")
            else:
                print(f"✗ Failed to add owner: {name}")
        except Exception as e:
            print(f"✗ Error adding owner {name}: {e}")

    print("\nTest data setup completed!")
    api.close()

if __name__ == "__main__":
    add_test_data()
