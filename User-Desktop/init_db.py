"""
Database initialization script.
This script initializes the database with required tables and sample data.
"""

import os
import sys
from src.models.database_api import get_api

def main():
    """Initialize the database."""
    print("Initializing the database...")

    # Get the API instance
    api = get_api()

    # Connect to the database
    if not api.connect():
        print("Failed to connect to the database.")
        return False

    # Insert initial data
    if not api.insert_initial_data():
        print("Failed to insert initial data.")
        api.close()
        return False

    print("Database initialized successfully.")

    # Close the connection
    api.close()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
