#!/usr/bin/env python3
# filepath: e:\Github\Clients\Luay-Alkawaz\New-App\User-Desktop\check_db.py

"""
Script to check the database schema and test basic database operations.
"""

import os
import sys
from configs.database import DatabaseManager

def main():
    """Check database schema and test operations."""
    print("Checking database schema and testing operations...")

    # Initialize database manager
    db = DatabaseManager()

    # Connect to local database
    if not db.connect_local():
        print("Failed to connect to local database.")
        return

    print(f"Connected to local database at {db.db_path}")

    # Check table schema
    print("\nChecking table schema...")

    # Get schema for all tables
    tables = db.execute_query("SELECT name FROM sqlite_master WHERE type='table';")

    for table in tables:
        table_name = table['name']
        print(f"\nSchema for table: {table_name}")

        schema = db.execute_query(f"PRAGMA table_info({table_name});")

        for column in schema:
            print(f"  {column['name']} ({column['type']})")

    # Try to insert sample data
    print("\nTesting insertion of sample data...")

    # Insert sample owner if not exists
    owner_exists = db.execute_query("SELECT COUNT(*) as count FROM Owners WHERE Ownercode = ?", ('A123',))

    if owner_exists[0]['count'] == 0:
        db.execute_query(
            "INSERT INTO Owners (Ownercode, ownername, ownerphone, Note) VALUES (?, ?, ?, ?)",
            ('A123', 'Mohammed Khaled', '07812345678', 'Test owner')
        )
        print("Sample owner inserted")
    else:
        print("Sample owner already exists")

    # Test insertion of property data
    try:
        # Try without the Buildtcode column
        result = db.execute_query(
            """INSERT OR IGNORE INTO Realstatspecification (
                Companyco, realstatecode, Rstatetcode,
                "Property-area", "N-of-bedrooms", "N-of-bathrooms",
                "Property-corner", "Offer-Type-Code", Ownercode,
                "Property-address"
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ('E901', 'E901B7F2', '1', 145.75, 3, 2, True, '1', 'A123', 'Test Address')
        )
        print("Property inserted successfully without Buildtcode")
    except Exception as e:
        print(f"Error inserting property without Buildtcode: {e}")

    # Close connection
    db.close()
    print("\nDatabase check completed successfully.")

if __name__ == "__main__":
    main()
