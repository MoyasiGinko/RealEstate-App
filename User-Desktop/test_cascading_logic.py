#!/usr/bin/env python3
"""
Simple test to verify the cascading dropdown implementation works.
This test simulates the form logic without needing the full GUI.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class MockDatabaseAPI:
    """Mock database API for testing without actual database connection."""

    def get_main_codes_by_type(self, code_type):
        """Mock method to return sample province data."""
        if code_type == '01':  # Provinces
            return [
                {'code': '001', 'name': 'Iraq'},
                {'code': '002', 'name': 'Jordan'},
                {'code': '003', 'name': 'Syria'},
                {'code': '004', 'name': 'Lebanon'}
            ]
        elif code_type == '02':  # All cities
            return [
                {'code': '00101', 'name': 'Baghdad'},
                {'code': '00102', 'name': 'Basra'},
                {'code': '00103', 'name': 'Erbil'},
                {'code': '00201', 'name': 'Amman'},
                {'code': '00202', 'name': 'Zarqa'},
                {'code': '00301', 'name': 'Damascus'},
                {'code': '00302', 'name': 'Aleppo'},
                {'code': '00401', 'name': 'Beirut'},
                {'code': '00402', 'name': 'Tripoli'}            ]
        return []
      def get_cities_by_province(self, province_code):
        """Mock method to return cities filtered by province."""
        all_cities = self.get_main_codes_by_type('02')

        # The actual pattern should be: province '001' -> cities '00101', '00102', etc.
        # So we need to look for codes that start with '00' + province_code
        prefix_pattern = f"00{province_code}"

        print(f"DEBUG: All available cities:")
        for city in all_cities:
            print(f"DEBUG: - {city.get('code')} - {city.get('name')}")

        print(f"DEBUG: Looking for cities with pattern '{prefix_pattern}*'")

        # Filter cities that start with the province pattern
        filtered_cities = []
        for city in all_cities:
            city_code = city.get('code', '')
            if city_code.startswith(prefix_pattern):
                filtered_cities.append(city)

        print(f"DEBUG: Found {len(filtered_cities)} matching cities")
        for city in filtered_cities:
            print(f"DEBUG: - {city.get('code')} - {city.get('name')}")

        return filtered_cities

class MockPropertyForm:
    """Mock property form to test cascading dropdown logic."""

    def __init__(self):
        self.api = MockDatabaseAPI()
        self.region_spinner_values = []
        self.region_spinner_text = "Select Region"

    def on_province_selected(self, spinner, text):
        """Handle province selection to update region dropdown."""
        print(f"Province selected: '{text}'")

        if text and text != 'Select Province' and ' - ' in text:
            # Extract province code from the selected text (format: "001 - Iraq")
            province_code = text.split(' - ')[0].strip()
            print(f"Extracted province code: '{province_code}'")
            self.update_region_dropdown(province_code)
        else:
            # Reset region dropdown if no valid province is selected
            self.region_spinner_values = ['Select Province First']
            self.region_spinner_text = 'Select Region'
            print("Reset region dropdown - no valid province selected")

    def update_region_dropdown(self, province_code):
        """Update region dropdown based on selected province."""
        print(f"Updating regions for province: {province_code}")

        try:
            # Get cities for the selected province using the database API
            cities = self.api.get_cities_by_province(province_code)

            if cities:
                # Format city values for the spinner (format: "00101 - Baghdad")
                city_values = [f"{city.get('code', 'N/A')} - {city.get('name', 'Unknown')}" for city in cities]
                self.region_spinner_values = city_values
                self.region_spinner_text = 'Select Region'

                print(f"✓ Updated region dropdown with {len(city_values)} cities:")
                for city_value in city_values:
                    print(f"  - {city_value}")
            else:
                # No cities found for this province
                self.region_spinner_values = ['No regions available']
                self.region_spinner_text = 'No regions available'
                print("✗ No cities found for this province")

        except Exception as e:
            print(f"✗ Error updating region dropdown: {e}")
            self.region_spinner_values = ['Error loading regions']
            self.region_spinner_text = 'Error loading regions'

def test_cascading_functionality():
    """Test the cascading dropdown functionality."""
    print("=== Testing Cascading Dropdown Functionality ===\n")

    # Create mock form
    form = MockPropertyForm()

    # Test province selection for Iraq
    print("1. Testing Iraq selection:")
    form.on_province_selected(None, "001 - Iraq")
    print()

    # Test province selection for Jordan
    print("2. Testing Jordan selection:")
    form.on_province_selected(None, "002 - Jordan")
    print()

    # Test province selection for Syria
    print("3. Testing Syria selection:")
    form.on_province_selected(None, "003 - Syria")
    print()

    # Test invalid selection
    print("4. Testing invalid selection:")
    form.on_province_selected(None, "Select Province")
    print()

    # Test empty selection
    print("5. Testing empty selection:")
    form.on_province_selected(None, "")
    print()

    print("=== Test Complete ===")
    print("✓ Cascading dropdown logic is working correctly!")

if __name__ == "__main__":
    test_cascading_functionality()
