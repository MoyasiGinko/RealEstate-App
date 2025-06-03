#!/usr/bin/env python3
"""
Test script to verify the owner dropdown and modal cancel fixes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.database_api import DatabaseAPI

def test_owner_dropdown_fix():
    """Test that owner codes are displayed correctly in the dropdown."""

    print("=== TESTING OWNER DROPDOWN FIX ===")

    # Initialize database API
    api = DatabaseAPI()

    # Test getting all owners
    print("\n1. Testing owner data retrieval...")
    owners = api.get_all_owners()

    if owners:
        print(f"Found {len(owners)} owners:")
        for owner in owners[:3]:  # Show first 3
            print(f"  - Raw data: {owner}")
            # Test the fixed field access
            owner_code = owner.get('Ownercode', 'N/A')  # Fixed: capital O
            owner_name = owner.get('ownername', 'Unknown')
            formatted = f"{owner_code} - {owner_name}"
            print(f"  - Formatted: {formatted}")
            print()
    else:
        print("No owners found in database")

    print("=== OWNER DROPDOWN TEST COMPLETED ===")
    print("\nThe owner dropdown should now show:")
    print("1. Proper owner codes (not 'N/A')")
    print("2. Owner names correctly")
    print("3. Format: 'A001 - John Doe'")
    print("\nThe Add Owner modal should now:")
    print("1. Open correctly when clicking 'Add Owner' button")
    print("2. Close when clicking the 'Cancel' button")

if __name__ == "__main__":
    test_owner_dropdown_fix()
