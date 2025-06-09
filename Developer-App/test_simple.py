#!/usr/bin/env python3
"""
Simple database test script
"""

import sys
import os
import sqlite3
from pathlib import Path

def test_direct_database():
    """Test database connection directly"""
    print("🔌 Testing Direct Database Connection")
    print("=" * 40)

    try:
        # Create data directory
        data_dir = Path('./data')
        data_dir.mkdir(exist_ok=True)

        # Connect to SQLite database
        db_path = data_dir / 'app_database.db'
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row

        print(f"✓ Connected to database: {db_path}")

        # Create tables
        cursor = conn.cursor()

        # Create Companyinfo table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Companyinfo (
                Companyco TEXT PRIMARY KEY,
                Companyna TEXT,
                Cityco TEXT,
                Caddress TEXT,
                Cophoneno TEXT,
                Username TEXT,
                Password TEXT,
                SubscriptionTCode TEXT,
                Lastpayment TEXT,
                Subscriptionduration TEXT,
                Registrationdate TEXT,
                descriptions TEXT
            )
        """)

        # Create Maincode table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Maincode (
                recty TEXT,
                code TEXT,
                name TEXT,
                description TEXT
            )
        """)

        conn.commit()
        print("✓ Tables created successfully")

        # Test insert
        cursor.execute("""
            INSERT OR REPLACE INTO Companyinfo
            (Companyco, Companyna, Cityco)
            VALUES (?, ?, ?)
        """, ('TEST001', 'Test Company', 'Test City'))

        cursor.execute("""
            INSERT OR REPLACE INTO Maincode
            (recty, code, name, description)
            VALUES (?, ?, ?, ?)
        """, ('TYPE1', 'CODE001', 'Test Code', 'Test Description'))

        conn.commit()
        print("✓ Test data inserted")

        # Test select
        cursor.execute("SELECT * FROM Companyinfo WHERE Companyco = ?", ('TEST001',))
        company = cursor.fetchone()
        if company:
            print(f"✓ Company data: {dict(company)}")

        cursor.execute("SELECT * FROM Maincode WHERE code = ?", ('CODE001',))
        maincode = cursor.fetchone()
        if maincode:
            print(f"✓ MainCode data: {dict(maincode)}")

        # Clean up test data
        cursor.execute("DELETE FROM Companyinfo WHERE Companyco = ?", ('TEST001',))
        cursor.execute("DELETE FROM Maincode WHERE code = ?", ('CODE001',))
        conn.commit()
        print("✓ Test data cleaned up")

        conn.close()
        print("✓ Database connection closed")

        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Simple Database Test")
    print("=" * 50)

    success = test_direct_database()

    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)

    if success:
        print("✅ Database test PASSED")
        print("✅ Database schema is working correctly")
        sys.exit(0)
    else:
        print("❌ Database test FAILED")
        sys.exit(1)
