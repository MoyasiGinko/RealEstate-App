"""
Simplified test runner for the application.
"""
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_property_management_import():
    """Test importing property_management.py."""
    try:
        print("Importing property_management module...")
        from src.screens.property_management import PropertyManagementScreen
        print("Successfully imported PropertyManagementScreen")
        return True
    except Exception as e:
        print(f"Error importing property_management module: {e}")
        return False

def test_search_report_import():
    """Test importing search_report.py."""
    try:
        print("Importing search_report module...")
        from src.screens.search_report import SearchReportScreen
        print("Successfully imported SearchReportScreen")
        return True
    except Exception as e:
        print(f"Error importing search_report module: {e}")
        return False

def test_database_api_import():
    """Test importing database_api.py."""
    try:
        print("Importing database_api module...")
        from src.models.database_api import get_api
        print("Successfully imported get_api")
        api = get_api()
        print("Successfully got API instance")
        return True
    except Exception as e:
        print(f"Error importing database_api module: {e}")
        return False

def main():
    """Run tests."""
    print("Testing module imports...")

    db_api_ok = test_database_api_import()
    print()

    if db_api_ok:
        property_management_ok = test_property_management_import()
        print()

        search_report_ok = test_search_report_import()
        print()

        if property_management_ok and search_report_ok:
            print("All modules imported successfully!")
        else:
            print("Some modules failed to import.")
    else:
        print("Database API import failed. Stopping tests.")

if __name__ == "__main__":
    main()
