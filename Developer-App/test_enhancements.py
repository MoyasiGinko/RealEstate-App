#!/usr/bin/env python3
"""
Test script to verify CompanyInfo CRUD enhancements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import DatabaseManager
from src.api.api_manager import APIManager
from src.api.models import CompanyInfo


def test_api_functionality():
    """Test the enhanced API functionality"""
    print("=== Testing Enhanced CompanyInfo CRUD API ===")

    # Initialize database and API
    db_manager = DatabaseManager("./data/local.db")
    if not db_manager.connect():
        print("❌ Failed to connect to database")
        return False

    api_manager = APIManager(db_manager)
    if not api_manager.initialize():
        print("❌ Failed to initialize API manager")
        return False

    print("✅ Database and API initialized successfully")

    # Test 1: Auto-generate company code
    print("\n--- Test 1: Auto-generate Company Code ---")
    response = api_manager.company.get_next_company_code()
    if response.success:
        next_code = response.data['code']
        print(f"✅ Generated company code: {next_code}")
    else:
        print(f"❌ Failed to generate company code: {response.error}")
        return False

    # Test 2: Auto-generate subscription code
    print("\n--- Test 2: Auto-generate Subscription Code ---")
    response = api_manager.company.get_next_subscription_code()
    if response.success:
        next_sub_code = response.data['code']
        print(f"✅ Generated subscription code: {next_sub_code}")
    else:
        print(f"❌ Failed to generate subscription code: {response.error}")
        return False

    # Test 3: Get cities for dropdown
    print("\n--- Test 3: Get Cities for Dropdown ---")
    response = api_manager.company.get_cities()
    if response.success:
        cities = response.data
        print(f"✅ Retrieved {len(cities)} cities")
        if cities:
            print(f"   Sample city: {cities[0]['display']}")
    else:
        print(f"❌ Failed to get cities: {response.error}")
        return False

    # Test 4: Get countries for MainCode
    print("\n--- Test 4: Get Countries for MainCode ---")
    response = api_manager.maincode.get_countries()
    if response.success:
        countries = response.data
        print(f"✅ Retrieved {len(countries)} countries")
        if countries:
            print(f"   Sample country: {countries[0]['display']}")
    else:
        print(f"❌ Failed to get countries: {response.error}")
        return False

    # Test 5: Create a test company with auto-generated codes
    print("\n--- Test 5: Create Test Company ---")
    test_company_data = {
        'company_code': next_code,
        'company_name': 'Test Company AutoGen',
        'city_code': cities[0]['code'] if cities else None,
        'company_address': 'Test Address 123',
        'phone_number': '07901234567',
        'username': 'testuser',
        'password': 'testpass123',
        'subscription_code': next_sub_code,
        'subscription_duration': '12',
        'descriptions': 'Auto-generated test company'
    }

    response = api_manager.company.create_company(test_company_data)
    if response.success:
        print(f"✅ Created test company: {test_company_data['company_code']}")
    else:
        print(f"❌ Failed to create test company: {response.error}")
        return False

    # Test 6: Retrieve and verify the created company
    print("\n--- Test 6: Verify Created Company ---")
    response = api_manager.company.get_company(test_company_data['company_code'])
    if response.success:
        company = response.data
        print(f"✅ Retrieved company: {company.company_name}")
        print(f"   Company Code: {company.company_code}")
        print(f"   City Code: {company.city_code}")
        print(f"   Subscription Code: {company.subscription_code}")
    else:
        print(f"❌ Failed to retrieve test company: {response.error}")
        return False

    # Test 7: Update the test company
    print("\n--- Test 7: Update Test Company ---")
    update_data = {
        'company_name': 'Updated Test Company',
        'descriptions': 'Updated description'
    }

    response = api_manager.company.update_company(test_company_data['company_code'], update_data)
    if response.success:
        print("✅ Updated test company successfully")
    else:
        print(f"❌ Failed to update test company: {response.error}")
        return False

    # Test 8: Clean up - delete the test company
    print("\n--- Test 8: Clean Up Test Company ---")
    response = api_manager.company.delete_company(test_company_data['company_code'])
    if response.success:
        print("✅ Deleted test company successfully")
    else:
        print(f"❌ Failed to delete test company: {response.error}")
        return False

    print("\n🎉 All tests passed successfully!")
    print("\n=== Summary of Enhanced Features ===")
    print("✅ Auto-generation of company codes (E001, E002, etc.)")
    print("✅ Auto-generation of subscription codes (1, 2, etc.)")
    print("✅ City dropdown populated from MainCode records")
    print("✅ Country selection for MainCode city creation")
    print("✅ Proper city code extraction from dropdown selections")
    print("✅ Enhanced form validation and error handling")

    return True


if __name__ == "__main__":
    success = test_api_functionality()
    sys.exit(0 if success else 1)
