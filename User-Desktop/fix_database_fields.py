"""
Script to fix uppercase field references in database_api.py
"""
import os
import re

def fix_database_api():
    file_path = 'src/models/database_api.py'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace uppercase table field references with lowercase
    replacements = [
        (r'SELECT \* FROM Owners', r'SELECT * FROM Owners'),  # Keep this as is - table name
        (r'SELECT \* FROM Realstatspecification', r'SELECT * FROM Realstatspecification'),  # Keep this as is - table name
        (r'INSERT INTO Maincode \(Recty, Code, Name, Description\)', r'INSERT INTO Maincode (recty, code, name, description)'),
        (r'INSERT OR IGNORE INTO Maincode \(Recty, Code, Name, Description\)', r'INSERT OR IGNORE INTO Maincode (recty, code, name, description)'),
        (r'm1\.Code', r'm1.code'),
        (r'm1\.Name', r'm1.name'),
        (r'm1\.Recty', r'm1.recty'),
        (r'm2\.Code', r'm2.code'),
        (r'm2\.Name', r'm2.name'),
        (r'm2\.Recty', r'm2.recty'),
    ]

    for old, new in replacements:
        content = re.sub(old, new, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated field references in {file_path}")

if __name__ == "__main__":
    fix_database_api()
