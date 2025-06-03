#!/usr/bin/env python3
"""
Seed Data Loader Utility
Loads sample data from seed.db into the main database.
"""

import os
import sqlite3
import sys

def create_seed_database():
    """Create seed database with sample data following Data_types.md specifications."""
    print("Creating seed database with sample data...")

    seed_db_path = "data/seed.db"

    # Ensure data directory exists
    os.makedirs(os.path.dirname(seed_db_path), exist_ok=True)    # Remove existing seed database
    if os.path.exists(seed_db_path):
        try:
            os.remove(seed_db_path)
            print(f"✓ Removed existing seed database")
        except OSError as e:
            print(f"⚠️  Could not remove existing seed database: {e}")
            # Create with different name if locked
            seed_db_path = seed_db_path.replace('.db', '_new.db')
            print(f"✓ Creating seed database with new name: {seed_db_path}")

    try:
        conn = sqlite3.connect(seed_db_path)
        cursor = conn.cursor()

        # Create tables (same structure as main database)
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS Maincode (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recty CHAR(2),
                Code CHAR(16) UNIQUE,
                Desc TEXT
            );

            CREATE TABLE IF NOT EXISTS Companyinfo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                companycode CHAR(16),
                companyname TEXT,
                ownername TEXT,
                phone TEXT,
                email TEXT,
                address TEXT
            );

            CREATE TABLE IF NOT EXISTS Owners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Ownercode CHAR(16),
                ownername TEXT,
                phone TEXT,
                email TEXT,
                address TEXT
            );

            CREATE TABLE IF NOT EXISTS Realstatspecification (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Realstate_name TEXT,
                property_type CHAR(16),
                Building_type CHAR(16),
                Unit_specification CHAR(16),
                offer_type CHAR(16),
                owner_id INTEGER,
                province CHAR(16),
                city CHAR(16),
                district TEXT,
                street TEXT,
                alley TEXT,
                house_number TEXT,
                area_m2 REAL,
                rooms_count INTEGER,
                price REAL,
                description TEXT,
                FOREIGN KEY (property_type) REFERENCES Maincode(Code),
                FOREIGN KEY (Building_type) REFERENCES Maincode(Code),
                FOREIGN KEY (Unit_specification) REFERENCES Maincode(Code),
                FOREIGN KEY (offer_type) REFERENCES Maincode(Code),
                FOREIGN KEY (province) REFERENCES Maincode(Code),
                FOREIGN KEY (city) REFERENCES Maincode(Code)
            );

            CREATE TABLE IF NOT EXISTS realstatephotos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                realstate_id INTEGER,
                photo_path TEXT,
                FOREIGN KEY (realstate_id) REFERENCES Realstatspecification(id)
            );
        ''')

        # Insert Maincode data (following Data_types.md)
        maincode_data = [
            # Countries (recty='01')
            ('01', '001', 'Iraq'),
            ('01', '002', 'Jordan'),
            ('01', '003', 'Syria'),
            ('01', '004', 'Lebanon'),
            ('01', '005', 'Turkey'),

            # Cities (recty='02', format: country+city)
            ('02', '00101', 'Baghdad'),
            ('02', '00102', 'Basra'),
            ('02', '00103', 'Erbil'),
            ('02', '00104', 'Mosul'),
            ('02', '00105', 'Najaf'),
            ('02', '00201', 'Amman'),
            ('02', '00202', 'Zarqa'),

            # Property Types (recty='03')
            ('03', '001', 'Residential'),
            ('03', '002', 'Commercial'),
            ('03', '003', 'Industrial'),
            ('03', '004', 'Agricultural'),
            ('03', '005', 'Mixed Use'),

            # Building Types (recty='04')
            ('04', '001', 'House'),
            ('04', '002', 'Apartment'),
            ('04', '003', 'Villa'),
            ('04', '004', 'Office'),
            ('04', '005', 'Shop'),
            ('04', '006', 'Warehouse'),

            # Unit Specifications (recty='05')
            ('05', '001', 'Studio'),
            ('05', '002', '1 Bedroom'),
            ('05', '003', '2 Bedroom'),
            ('05', '004', '3 Bedroom'),
            ('05', '005', '4+ Bedroom'),

            # Offer Types (recty='06')
            ('06', '001', 'For Sale'),
            ('06', '002', 'For Rent'),
            ('06', '003', 'For Lease')
        ]

        cursor.executemany('INSERT OR REPLACE INTO Maincode (recty, Code, Desc) VALUES (?, ?, ?)', maincode_data)

        # Insert sample company
        cursor.execute('''
            INSERT INTO Companyinfo (companycode, companyname, ownername, phone, email, address)
            VALUES ('E901', 'Best Real Estate', 'Ahmed Al-Kawaz', '+964-770-123-4567', 'info@bestrealestate.iq', 'Baghdad, Iraq')
        ''')

        # Insert sample owners
        owners_data = [
            ('A001', 'Mohammed Hassan', '+964-770-111-2222', 'mohammed@email.com', 'Baghdad, Al-Karkh'),
            ('A002', 'Fatima Ahmed', '+964-770-333-4444', 'fatima@email.com', 'Baghdad, Al-Rusafa'),
            ('A003', 'Ali Karim', '+964-770-555-6666', 'ali@email.com', 'Basra, Hay Al-Andalus'),
            ('A004', 'Sarah Ibrahim', '+964-770-777-8888', 'sarah@email.com', 'Erbil, Ankawa'),
            ('A005', 'Omar Mahmoud', '+964-770-999-0000', 'omar@email.com', 'Najaf, City Center')
        ]

        cursor.executemany('INSERT INTO Owners (Ownercode, ownername, phone, email, address) VALUES (?, ?, ?, ?, ?)', owners_data)

        # Insert sample properties
        properties_data = [
            ('Modern Villa in Baghdad', '001', '003', '005', '001', 1, '001', '00101', 'Al-Karkh', 'Al-Mansour', 'Street 14', '25', 350.0, 4, 250000.0, 'Beautiful modern villa with garden'),
            ('Downtown Apartment', '001', '002', '003', '002', 2, '001', '00101', 'Al-Rusafa', 'Al-Karrada', 'Street 62', '18', 120.0, 2, 800.0, 'Furnished apartment in city center'),
            ('Commercial Shop', '002', '005', '001', '001', 3, '001', '00102', 'Hay Al-Andalus', 'Main Street', 'Commercial Complex', '5', 80.0, 1, 180000.0, 'Prime location shop'),
            ('Family House', '001', '001', '004', '002', 4, '001', '00103', 'Ankawa', 'Christian Quarter', 'Street 7', '12', 200.0, 3, 1200.0, 'Spacious family house'),
            ('Investment Property', '003', '006', '001', '003', 5, '001', '00104', 'Industrial Zone', 'Factory Street', 'Warehouse District', '1', 500.0, 1, 150000.0, 'Great for storage business')
        ]

        cursor.executemany('''
            INSERT INTO Realstatspecification
            (Realstate_name, property_type, Building_type, Unit_specification, offer_type, owner_id, province, city, district, street, alley, house_number, area_m2, rooms_count, price, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', properties_data)

        # Insert sample photos
        photos_data = [
            (1, 'images/properties/villa1_main.jpg'),
            (1, 'images/properties/villa1_garden.jpg'),
            (2, 'images/properties/apt1_living.jpg'),
            (2, 'images/properties/apt1_kitchen.jpg'),
            (3, 'images/properties/shop1_front.jpg'),
            (4, 'images/properties/house1_exterior.jpg'),
            (4, 'images/properties/house1_interior.jpg'),
            (5, 'images/properties/warehouse1.jpg')
        ]

        cursor.executemany('INSERT INTO realstatephotos (realstate_id, photo_path) VALUES (?, ?)', photos_data)

        conn.commit()
        conn.close()

        print(f"✓ Seed database created successfully: {seed_db_path}")
        print("✓ Sample data includes:")
        print("  - 31 Maincode records (countries, cities, property types, etc.)")
        print("  - 1 sample company")
        print("  - 5 sample owners")
        print("  - 5 sample properties")
        print("  - 8 sample property photos")

        return seed_db_path

    except Exception as e:
        print(f"✗ Error creating seed database: {e}")
        return None

def load_seed_data(target_db="data/local.db", replace_existing=True):
    """Load seed data from seed.db into target database.

    Args:
        target_db: Path to target database
        replace_existing: If True, replace existing records with same unique keys.
                         If False, skip existing records (INSERT OR IGNORE).
    """
    print(f"Loading seed data into: {target_db}")
    print(f"Strategy: {'Replace existing' if replace_existing else 'Skip existing'} records")

    seed_db_path = "data/seed.db"

    # Create seed database if it doesn't exist
    if not os.path.exists(seed_db_path):
        print("Seed database not found. Creating it...")
        create_seed_database()

    if not os.path.exists(target_db):
        print(f"✗ Target database not found: {target_db}")
        return False

    try:
        # Connect to both databases
        main_conn = sqlite3.connect(target_db)
        main_conn.row_factory = sqlite3.Row
        main_cursor = main_conn.cursor()

        seed_conn = sqlite3.connect(seed_db_path)
        seed_conn.row_factory = sqlite3.Row
        seed_cursor = seed_conn.cursor()

        print("✓ Connected to both databases")

        # Load data in correct order (respecting foreign keys)
        tables_order = ['Maincode', 'Companyinfo', 'Owners', 'Realstatspecification', 'realstatephotos']

        # Define which strategy to use for each table
        insert_strategy = "INSERT OR REPLACE" if replace_existing else "INSERT OR IGNORE"

        for table in tables_order:
            print(f"Loading {table} data...")

            # Get data from seed database
            seed_cursor.execute(f'SELECT * FROM {table}')
            rows = seed_cursor.fetchall()

            if not rows:
                print(f"  No data in {table}")
                continue

            # Insert/Update seed data with conflict resolution
            inserted_count = 0
            skipped_count = 0

            for row in rows:
                row_dict = dict(row)
                fields = ', '.join([f'"{k}"' if '-' in k else k for k in row_dict.keys()])
                placeholders = ', '.join(['?' for _ in row_dict.keys()])
                query = f'{insert_strategy} INTO {table} ({fields}) VALUES ({placeholders})'

                try:
                    cursor_result = main_cursor.execute(query, tuple(row_dict.values()))
                    if cursor_result.rowcount > 0:
                        inserted_count += 1
                    else:
                        skipped_count += 1
                except sqlite3.IntegrityError as e:
                    print(f"    ⚠️  Skipped record due to constraint: {e}")
                    skipped_count += 1
                except Exception as e:
                    print(f"    ❌ Error inserting record: {e}")
                    skipped_count += 1

            if inserted_count > 0:
                print(f"  ✓ Inserted {inserted_count} records into {table}")
            if skipped_count > 0:
                print(f"  ⚠️  Skipped {skipped_count} records in {table} (already exist or constraint violation)")

        # Commit changes
        main_conn.commit()
        print('\n✓ All data committed to main database')

        # Close connections
        main_conn.close()
        seed_conn.close()

        print('✓ Seed data loaded successfully!')
        return True

    except Exception as e:
        print(f'✗ Error loading seed data: {e}')
        return False

def smart_merge_seed_data(target_db="data/local.db"):
    """Smart merge seed data: only add records that don't exist, preserve existing data.

    This function checks for existing records by unique constraints and only adds
    new records, preserving any existing data in the target database.
    """
    print(f"Smart merging seed data into: {target_db}")
    print("Strategy: Preserve existing data, only add missing records")

    seed_db_path = "data/seed.db"

    # Create seed database if it doesn't exist
    if not os.path.exists(seed_db_path):
        print("Seed database not found. Creating it...")
        create_seed_database()

    if not os.path.exists(target_db):
        print(f"✗ Target database not found: {target_db}")
        return False

    try:
        # Connect to both databases
        main_conn = sqlite3.connect(target_db)
        main_conn.row_factory = sqlite3.Row
        main_cursor = main_conn.cursor()

        seed_conn = sqlite3.connect(seed_db_path)
        seed_conn.row_factory = sqlite3.Row
        seed_cursor = seed_conn.cursor()

        print("✓ Connected to both databases")

        # Define table-specific merge strategies
        table_strategies = {
            'Maincode': {
                'check_field': 'Code',
                'check_query': 'SELECT COUNT(*) FROM Maincode WHERE Code = ?'
            },
            'Companyinfo': {
                'check_field': 'companycode',
                'check_query': 'SELECT COUNT(*) FROM Companyinfo WHERE companycode = ?'
            },
            'Owners': {
                'check_field': 'Ownercode',
                'check_query': 'SELECT COUNT(*) FROM Owners WHERE Ownercode = ?'
            },
            'Realstatspecification': {
                'check_field': 'id',
                'check_query': 'SELECT COUNT(*) FROM Realstatspecification WHERE Realstate_name = ? AND owner_id = ?'
            },
            'realstatephotos': {
                'check_field': 'photo_path',
                'check_query': 'SELECT COUNT(*) FROM realstatephotos WHERE photo_path = ?'
            }
        }

        tables_order = ['Maincode', 'Companyinfo', 'Owners', 'Realstatspecification', 'realstatephotos']

        for table in tables_order:
            print(f"Smart merging {table} data...")

            # Get data from seed database
            seed_cursor.execute(f'SELECT * FROM {table}')
            rows = seed_cursor.fetchall()

            if not rows:
                print(f"  No data in {table}")
                continue

            strategy = table_strategies.get(table)
            if not strategy:
                print(f"  ⚠️  No merge strategy defined for {table}, skipping...")
                continue

            inserted_count = 0
            skipped_count = 0

            for row in rows:
                row_dict = dict(row)

                # Check if record already exists
                exists = False
                try:
                    if table == 'Realstatspecification':
                        # Special case for properties - check by name and owner
                        main_cursor.execute(strategy['check_query'],
                                          (row_dict.get('Realstate_name'), row_dict.get('owner_id')))
                    else:
                        # Standard check by unique field
                        check_value = row_dict.get(strategy['check_field'])
                        if check_value:
                            main_cursor.execute(strategy['check_query'], (check_value,))
                        else:
                            exists = False

                    if not exists:
                        count = main_cursor.fetchone()[0]
                        exists = count > 0
                except Exception as e:
                    print(f"    ⚠️  Error checking existing record: {e}")
                    exists = False

                if exists:
                    skipped_count += 1
                    continue

                # Insert new record
                try:
                    fields = ', '.join([f'"{k}"' if '-' in k else k for k in row_dict.keys()])
                    placeholders = ', '.join(['?' for _ in row_dict.keys()])
                    query = f'INSERT INTO {table} ({fields}) VALUES ({placeholders})'
                    main_cursor.execute(query, tuple(row_dict.values()))
                    inserted_count += 1
                except Exception as e:
                    print(f"    ❌ Error inserting record: {e}")
                    skipped_count += 1

            if inserted_count > 0:
                print(f"  ✓ Added {inserted_count} new records to {table}")
            if skipped_count > 0:
                print(f"  ⚠️  Skipped {skipped_count} existing records in {table}")

        # Commit changes
        main_conn.commit()
        print('\n✓ All changes committed to main database')

        # Close connections
        main_conn.close()
        seed_conn.close()

        print('✓ Smart merge completed successfully!')
        return True

    except Exception as e:
        print(f'✗ Error during smart merge: {e}')
        return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Database seed utilities')
    parser.add_argument('--create-seed', action='store_true', help='Create seed database')
    parser.add_argument('--load-seed', help='Load seed data into specified database')
    parser.add_argument('--smart-merge', help='Smart merge seed data (preserve existing)')
    parser.add_argument('--skip-existing', action='store_true',
                       help='Skip existing records instead of replacing them (default: replace)')

    args = parser.parse_args()

    if args.create_seed:
        create_seed_database()
    elif args.smart_merge:
        smart_merge_seed_data(args.smart_merge)
    elif args.load_seed:
        replace_existing = not args.skip_existing
        load_seed_data(args.load_seed, replace_existing)
    else:
        # Default: load seed data into main database
        replace_existing = not args.skip_existing
        load_seed_data(replace_existing=replace_existing)