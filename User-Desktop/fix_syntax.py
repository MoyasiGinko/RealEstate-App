"""
Fix script for database API with better syntax handling.
"""
import os

def fix_database_api():
    # Path to database_api.py
    file_path = os.path.join('src', 'models', 'database_api.py')

    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Find and fix the problematic section
    for i in range(len(lines)):
        if '# Lookup Data Functions' in lines[i]:
            # Fix the line that contains both the comment and the method definition
            lines[i] = "    # Lookup Data Functions\n    def get_main_codes_by_type(self, record_type):\n"

        # Fix the line that has docstring and return statement
        if '"""        return self.db.execute_query(' in lines[i]:
            # Split into two lines
            lines[i] = '        """\n        return self.db.execute_query(\n'

    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)

    print(f"Fixed syntax issues in database_api.py")

if __name__ == "__main__":
    fix_database_api()
