"""
Fix script for database API.
"""
import os
import sys

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def fix_database_api():
    # Path to database_api.py
    file_path = os.path.join('src', 'models', 'database_api.py')

    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()

    # Fix the method with lowercase column names
    old_query = 'SELECT DISTINCT Code, Name FROM Maincode WHERE Recty = ? ORDER BY Name'
    new_query = 'SELECT DISTINCT code, name FROM Maincode WHERE recty = ? ORDER BY name'

    # Replace the query
    content = content.replace(old_query, new_query)

    # Fix insert query with lowercase column names
    old_insert = 'INSERT INTO Maincode (Recty, Code, Name, Description) VALUES (?, ?, ?, ?)'
    new_insert = 'INSERT INTO Maincode (recty, code, name, description) VALUES (?, ?, ?, ?)'

    # Replace the insert query
    content = content.replace(old_insert, new_insert)

    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(content)

    print(f"Updated database_api.py with lowercase column names")

if __name__ == "__main__":
    fix_database_api()
