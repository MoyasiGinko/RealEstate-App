"""
Test script for the database API.
"""

import os
import sys
import unittest
from datetime import date

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.database_api import DatabaseAPI

class TestDatabaseAPI(unittest.TestCase):
    """Test cases for the DatabaseAPI class."""

    def setUp(self):
        """Set up test case."""
        self.api = DatabaseAPI()
        self.api.db.db_path = ":memory:"  # Use in-memory database for testing
        self.assertTrue(self.api.connect())

        # Set company code
        self.api.set_company_code('E901')

        # Insert initial data
        self.api.insert_initial_data()

    def tearDown(self):
        """Tear down test case."""
        self.api.close()

    def test_owner_management(self):
        """Test owner management functions."""
        # Add an owner
        owner_code = self.api.add_owner("Test Owner", "07901234567", "Test note")
        self.assertIsNotNone(owner_code)

        # Get the owner
        owner = self.api.get_owner_by_code(owner_code)
        self.assertIsNotNone(owner)
        self.assertEqual(owner['ownername'], "Test Owner")
        self.assertEqual(owner['ownerphone'], "07901234567")
        self.assertEqual(owner['Note'], "Test note")

        # Update the owner
        self.assertTrue(self.api.update_owner(owner_code, "Updated Owner", "07901234568", "Updated note"))

        # Get the updated owner
        owner = self.api.get_owner_by_code(owner_code)
        self.assertEqual(owner['ownername'], "Updated Owner")
        self.assertEqual(owner['ownerphone'], "07901234568")
        self.assertEqual(owner['Note'], "Updated note")

        # Delete the owner
        self.assertTrue(self.api.delete_owner(owner_code))

        # Verify owner is deleted
        owner = self.api.get_owner_by_code(owner_code)
        self.assertIsNone(owner)

    def test_property_management(self):
        """Test property management functions."""
        # Add an owner for the property
        owner_code = self.api.add_owner("Property Owner", "07901234567", "Property owner")

        # Add a property
        property_data = {
            'Rstatetcode': '03001',              # Residential
            'Buildtcode': '04002',               # House
            'Yearmake': date(2010, 1, 1).isoformat(),
            'Property-area': 150.75,
            'Unitm-code': '05001',               # Square Meter
            'Property-facade': 10.5,
            'Property-depth': 15.0,
            'N-of-bedrooms': 3,
            'N-of-bathrooms': 2,
            'Property-corner': True,
            'Offer-Type-Code': '06001',          # For Sale
            'Province-code': '01001',            # Baghdad
            'Region-code': '02001',              # Baghdad City
            'Property-address': 'Test Address',
            'Ownercode': owner_code,
            'Descriptions': 'Test property'
        }

        property_code = self.api.add_property(property_data)
        self.assertIsNotNone(property_code)

        # Get the property
        property_obj = self.api.get_property_by_code(property_code)
        self.assertIsNotNone(property_obj)
        self.assertEqual(property_obj['Ownercode'], owner_code)
        self.assertEqual(property_obj['Property-area'], 150.75)
        self.assertEqual(property_obj['N-of-bedrooms'], 3)

        # Update the property
        update_data = {
            'Property-area': 160.5,
            'N-of-bedrooms': 4,
            'Descriptions': 'Updated property'
        }

        self.assertTrue(self.api.update_property(property_code, update_data))

        # Get the updated property
        property_obj = self.api.get_property_by_code(property_code)
        self.assertEqual(property_obj['Property-area'], 160.5)
        self.assertEqual(property_obj['N-of-bedrooms'], 4)
        self.assertEqual(property_obj['Descriptions'], 'Updated property')

        # Add a photo
        self.assertTrue(self.api.add_property_photo(
            property_code, '/photos/', 'test_photo', '.jpg'
        ))

        # Check photosituation is updated
        property_obj = self.api.get_property_by_code(property_code)
        self.assertTrue(property_obj['Photosituation'])

        # Get property photos
        photos = self.api.get_property_photos(property_code)
        self.assertEqual(len(photos), 1)
        self.assertEqual(photos[0]['photofilename'], 'test_photo')

        # Delete the photo
        self.assertTrue(self.api.delete_property_photo(property_code, 'test_photo'))

        # Check photosituation is updated
        property_obj = self.api.get_property_by_code(property_code)
        self.assertFalse(property_obj['Photosituation'])

        # Delete the property
        self.assertTrue(self.api.delete_property(property_code))

        # Verify property is deleted
        property_obj = self.api.get_property_by_code(property_code)
        self.assertIsNone(property_obj)

    def test_lookup_data(self):
        """Test lookup data functions."""
        # Get property types
        property_types = self.api.get_property_types()
        self.assertGreater(len(property_types), 0)

        # Get building types
        building_types = self.api.get_building_types()
        self.assertGreater(len(building_types), 0)

        # Get provinces
        provinces = self.api.get_provinces()
        self.assertGreater(len(provinces), 0)

        # Get cities
        cities = self.api.get_cities()
        self.assertGreater(len(cities), 0)

    def test_search_properties(self):
        """Test property search."""
        # Add an owner for the property
        owner_code = self.api.add_owner("Search Owner", "07901234567", "Search owner")

        # Add properties with different characteristics
        for i in range(5):
            property_data = {
                'Rstatetcode': '03001',              # Residential
                'Buildtcode': '04002',               # House
                'Yearmake': date(2010 + i, 1, 1).isoformat(),
                'Property-area': 100 + (i * 20),
                'Unitm-code': '05001',               # Square Meter
                'N-of-bedrooms': 2 + i,
                'N-of-bathrooms': 1 + i,
                'Property-corner': i % 2 == 0,
                'Offer-Type-Code': '06001' if i % 2 == 0 else '06002',  # For Sale/Rent
                'Province-code': '01001',            # Baghdad
                'Region-code': '02001',              # Baghdad City
                'Property-address': f'Search Address {i}',
                'Ownercode': owner_code,
                'Descriptions': f'Search property {i}'
            }

            self.assertIsNotNone(self.api.add_property(property_data))

        # Search by bedrooms
        results = self.api.search_properties({'N-of-bedrooms': 3})
        self.assertEqual(len(results), 1)

        # Search by property area range (using SQL BETWEEN in calling code)
        # This would need to be implemented in the actual search method

        # Search by offer type
        results = self.api.search_properties({'Offer-Type-Code': '06001'})  # For Sale
        self.assertEqual(len(results), 3)  # Properties with even index

        # Search by province
        results = self.api.search_properties({'Province-code': '01001'})
        self.assertEqual(len(results), 5)  # All properties

    def test_company_info(self):
        """Test company information functions."""
        # Get company info
        company = self.api.get_company_info()
        self.assertIsNotNone(company)
        self.assertEqual(company['Companyco'], 'E901')

        # Update company info
        company_data = {
            'Companyco': 'E901',
            'Companyna': 'Updated Company',
            'Cophoneno': '07901234567',
            'Caddress': 'Updated Address'
        }

        self.assertTrue(self.api.set_company_info(company_data))

        # Get updated company info
        company = self.api.get_company_info()
        self.assertEqual(company['Companyna'], 'Updated Company')
        self.assertEqual(company['Caddress'], 'Updated Address')

if __name__ == '__main__':
    unittest.main()
