#!/usr/bin/env python3
"""
Database Creation Utility
Creates a fresh database with updated schema including Maincode relations.
"""

import os
import sqlite3
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_fresh_database(db_path="data/local.db"):
    """Create a fresh database with updated schema."""
    print(f"Creating fresh database: {db_path}")

    try:
        # Import database configuration
        from configs.database import DatabaseManager

        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Remove existing database if it exists
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"✓ Removed existing database: {db_path}")
            except OSError as e:
                print(f"⚠️  Could not remove existing database: {e}")
                print("⚠️  Please close any applications using the database and try again")
                return None

        # Create new database using DatabaseManager
        db = DatabaseManager(db_path)
        if db.connect_local() and db.create_tables():
            print("✓ Database tables created successfully")
            db.close()
            return db_path
        else:
            print("✗ Failed to create tables")
            return None

    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return None

if __name__ == "__main__":
    db_path = create_fresh_database()
    if db_path:
        print(f"\n🎉 Database created successfully: {db_path}")
    else:
        print("\n❌ Database creation failed")