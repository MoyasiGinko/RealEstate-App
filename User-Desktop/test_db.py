#!/usr/bin/env python3
# filepath: e:\Github\Clients\Luay-Alkawaz\New-App\User-Desktop\test_db.py

"""
Simple script to test the database connection and initialization.
This script creates the database, creates tables, and inserts sample data.
"""

import os
import sys
from configs.database import DatabaseManager

def main():
    """Test the database connection and initialization."""
    print("Testing database connection and initialization...")

    # Initialize database manager
    db = DatabaseManager()

    # Connect to local database
    if not db.connect_local():
        print("Failed to connect to local database.")
        return

    print(f"Connected to local database at {db.db_path}")

    # Test connection
    if not db.test_connection():
        print("Failed to test database connection.")
        return

    # Create tables
    if not db.create_tables():
        print("Failed to create tables.")
        return

    print("Tables created successfully.")

    # Insert sample data
    print("Inserting sample data...")

    # Insert sample Maincode records
    maincode_data = [
        ('01', '01001', 'Iraq', 'Country Code'),
        ('01', '01002', 'Saudi Arabia', 'Country Code'),
        ('02', '02001', 'Baghdad', 'City Code'),
        ('03', '03001', 'Residential', 'Property Type'),
        ('03', '03002', 'Commercial', 'Property Type'),
        ('04', '04001', 'Apartment', 'Building Type'),
        ('04', '04002', 'House', 'Building Type'),
        ('05', '05001', 'Square Meter', 'Unit of Measurement'),
        ('06', '06001', 'For Sale', 'Offer Type'),
        ('06', '06002', 'For Rent', 'Offer Type')
    ]

    for record in maincode_data:
        db.execute_query(
            "INSERT OR IGNORE INTO Maincode (Recty, Code, Name, Description) VALUES (?, ?, ?, ?)",
            record
        )

    # Insert sample company
    db.execute_query(
        "INSERT OR IGNORE INTO Companyinfo (Companyco, Companyna, Cityco) VALUES (?, ?, ?)",
        ('E901', 'Best Real Estate', '02001')
    )

    # Insert sample owner
    db.execute_query(
        "INSERT OR IGNORE INTO Owners (Ownercode, ownername, ownerphone, Note) VALUES (?, ?, ?, ?)",
        ('A123', 'Mohammed Khaled', '07812345678', 'Sample owner')
    )

    # Insert sample property
    db.execute_query(
        """INSERT OR IGNORE INTO Realstatspecification (
            Companyco, realstatecode, Rstatetcode, Buildtcode,
            "Property-area", "N-of-bedrooms", "N-of-bathrooms",
            "Property-corner", "Offer-Type-Code", Ownercode,
            "Property-address"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        ('E901', 'E901A7F2', '1', '1', 145.75, 3, 2, True, '1', 'A123', 'Test Address')
    )

    # Query and display data to verify
    print("\nQuerying data to verify...")

    # Query owners
    owners = db.execute_query("SELECT * FROM Owners")
    print("\nOwners:")
    for owner in owners:
        print(f"  {owner['Ownercode']} - {owner['ownername']} - {owner['ownerphone']}")

    # Query properties
    properties = db.execute_query("SELECT * FROM Realstatspecification")
    print("\nProperties:")
    for prop in properties:
        print(f"  {prop['realstatecode']} - {prop['Ownercode']} - {prop['Property-area']} m²")

    # Close connection
    db.close()
    print("\nDatabase test completed successfully.")

if __name__ == "__main__":
    main()
