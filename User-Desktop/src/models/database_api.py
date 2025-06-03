"""
Database API module for the Real Estate desktop application.
This module provides the API functions for interacting with the database.
"""

import os
import sys
import random
import string
import datetime
from pathlib import Path

# Add the parent directory to sys.path to allow importing from configs
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from configs.database import DatabaseManager

class DatabaseAPI:
    """Database API for the Real Estate desktop application."""

    def __init__(self):
        """Initialize the database API."""
        self.db = DatabaseManager()
        self.company_code = None

    def connect(self):
        """Connect to the database."""
        return self.db.connect_local() and self.db.create_tables()

    def close(self):
        """Close the database connection."""
        self.db.close()

    def set_company_code(self, company_code):
        """Set the company code."""
        self.company_code = company_code

    # Owner Management Functions

    def get_all_owners(self):
        """Get all owners from the database."""
        return self.db.execute_query("SELECT * FROM Owners ORDER BY ownername")

    def get_owner_by_code(self, owner_code):
        """Get an owner by code."""
        owners = self.db.execute_query("SELECT * FROM Owners WHERE Ownercode = ?", (owner_code,))
        return owners[0] if owners else None

    def add_owner(self, owner_name, owner_phone, note=None):
        """
        Add a new owner to the database.

        Args:
            owner_name (str): The name of the owner
            owner_phone (str): The phone number of the owner
            note (str, optional): Notes about the owner

        Returns:
            str: The owner code if successful, None otherwise
        """
        # Generate a unique owner code (A + 3 digits)
        while True:
            owner_code = 'A' + ''.join(random.choices(string.digits, k=3))
            existing = self.db.execute_query("SELECT COUNT(*) as count FROM Owners WHERE Ownercode = ?", (owner_code,))
            if existing[0]['count'] == 0:
                break

        result = self.db.execute_query(
            "INSERT INTO Owners (Ownercode, ownername, ownerphone, Note) VALUES (?, ?, ?, ?)",
            (owner_code, owner_name, owner_phone, note)
        )

        return owner_code if result else None

    def update_owner(self, owner_code, owner_name, owner_phone, note=None):
        """
        Update an existing owner in the database.

        Args:
            owner_code (str): The code of the owner to update
            owner_name (str): The new name of the owner
            owner_phone (str): The new phone number of the owner
            note (str, optional): New notes about the owner

        Returns:
            bool: True if successful, False otherwise
        """
        return self.db.execute_query(
            "UPDATE Owners SET ownername = ?, ownerphone = ?, Note = ? WHERE Ownercode = ?",
            (owner_name, owner_phone, note, owner_code)
        )

    def delete_owner(self, owner_code):
        """
        Delete an owner from the database.

        Args:
            owner_code (str): The code of the owner to delete

        Returns:
            bool: True if successful, False otherwise
        """
        # Check if owner is linked to any properties
        properties = self.db.execute_query(
            "SELECT COUNT(*) as count FROM Realstatspecification WHERE Ownercode = ?",
            (owner_code,)
        )

        if properties[0]['count'] > 0:
            return False  # Cannot delete owner linked to properties

        return self.db.execute_query("DELETE FROM Owners WHERE Ownercode = ?", (owner_code,))

    # Property Management Functions

    def get_all_properties(self):
        """Get all properties from the database."""
        return self.db.execute_query("""
            SELECT r.*, o.ownername, m1.name as property_type, m2.name as building_type
            FROM Realstatspecification r
            LEFT JOIN Owners o ON r.Ownercode = o.Ownercode
            LEFT JOIN Maincode m1 ON r.Rstatetcode = m1.code AND m1.recty = '03'
            LEFT JOIN Maincode m2 ON r.Buildtcode = m2.code AND m2.recty = '04'
            ORDER BY r.realstatecode
        """)

    def get_property_by_code(self, property_code):
        """Get a property by code."""
        properties = self.db.execute_query(
            "SELECT * FROM Realstatspecification WHERE realstatecode = ?",
            (property_code,)
        )
        return properties[0] if properties else None

    def get_property_photos(self, property_code):
        """Get photos for a property."""
        return self.db.execute_query(
            "SELECT * FROM realstatephotos WHERE realstatecode = ?",
            (property_code,)
        )

    def generate_property_code(self):
        """Generate a unique property code (CompanyCode + Random 4 chars)."""
        if not self.company_code:
            raise ValueError("Company code not set")

        while True:
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            property_code = self.company_code + random_part

            existing = self.db.execute_query(
                "SELECT COUNT(*) as count FROM Realstatspecification WHERE realstatecode = ?",
                (property_code,)
            )

            if existing[0]['count'] == 0:
                return property_code

    def add_property(self, property_data):
        """
        Add a new property to the database.

        Args:
            property_data (dict): A dictionary containing property data:
                - Rstatetcode: Property type code
                - Buildtcode: Building type code
                - Yearmake: Year built
                - Property-area: Area in square meters
                - Unitm-code: Unit of measure code
                - Property-facade: Facade length
                - Property-depth: Depth
                - N-of-bedrooms: Number of bedrooms
                - N-of-bathrooms: Number of bathrooms
                - Property-corner: Is corner property (boolean)
                - Offer-Type-Code: Offer type code
                - Province-code: Province code
                - Region-code: Region code
                - Property-address: Address
                - Ownercode: Owner code
                - Descriptions: Description

        Returns:
            str: The property code if successful, None otherwise
        """
        if not self.company_code:
            raise ValueError("Company code not set")

        # Generate a unique property code
        property_code = self.generate_property_code()

        # Prepare data for insertion
        data = {
            'Companyco': self.company_code,
            'realstatecode': property_code,
            'Photosituation': False  # Default to no photos
        }

        # Add the property data
        data.update(property_data)

        # Build the SQL query
        fields = ', '.join([f'"{k}"' if '-' in k else k for k in data.keys()])
        placeholders = ', '.join(['?' for _ in data.keys()])

        query = f"INSERT INTO Realstatspecification ({fields}) VALUES ({placeholders})"

        result = self.db.execute_query(query, tuple(data.values()))

        return property_code if result else None

    def update_property(self, property_code, property_data):
        """
        Update an existing property in the database.

        Args:
            property_code (str): The code of the property to update
            property_data (dict): A dictionary containing property data to update

        Returns:
            bool: True if successful, False otherwise
        """
        # Build the SQL query
        set_clause = ', '.join([f'"{k}" = ?' if '-' in k else f"{k} = ?" for k in property_data.keys()])

        query = f"UPDATE Realstatspecification SET {set_clause} WHERE realstatecode = ?"

        # Add property_code to the values
        values = list(property_data.values())
        values.append(property_code)

        return self.db.execute_query(query, tuple(values))

    def delete_property(self, property_code):
        """
        Delete a property from the database.

        Args:
            property_code (str): The code of the property to delete

        Returns:
            bool: True if successful, False otherwise
        """
        # First delete all photos
        self.db.execute_query("DELETE FROM realstatephotos WHERE realstatecode = ?", (property_code,))

        # Then delete the property
        return self.db.execute_query("DELETE FROM Realstatspecification WHERE realstatecode = ?", (property_code,))

    def add_property_photo(self, property_code, file_path, photo_filename, photo_extension):
        """
        Add a photo for a property.

        Args:
            property_code (str): The code of the property
            file_path (str): Path to store the photo
            photo_filename (str): Filename of the photo
            photo_extension (str): File extension

        Returns:
            bool: True if successful, False otherwise
        """
        result = self.db.execute_query(
            """INSERT INTO realstatephotos
               (realstatecode, Storagepath, photofilename, Photoextension)
               VALUES (?, ?, ?, ?)""",
            (property_code, file_path, photo_filename, photo_extension)
        )

        # Update the Photosituation flag in the property record
        if result:
            self.db.execute_query(
                "UPDATE Realstatspecification SET Photosituation = ? WHERE realstatecode = ?",
                (True, property_code)
            )

        return result

    def delete_property_photo(self, property_code, photo_filename):
        """
        Delete a photo for a property.

        Args:
            property_code (str): The code of the property
            photo_filename (str): Filename of the photo

        Returns:
            bool: True if successful, False otherwise
        """
        result = self.db.execute_query(
            "DELETE FROM realstatephotos WHERE realstatecode = ? AND photofilename = ?",
            (property_code, photo_filename)
        )

        # Check if any photos remain for this property
        photos = self.db.execute_query(
            "SELECT COUNT(*) as count FROM realstatephotos WHERE realstatecode = ?",
            (property_code,)
        )

        # If no photos remain, update the Photosituation flag
        if photos[0]['count'] == 0:
            self.db.execute_query(
                "UPDATE Realstatspecification SET Photosituation = ? WHERE realstatecode = ?",
                (False, property_code)
            )

        return result

    # Lookup Data Functions
    def get_main_codes_by_type(self, record_type):
        """
        Get main codes by record type.

        Args:
            record_type (str): Record type code (e.g. '01', '02', '03', etc.)

        Returns:
            list: List of dictionaries containing Code and Name
        """
        return self.db.execute_query(
            "SELECT DISTINCT code, name FROM Maincode WHERE recty = ? ORDER BY name",
            (record_type,)
        )

    def get_provinces(self):
        """Get all provinces."""
        return self.get_main_codes_by_type('01')

    def get_cities(self):
        """Get all cities."""
        return self.get_main_codes_by_type('02')

    def get_property_types(self):
        """Get all property types."""
        return self.get_main_codes_by_type('03')

    def get_building_types(self):
        """Get all building types."""
        return self.get_main_codes_by_type('04')

    def get_unit_measures(self):
        """Get all unit measures."""
        return self.get_main_codes_by_type('05')

    def get_offer_types(self):
        """Get all offer types."""
        return self.get_main_codes_by_type('06')

    def add_main_code(self, record_type, code, name, description=None):
        """
        Add a new main code.

        Args:
            record_type (str): Record type code
            code (str): Full classification code
            name (str): Name
            description (str, optional): Description

        Returns:
            bool: True if successful, False otherwise
        """
        return self.db.execute_query(
            "INSERT INTO Maincode (recty, code, name, description) VALUES (?, ?, ?, ?)",
            (record_type, code, name, description)
        )

    # Company Information Functions

    def get_company_info(self, company_code=None):
        """
        Get company information.

        Args:
            company_code (str, optional): Company code

        Returns:
            dict: Company information if successful, None otherwise
        """
        code = company_code or self.company_code
        if not code:
            return None

        companies = self.db.execute_query(
            "SELECT * FROM Companyinfo WHERE Companyco = ?",
            (code,)
        )

        return companies[0] if companies else None

    def set_company_info(self, company_data):
        """
        Set company information.

        Args:
            company_data (dict): Company data

        Returns:
            bool: True if successful, False otherwise
        """
        # Check if company exists
        company_code = company_data.get('Companyco')
        if not company_code:
            return False

        existing = self.db.execute_query(
            "SELECT COUNT(*) as count FROM Companyinfo WHERE Companyco = ?",
            (company_code,)
        )

        if existing[0]['count'] > 0:
            # Update existing company
            set_clause = ', '.join([f"{k} = ?" for k in company_data.keys() if k != 'Companyco'])

            query = f"UPDATE Companyinfo SET {set_clause} WHERE Companyco = ?"

            # Add company_code to the values
            values = [company_data[k] for k in company_data.keys() if k != 'Companyco']
            values.append(company_code)

            return self.db.execute_query(query, tuple(values))
        else:
            # Insert new company
            fields = ', '.join(company_data.keys())
            placeholders = ', '.join(['?' for _ in company_data.keys()])

            query = f"INSERT INTO Companyinfo ({fields}) VALUES ({placeholders})"

            return self.db.execute_query(query, tuple(company_data.values()))

    # Search & Report Functions

    def search_properties(self, search_criteria):
        """
        Search properties based on criteria.

        Args:
            search_criteria (dict): Search criteria

        Returns:
            list: List of properties matching the criteria
        """
        where_clauses = []
        values = []

        # Build WHERE clause based on search criteria
        for field, value in search_criteria.items():
            if value is not None and value != "":
                if isinstance(value, str) and '%' in value:
                    # For LIKE searches
                    where_clauses.append(f'"{field}" LIKE ?' if '-' in field else f"{field} LIKE ?")
                else:
                    # For exact matches
                    where_clauses.append(f'"{field}" = ?' if '-' in field else f"{field} = ?")
                values.append(value)

        # Default query if no criteria provided
        if not where_clauses:
            return self.get_all_properties()

        # Build the full query
        where_clause = " AND ".join(where_clauses)

        query = f"""
            SELECT r.*, o.ownername, m1.name as property_type, m2.name as building_type
            FROM Realstatspecification r
            LEFT JOIN Owners o ON r.Ownercode = o.Ownercode
            LEFT JOIN Maincode m1 ON r.Rstatetcode = m1.code AND m1.recty = '03'
            LEFT JOIN Maincode m2 ON r.Buildtcode = m2.code AND m2.recty = '04'
            WHERE {where_clause}
            ORDER BY r.realstatecode
        """

        return self.db.execute_query(query, tuple(values))    # Database Validation Functions

    def validate_database_integrity(self):
        """
        Validate database integrity and foreign key constraints.

        Returns:
            bool: True if database is valid, False otherwise
        """
        try:
            # Check if all required tables exist
            required_tables = ['Maincode', 'Realstatspecification', 'Owners', 'Companyinfo', 'realstatephotos']
            for table in required_tables:
                result = self.db.execute_query(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table,)
                )
                if not result:
                    print(f"Missing required table: {table}")
                    return False

            # Check foreign key constraints by attempting a few test queries
            # This ensures the foreign keys are properly set up
            test_queries = [
                "SELECT COUNT(*) FROM Realstatspecification r LEFT JOIN Maincode m ON r.Rstatetcode = m.code",
                "SELECT COUNT(*) FROM Realstatspecification r LEFT JOIN Owners o ON r.Ownercode = o.Ownercode",
                "SELECT COUNT(*) FROM Companyinfo c LEFT JOIN Maincode m ON c.Cityco = m.code"
            ]

            for query in test_queries:
                result = self.db.execute_query(query)
                if not result:
                    return False

            return True

        except Exception as e:
            print(f"Database validation error: {e}")
            return False

    def get_database_statistics(self):
        """
        Get database statistics.

        Returns:
            dict: Database statistics
        """
        stats = {}

        try:
            # Count records in each table
            tables = ['Maincode', 'Realstatspecification', 'Owners', 'Companyinfo', 'realstatephotos']

            for table in tables:
                result = self.db.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                stats[table] = result[0]['count'] if result else 0

            # Get maincode breakdown by record type
            maincode_types = self.db.execute_query(
                "SELECT recty, COUNT(*) as count FROM Maincode GROUP BY recty ORDER BY recty"
            )
            stats['maincode_by_type'] = {item['recty']: item['count'] for item in maincode_types}

            return stats

        except Exception as e:
            print(f"Error getting database statistics: {e}")
            return {}

# Create a singleton instance of the API
api = DatabaseAPI()

def get_api():
    """Get the API instance."""
    return api
