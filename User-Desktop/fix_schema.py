#!/usr/bin/env python3
# filepath: e:\Github\Clients\Luay-Alkawaz\New-App\User-Desktop\fix_schema.py

"""
Script to fix the schema discrepancies in the database.
"""

import os
import sys
import sqlite3

def main():
    """Fix schema discrepancies in the database."""
    print("Fixing schema discrepancies...")

    # Get the path to the database file
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'local.db')

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Print current schema
    print("\nCurrent schema for Realstatspecification table:")
    cursor.execute("PRAGMA table_info(Realstatspecification);")
    columns = cursor.fetchall()

    for column in columns:
        cid, name, type_, notnull, dflt_value, pk = column
        print(f"  {cid}: {name} ({type_}), NotNull={notnull}, PK={pk}")

    # Drop the table and recreate it with the correct schema
    try:
        print("\nDropping and recreating the Realstatspecification table...")

        # First, drop any foreign key constraints
        cursor.execute("PRAGMA foreign_keys = OFF;")

        # Drop the table
        cursor.execute("DROP TABLE IF EXISTS Realstatspecification;")

        # Recreate the table with the correct schema
        cursor.execute('''
        CREATE TABLE Realstatspecification (
            Companyco CHAR(4) NOT NULL,
            realstatecode CHAR(8) PRIMARY KEY,
            Rstatetcode CHAR(1),
            Yearmake DATE,
            Buildtcode CHAR(1),
            "Property-area" REAL,
            "Unitm-code" CHAR(1),
            "Property-facade" REAL,
            "Property-depth" REAL,
            "N-of-bedrooms" INTEGER,
            "N-of-bathrooms" INTEGER,
            "Property-corner" BOOLEAN,
            "Offer-Type-Code" CHAR(1),
            "Province-code" CHAR(2),
            "Region-code" CHAR(9),
            "Property-address" TEXT,
            Photosituation BOOLEAN,
            Ownercode CHAR(4),
            Descriptions TEXT,
            FOREIGN KEY (Ownercode) REFERENCES Owners(Ownercode),
            FOREIGN KEY (Companyco) REFERENCES Companyinfo(Companyco)
        )
        ''')

        # Re-enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")

        conn.commit()
        print("Table recreated successfully.")

        # Verify the new schema
        print("\nNew schema for Realstatspecification table:")
        cursor.execute("PRAGMA table_info(Realstatspecification);")
        columns = cursor.fetchall()

        for column in columns:
            cid, name, type_, notnull, dflt_value, pk = column
            print(f"  {cid}: {name} ({type_}), NotNull={notnull}, PK={pk}")

        # Test insertion
        print("\nTesting insertion with new schema...")
        cursor.execute('''
        INSERT INTO Realstatspecification (
            Companyco, realstatecode, Rstatetcode, Buildtcode,
            "Property-area", "N-of-bedrooms", "N-of-bathrooms",
            "Property-corner", "Offer-Type-Code", Ownercode,
            "Property-address"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('E901', 'E901D7F2', '1', '1', 180.50, 5, 3, True, '1', 'A124', 'Fixed Schema Test'))

        conn.commit()
        print("Test insertion successful.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()

    # Close connection
    conn.close()
    print("\nSchema fix completed.")

if __name__ == "__main__":
    main()
