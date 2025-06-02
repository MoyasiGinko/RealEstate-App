#!/usr/bin/env python3
# filepath: e:\Github\Clients\Luay-Alkawaz\New-App\User-Desktop\test_insert.py

"""
Script to test inserting data into the database with the correct column names.
"""

import os
import sys
from configs.database import DatabaseManager

def main():
    """Test inserting data with correct column names."""
    print("Testing data insertion with correct column names...")

    # Initialize database manager
    db = DatabaseManager()

    # Connect to local database
    if not db.connect_local():
        print("Failed to connect to local database.")
        return

    print(f"Connected to local database at {db.db_path}")

    # Try to insert sample data
    print("\nTesting insertion of sample data...")

    # Insert sample owner if not exists
    owner_exists = db.execute_query("SELECT COUNT(*) as count FROM Owners WHERE Ownercode = ?", ('A124',))

    if owner_exists[0]['count'] == 0:
        db.execute_query(
            "INSERT INTO Owners (Ownercode, ownername, ownerphone, Note) VALUES (?, ?, ?, ?)",
            ('A124', 'Ali Hassan', '07701234567', 'Test owner 2')
        )
        print("Sample owner inserted")
    else:
        print("Sample owner already exists")

    # Test insertion of property data with correct column names
    try:
        # Use the exact column names from the schema
        result = db.execute_query(
            """INSERT OR IGNORE INTO Realstatspecification (
                Companyco, realstatecode, Rstatetcode, Buildtcode,
                "Property-area", "N-of-bedrooms", "N-of bathrooms",
                "Property-corner", "Offer-Type-Code", Ownercode,
                "Property-address"
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ('E901', 'E901C7F2', '1', '1', 160.25, 4, 3, True, '1', 'A124', 'Another Test Address')
        )
        print("Property inserted successfully with correct column names")
    except Exception as e:
        print(f"Error inserting property: {e}")

    # Query and display data to verify
    print("\nQuerying data to verify...")

    # Query properties
    properties = db.execute_query("SELECT * FROM Realstatspecification")
    print("\nProperties:")
    for prop in properties:
        print(f"  {prop['realstatecode']} - Owner: {prop['Ownercode']} - Area: {prop['Property-area']} m²")

    # Close connection
    db.close()
    print("\nData insertion test completed successfully.")

if __name__ == "__main__":
    main()
