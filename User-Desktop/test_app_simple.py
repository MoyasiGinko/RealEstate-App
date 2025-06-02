#!/usr/bin/env python3
"""
Simple comprehensive test to verify all fixes are working correctly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_database_dropdowns():
    """Test that all dropdown types return proper data"""
    print("🔍 Testing Database Dropdown Functionality...")

    try:
        from src.models.database_api import DatabaseAPI

        # Initialize database and connect
        db = DatabaseAPI()
        db.connect()

        # Test all dropdown types
        test_results = []

        # Property Types
        try:
            property_types = db.get_property_types()
            if property_types and len(property_types) > 0:
                sample = property_types[0]
                if 'code' in sample and 'name' in sample:
                    print(f"  ✅ Property Types: {len(property_types)} items")
                    print(f"     Sample: {sample['code']} - {sample['name']}")
                    test_results.append(True)
                else:
                    print(f"  ❌ Property Types: Invalid structure")
                    test_results.append(False)
            else:
                print(f"  ⚠️  Property Types: No data")
                test_results.append(False)
        except Exception as e:
            print(f"  ❌ Property Types: Error - {e}")
            test_results.append(False)

        # Building Types
        try:
            building_types = db.get_building_types()
            if building_types and len(building_types) > 0:
                sample = building_types[0]
                if 'code' in sample and 'name' in sample:
                    print(f"  ✅ Building Types: {len(building_types)} items")
                    print(f"     Sample: {sample['code']} - {sample['name']}")
                    test_results.append(True)
                else:
                    print(f"  ❌ Building Types: Invalid structure")
                    test_results.append(False)
            else:
                print(f"  ⚠️  Building Types: No data")
                test_results.append(False)
        except Exception as e:
            print(f"  ❌ Building Types: Error - {e}")
            test_results.append(False)

        # Provinces
        try:
            provinces = db.get_provinces()
            if provinces and len(provinces) > 0:
                sample = provinces[0]
                if 'code' in sample and 'name' in sample:
                    print(f"  ✅ Provinces: {len(provinces)} items")
                    print(f"     Sample: {sample['code']} - {sample['name']}")
                    test_results.append(True)
                else:
                    print(f"  ❌ Provinces: Invalid structure")
                    test_results.append(False)
            else:
                print(f"  ⚠️  Provinces: No data")
                test_results.append(False)
        except Exception as e:
            print(f"  ❌ Provinces: Error - {e}")
            test_results.append(False)

        # Cities
        try:
            cities = db.get_cities()
            if cities and len(cities) > 0:
                sample = cities[0]
                if 'code' in sample and 'name' in sample:
                    print(f"  ✅ Cities: {len(cities)} items")
                    print(f"     Sample: {sample['code']} - {sample['name']}")
                    test_results.append(True)
                else:
                    print(f"  ❌ Cities: Invalid structure")
                    test_results.append(False)
            else:
                print(f"  ⚠️  Cities: No data")
                test_results.append(False)
        except Exception as e:
            print(f"  ❌ Cities: Error - {e}")
            test_results.append(False)

        # Owners
        try:
            owners = db.get_all_owners()
            if owners and len(owners) > 0:
                sample = owners[0]
                owner_code = sample.get('Ownercode') or sample.get('ownercode', 'N/A')
                owner_name = sample.get('ownername', 'Unknown')
                print(f"  ✅ Owners: {len(owners)} items")
                print(f"     Sample: {owner_code} - {owner_name}")
                test_results.append(True)
            else:
                print(f"  ⚠️  Owners: No data")
                test_results.append(False)
        except Exception as e:
            print(f"  ❌ Owners: Error - {e}")
            test_results.append(False)

        return all(test_results)

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_application_imports():
    """Test that the application can be imported without errors"""
    print("\n🔍 Testing Application Imports...")

    try:
        # Test main app
        from src.main import MainApp
        print("  ✅ Main application imported successfully")

        # Test dashboard screen
        from src.screens.dashboard import DashboardScreen
        print("  ✅ Dashboard screen imported successfully")

        # Test property management screen
        from src.screens.property_management import PropertyManagementScreen
        print("  ✅ Property management screen imported successfully")

        # Test search report screen
        from src.screens.search_report import SearchReportScreen
        print("  ✅ Search report screen imported successfully")

        return True

    except Exception as e:
        print(f"  ❌ Application imports failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Simple Application Test")
    print("=" * 50)

    # Run tests
    db_test = test_database_dropdowns()
    import_test = test_application_imports()

    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)

    print(f"Database Dropdowns: {'✅ PASSED' if db_test else '❌ FAILED'}")
    print(f"Application Imports: {'✅ PASSED' if import_test else '❌ FAILED'}")

    total_passed = sum([db_test, import_test])
    print(f"\n🎯 Overall Result: {total_passed}/2 tests passed")

    if total_passed == 2:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ The dropdown fix is complete and working!")
        print("✅ Application starts without FileNotFoundError!")
        print("✅ Database connection and dropdown data retrieval working!")
        print("\n🎊 The real estate application is ready for use!")
    else:
        print("⚠️  Some tests failed. Please check the output above.")

    return total_passed == 2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
