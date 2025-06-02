"""
Script to fix dropdown key issues in property_management.py
"""
import os
import re

def fix_dropdown_keys():
    file_path = 'src/screens/property_management.py'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace uppercase Code and Name keys with lowercase in various dropdown generation code
    patterns = [
        (r't\.get\(\'Code\', \'N/A\'\)', r't.get(\'code\', \'N/A\')'),
        (r't\.get\(\'Name\', \'Unknown\'\)', r't.get(\'name\', \'Unknown\')'),
        (r'p\.get\(\'Code\', \'N/A\'\)', r'p.get(\'code\', \'N/A\')'),
        (r'p\.get\(\'Name\', \'Unknown\'\)', r'p.get(\'name\', \'Unknown\')'),
        (r'c\.get\(\'Code\', \'N/A\'\)', r'c.get(\'code\', \'N/A\')'),
        (r'c\.get\(\'Name\', \'Unknown\'\)', r'c.get(\'name\', \'Unknown\')'),
        (r'o\.get\(\'Ownercode\', \'N/A\'\)', r'o.get(\'ownercode\', \'N/A\')'),
        (r'pt\.get\(\'Code\', \'N/A\'\)', r'pt.get(\'code\', \'N/A\')'),
        (r'pt\.get\(\'Name\', \'Unknown\'\)', r'pt.get(\'name\', \'Unknown\')'),
        (r'bt\.get\(\'Code\', \'N/A\'\)', r'bt.get(\'code\', \'N/A\')'),
        (r'bt\.get\(\'Name\', \'Unknown\'\)', r'bt.get(\'name\', \'Unknown\')'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated dropdown keys in {file_path}")

    # Also check search_report.py
    search_file = 'src/screens/search_report.py'
    if os.path.exists(search_file):
        with open(search_file, 'r', encoding='utf-8') as f:
            content = f.read()

        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        with open(search_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Updated dropdown keys in {search_file}")

if __name__ == "__main__":
    fix_dropdown_keys()
