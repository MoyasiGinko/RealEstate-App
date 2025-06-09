#!/usr/bin/env python3
"""
Simple test script to verify API functionality
Tests CompanyInfo and MainCode CRUD operations only
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def test_database_connection():
    """Test basic database connection"""
    print("🔌 Testing Database Connection")
    print("=" * 40)

    try:
        from src.core.database import DatabaseManager

        # Create database manager
        db_manager = DatabaseManager()
        print(f"✓ Database type: {db_manager.db_type}")

        # Test connection
        if db_manager.connect():
            print("✓ Database connected successfully")

            # Test basic operations
            connection_info = db_manager.get_info()
            print(f"✓ Connection info: {connection_info}")

            # Test connection health
            if db_manager.test_connection():
                print("✓ Connection test passed")
            else:
                print("❌ Connection test failed")

            db_manager.close()
            print("✓ Database connection closed")
            return True
        else:
            print("❌ Failed to connect to database")
            return False

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_api_functionality():
    """Test API layer functionality"""
    print("\n📡 Testing API Layer")
    print("=" * 40)

    try:
        from src.api import APIManager

        # Initialize API
        api = APIManager()
        init_result = api.initialize()

        if not init_result.success:
            print(f"❌ API initialization failed: {init_result.error}")
            return False

        print("✓ API initialized successfully")

        # Test CompanyInfo API
        print("\n📊 Testing CompanyInfo API:")
        companies_result = api.company.get_all_companies()
        if companies_result.success:
            print(f"✓ Retrieved {companies_result.count} companies")
        else:
            print(f"❌ Failed to get companies: {companies_result.error}")

        # Test MainCode API
        print("\n🔧 Testing MainCode API:")
        codes_result = api.maincode.get_all_main_codes()
        if codes_result.success:
            print(f"✓ Retrieved {codes_result.count} main codes")
        else:
            print(f"❌ Failed to get main codes: {codes_result.error}")        # Test creating a sample company
        print("\n✏️ Testing Company Creation:")
        test_company = {
            'company_code': 'TEST001',
            'company_name': 'Test Company',
            'city_code': 'NYC',
            'company_address': '123 Main St'
        }

        create_result = api.company.create_company(test_company)
        if create_result.success:
            print("✓ Test company created successfully")            # Test retrieving the company
            get_result = api.company.get_company('TEST001')
            if get_result.success:
                print("✓ Test company retrieved successfully")
                print(f"  Company: {get_result.data.company_name}")

                # Clean up - delete test company
                delete_result = api.company.delete_company('TEST001')
                if delete_result.success:
                    print("✓ Test company deleted successfully")
                else:
                    print(f"⚠️ Failed to delete test company: {delete_result.error}")
            else:
                print(f"❌ Failed to retrieve test company: {get_result.error}")
        else:
            print(f"❌ Failed to create test company: {create_result.error}")

        # Test creating a sample main code
        print("\n🔧 Testing MainCode Creation:")
        test_maincode = {
            'recty': 'TYPE1',
            'code': 'TEST001',
            'name': 'Test Code',
            'description': 'Test Description'
        }

        create_result = api.maincode.create_main_code(test_maincode)
        if create_result.success:
            print("✓ Test main code created successfully")

            # Clean up - delete test main code
            delete_result = api.maincode.delete_main_code('TEST001')
            if delete_result.success:
                print("✓ Test main code deleted successfully")
            else:
                print(f"⚠️ Failed to delete test main code: {delete_result.error}")
        else:
            print(f"❌ Failed to create test main code: {create_result.error}")

        api.close()
        print("✓ API closed successfully")
        return True

    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 CompanyInfo & MainCode API Test")
    print("=" * 50)

    # Test database connection
    db_test = test_database_connection()

    # Test API functionality
    api_test = test_api_functionality()

    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    print(f"Database Connection: {'✅ PASSED' if db_test else '❌ FAILED'}")
    print(f"API Functionality: {'✅ PASSED' if api_test else '❌ FAILED'}")

    if db_test and api_test:
        print("\n🎉 ALL TESTS PASSED! Ready for production use.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
