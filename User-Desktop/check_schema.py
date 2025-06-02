#!/usr/bin/env python3
# filepath: e:\Github\Clients\Luay-Alkawaz\New-App\User-Desktop\check_schema.py

"""
Script to check the actual schema of the SQLite database.
"""

import sqlite3
import os

def main():
    """Check the schema of the database."""
    # Get the path to the database file
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'local.db')

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get a list of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print(f"Tables in database: {db_path}")

    # For each table, get its schema
    for table in tables:
        table_name = table[0]
        print(f"\nSchema for table: {table_name}")

        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        for column in columns:
            cid, name, type_, notnull, dflt_value, pk = column
            print(f"  {cid}: {name} ({type_}), NotNull={notnull}, PK={pk}")

    # Close connection
    conn.close()

if __name__ == "__main__":
    main()
