#!/usr/bin/env python3
"""
Quick test script to verify database operations are working
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_database_contents():
    """Check what's in the database"""
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'local.db')

    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return

    print(f"✅ Database file found: {db_path}")
    print(f"📏 Database file size: {os.path.getsize(db_path)} bytes")
    print(f"🕐 Last modified: {datetime.fromtimestamp(os.path.getmtime(db_path))}")
    print()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📊 Tables in database: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
        print()

        # Check some data
        tables_to_check = ['Maincode', 'Owners', 'Realstatspecification', 'Companyinfo']
        for table in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"📈 {table}: {count} records")
            except sqlite3.OperationalError as e:
                print(f"⚠️  {table}: Error - {e}")

        conn.close()

    except Exception as e:
        print(f"❌ Error checking database: {e}")

def check_backups():
    """Check backup directory"""
    backup_dir = os.path.join(os.path.dirname(__file__), 'data', 'backups')

    if not os.path.exists(backup_dir):
        print("📁 No backups directory found")
        return

    backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
    print(f"💾 Backup files found: {len(backups)}")
    for backup in sorted(backups):
        backup_path = os.path.join(backup_dir, backup)
        size = os.path.getsize(backup_path)
        modified = datetime.fromtimestamp(os.path.getmtime(backup_path))
        print(f"   - {backup} ({size} bytes, {modified})")

if __name__ == "__main__":
    print("🔍 Database Operations Test")
    print("=" * 50)
    check_database_contents()
    print()
    check_backups()
    print()
    print("💡 Run this script after each database operation to see changes!")
