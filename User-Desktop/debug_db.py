"""
Debug script for database API queries.
"""
import sqlite3
import os
from src.models.database_api import get_api

def test_db_directly():
    """Test the database directly with SQLite3."""
    db_path = os.path.join('data', 'local.db')
    print(f"Connecting to {db_path}")

    # Connect directly with SQLite3
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check Maincode table structure
    cursor.execute("PRAGMA table_info(Maincode)")
    print("\nMaincode table structure:")
    for column in cursor.fetchall():
        print(f"  {column['name']} ({column['type']})")

    # Test query for property types (recty = 03)
    cursor.execute("SELECT DISTINCT code, name FROM Maincode WHERE recty = '03' ORDER BY name")
    rows = cursor.fetchall()

    print("\nProperty types from direct query:")
    if rows:
        for row in rows:
            print(f"  Code: {row['code']}, Name: {row['name']}")
    else:
        print("  No property types found")

    # Check data in the Maincode table
    cursor.execute("SELECT * FROM Maincode LIMIT 10")
    rows = cursor.fetchall()

    print("\nSample data from Maincode table:")
    if rows:
        for row in rows:
            column_names = row.keys()
            values = [f"{col}: {row[col]}" for col in column_names]
            print(f"  {', '.join(values)}")
    else:
        print("  No data found in Maincode table")

    conn.close()

def test_api():
    """Test the database API."""
    api = get_api()
    api.connect()

    print("\nTesting property types via API:")
    property_types = api.get_property_types()
    if property_types:
        for t in property_types:
            print(f"  Code: {t.get('code')}, Name: {t.get('name')}")
    else:
        print("  No property types found via API")

if __name__ == "__main__":
    test_db_directly()
    test_api()
