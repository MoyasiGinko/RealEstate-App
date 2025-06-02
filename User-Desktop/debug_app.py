"""
Debug runner for the Real Estate application.
"""
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_escaped_quotes(file_path):
    """Check a Python file for escaped quotes that might cause syntax errors."""
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f.readlines(), 1):
            if "\\\'" in line:
                print(f"Line {i}: Potential escaped quote issue:")
                print(f"    {line.strip()}")

def main():
    """Run checks and show debug info."""
    print("Running debug checks...")

    # Check property_management.py for escaped quotes
    property_management_path = os.path.join('src', 'screens', 'property_management.py')
    if os.path.exists(property_management_path):
        print(f"\nChecking {property_management_path} for escaped quotes:")
        check_escaped_quotes(property_management_path)

    # Check search_report.py for escaped quotes
    search_report_path = os.path.join('src', 'screens', 'search_report.py')
    if os.path.exists(search_report_path):
        print(f"\nChecking {search_report_path} for escaped quotes:")
        check_escaped_quotes(search_report_path)

    # Print database API query info
    print("\nDatabase configuration:")
    db_path = os.path.join('data', 'local.db')
    if os.path.exists(db_path):
        print(f"Database exists: {db_path}")
        # Get database size
        db_size = os.path.getsize(db_path) / 1024
        print(f"Database size: {db_size:.2f} KB")
    else:
        print(f"Database not found: {db_path}")

    print("\nDebugging complete.")

if __name__ == "__main__":
    main()
