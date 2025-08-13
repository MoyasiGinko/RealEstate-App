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

def create_fresh_database_safe(db_path="data/local.db"):
    """Create a fresh database with safe file handling for locked files."""
    print(f"Creating fresh database (safe mode): {db_path}")

    try:
        # Import database configuration
        from configs.database import DatabaseManager

        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Create a temporary database first
        temp_db_path = db_path + ".tmp"

        # Remove temp file if it exists
        if os.path.exists(temp_db_path):
            try:
                os.remove(temp_db_path)
            except OSError:
                pass

        # Create new database using DatabaseManager with temp path
        db = DatabaseManager(temp_db_path)
        if db.connect_local() and db.create_tables():
            print("✓ Database tables created successfully in temp file")
            db.close()

            # Now try to replace the original
            if os.path.exists(db_path):
                try:
                    # Try to remove the original
                    os.remove(db_path)
                    print(f"✓ Removed existing database: {db_path}")
                except OSError as e:
                    print(f"⚠️  Could not remove existing database: {e}")
                    # Instead of failing, try to backup the old one
                    import time
                    backup_path = db_path + f".backup_{int(time.time())}"
                    try:
                        os.rename(db_path, backup_path)
                        print(f"✓ Moved existing database to: {backup_path}")
                    except OSError as e2:
                        print(f"✗ Could not backup existing database: {e2}")
                        # Clean up temp file
                        if os.path.exists(temp_db_path):
                            os.remove(temp_db_path)
                        return None

            # Move temp file to final location
            os.rename(temp_db_path, db_path)
            print(f"✓ Database created successfully: {db_path}")
            return db_path
        else:
            print("✗ Failed to create tables")
            # Clean up temp file
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
            return None

    except Exception as e:
        print(f"✗ Error creating database: {e}")
        # Clean up temp file
        temp_db_path = db_path + ".tmp"
        if os.path.exists(temp_db_path):
            try:
                os.remove(temp_db_path)
            except OSError:
                pass
        return None


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