"""
Script to fix escaping issues in property_management.py
"""
import os
import re

def fix_escaping_issues():
    file_path = 'src/screens/property_management.py'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use regex to find and replace all patterns of t.get(\'code\', \'N/A\') with t.get('code', 'N/A')
    pattern = r"([a-z])\.get\(\\\'([a-zA-Z]+)\\\', \\\'([a-zA-Z-]+)\\\'\)"
    replacement = r"\1.get('\2', '\3')"
    content = re.sub(pattern, replacement, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed escaping issues in {file_path}")

    # Also check search_report.py
    search_file = 'src/screens/search_report.py'
    if os.path.exists(search_file):
        with open(search_file, 'r', encoding='utf-8') as f:
            content = f.read()

        content = re.sub(pattern, replacement, content)

        with open(search_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Fixed escaping issues in {search_file}")

if __name__ == "__main__":
    fix_escaping_issues()
