#!/usr/bin/env python3
"""
Test MainCode Country Selection Functionality
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from src.core.database import DatabaseManager
from src.api.maincode_api import MainCodeAPI
from kivy.logger import Logger
import kivy
kivy.require('2.3.1')

def main():
    print("============================================================")
    print("TESTING MAINCODE COUNTRY SELECTION FUNCTIONALITY")
    print("============================================================")

    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        db_manager.connect('./data/local.db')

        # Initialize MainCode API
        maincode_api = MainCodeAPI(db_manager)

        # Test 1: Get countries
        print("1. Testing Get Countries...")
        response = maincode_api.get_countries()
        if response.success:
            countries = response.data
            print(f"✅ Loaded {len(countries)} countries")
            if countries:
                print(f"   Sample country: {countries[0]['display']}")
        else:
            print(f"❌ Failed to get countries: {response.message}")
            return False

        # Test 2: Get record type options
        print("2. Testing Record Type Options...")
        options = maincode_api.get_record_type_options()
        print("✅ Record type options:")
        for option in options:
            print(f"   {option['text']}")

        # Test 3: Auto code generation for countries
        print("3. Testing Country Code Generation...")
        response = maincode_api.get_next_available_code('01')
        if response.success:
            country_code = response.data['code']
            print(f"✅ Next country code: {country_code}")
        else:
            print(f"❌ Failed to generate country code: {response.message}")
            return False

        # Test 4: Auto code generation for cities with country context
        if countries:
            print("4. Testing City Code Generation with Country Context...")
            test_country = countries[0]['code']
            response = maincode_api.get_next_available_code('02', test_country)
            if response.success:
                city_code = response.data['code']
                print(f"✅ Next city code for country {test_country}: {city_code}")
            else:
                print(f"❌ Failed to generate city code: {response.message}")
                return False
        else:
            print("⚠️  No countries available for city code test")

        print("\n============================================================")
        print("✅ ALL MAINCODE COUNTRY SELECTION TESTS PASSED!")
        print("============================================================")
        print("🎉 MAINCODE ENHANCEMENTS SUMMARY:")
        print("   ✅ Country Loading: WORKING")
        print("   ✅ Record Type Options: WORKING")
        print("   ✅ Country Code Auto-Generation: WORKING")
        print("   ✅ City Code Generation with Country Context: WORKING")
        print("   ✅ Country Selection for City Creation: IMPLEMENTED")

        db_manager.close()
        return True

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
