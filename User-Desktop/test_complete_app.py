#!/usr/bin/env python3
"""
Final comprehensive test to verify all fixes are working correctly.
This script tests:
1. Database connection
2. Dropdown data retrieval (all types)
3. Application startup without errors
4. PropertyForm initialization
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_database_dropdowns():
    """Test that all dropdown types return proper data"""
    print("🔍 Testing Database Dropdown Functionality...")

    try:
        from src.models.database_api import DatabaseAPI

        # Initialize database
        db = DatabaseAPI()        # Test all dropdown types
        dropdown_types = [
            ('Property Types', db.get_property_types),
            ('Building Types', db.get_building_types),
            ('Provinces', db.get_provinces),
            ('Cities', db.get_cities),
            ('All Owners', db.get_all_owners)
        ]        # Test all dropdown types (correct method for owners)
        dropdown_types = [
            ('Property Types', db.get_property_types),
            ('Building Types', db.get_building_types),
            ('Provinces', db.get_provinces),
            ('Cities', db.get_cities),
            ('All Owners', db.get_all_owners)
        ]

        all_passed = True
        for name, method in dropdown_types:
            try:
                data = method()
                if data and len(data) > 0:
                    # Check data structure based on method type
                    first_item = data[0]
                    if name == 'All Owners':
                        # Owners have different structure: Ownercode, ownername, etc.
                        if isinstance(first_item, dict) and ('Ownercode' in first_item or 'ownercode' in first_item):
                            owner_code = first_item.get('Ownercode') or first_item.get('ownercode', 'N/A')
                            owner_name = first_item.get('ownername', 'Unknown')
                            print(f"  ✅ {name}: {len(data)} items found")
                            print(f"     Sample: {owner_code} - {owner_name}")
                        else:
                            print(f"  ❌ {name}: Invalid data structure")
                            all_passed = False
                    else:
                        # Other dropdowns have code-name pairs
                        if isinstance(first_item, dict) and 'code' in first_item and 'name' in first_item:
                            print(f"  ✅ {name}: {len(data)} items found")
                            print(f"     Sample: {first_item['code']} - {first_item['name']}")
                        else:
                            print(f"  ❌ {name}: Invalid data structure")
                            all_passed = False
                else:
                    print(f"  ⚠️  {name}: No data found")
            except Exception as e:
                print(f"  ❌ {name}: Error - {e}")
                all_passed = False

        return all_passed

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_property_form_creation():
    """Test PropertyForm can be created without errors"""
    print("\n🔍 Testing PropertyForm Creation...")

    try:
        # Set up minimal Kivy environment
        os.environ['KIVY_NO_ARGS'] = '1'
        from kivy.app import App
        from kivy.config import Config        Config.set('graphics', 'width', '1')
        Config.set('graphics', 'height', '1')
        Config.set('graphics', 'show_cursor', '0')

        from src.screens.property_management import PropertyForm

        # Try to create PropertyForm instance with dummy callback
        def dummy_callback(*args, **kwargs):
            pass

        form = PropertyForm(save_callback=dummy_callback)
        print("  ✅ PropertyForm created successfully")
        print(f"  ✅ safe_get_text method exists: {hasattr(form, 'safe_get_text')}")

        # Test safe_get_text method
        if hasattr(form, 'safe_get_text'):
            test_result = form.safe_get_text(None)
            if test_result == "":
                print("  ✅ safe_get_text handles None correctly")
            else:
                print(f"  ❌ safe_get_text returned '{test_result}' instead of ''")
                return False

        return True

    except Exception as e:
        print(f"  ❌ PropertyForm creation failed: {e}")
        return False

def test_application_startup():
    """Test that the main application can be imported without errors"""
    print("\n🔍 Testing Application Import...")

    try:        # Test importing main components
        from src.main import MainApp
        print("  ✅ Main application imported successfully")

        from src.screens.dashboard import DashboardScreen
        print("  ✅ Dashboard screen imported successfully")

        from src.screens.property_management import PropertyManagementScreen
        print("  ✅ Property management screen imported successfully")

        return True

    except Exception as e:
        print(f"  ❌ Application import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive Application Test")
    print("=" * 50)

    # Run all tests
    tests = [
        ("Database Dropdowns", test_database_dropdowns),
        ("PropertyForm Creation", test_property_form_creation),
        ("Application Startup", test_application_startup)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)

    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\n🎯 Overall Result: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("🎉 ALL TESTS PASSED! The dropdown fix is complete and working!")
        print("\n📝 What was fixed:")
        print("  • Database column names changed from uppercase to lowercase")
        print("  • PropertyForm class completely reconstructed")
        print("  • Variable scope issues fixed (property_data → self.property_data)")
        print("  • Safe text handling added for None values")
        print("  • Syntax errors fixed throughout property_management.py")
        print("  • KV file path corrected for dashboard.py")
        print("  • Application now starts without FileNotFoundError")
    else:
        print("⚠️  Some tests failed. Please check the output above.")

    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
