"""
Fix all escaped quotes in Python files.
"""
import os
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find f-strings with escaped quotes
    modified = False
    pattern = r"f\".*?{([^}]*?)\\\'([^\']*?)\\\'([^}]*?)}.*?\""
    while re.search(pattern, content):
        content = re.sub(pattern, r'f".*?{\1\'\2\'\3}.*?"', content)
        modified = True

    # Also handle regular strings with escaped quotes
    pattern = r"\\\'([^\\\']*?)\\\'"
    while re.search(pattern, content):
        content = re.sub(pattern, r"'\1'", content)
        modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def fix_all_python_files(root_dir):
    fixed_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if fix_file(file_path):
                    fixed_files.append(file_path)
    return fixed_files

if __name__ == "__main__":
    fixed_files = fix_all_python_files('src')
    print(f"Fixed {len(fixed_files)} files:")
    for file in fixed_files:
        print(f"  - {file}")
