# Database Utilities

This folder contains essential database management utilities for the Real Estate application.

## Files

### 1. `create_database.py`

Creates a fresh database with updated schema including Maincode relations.

**Usage:**

```bash
python database_utils/create_database.py
```

**Features:**

- Creates database with proper foreign key relationships
- Uses schema from `configs/database.py`
- Handles locked database files by creating alternative names
- Implements UNIQUE constraint on Maincode.Code

### 2. `seed_data.py`

Manages sample data creation and loading with conflict resolution.

**Usage:**

```bash
# Create seed database with sample data
python database_utils/seed_data.py --create-seed

# Load seed data into main database (default: replace existing)
python database_utils/seed_data.py

# Load seed data and skip existing records
python database_utils/seed_data.py --skip-existing

# Load seed data into specific database
python database_utils/seed_data.py --load-seed data/target.db

# Smart merge: preserve existing data, only add missing records
python database_utils/seed_data.py --smart-merge data/local.db
```

**Conflict Resolution Options:**

1. **Replace Mode (default)**: Uses `INSERT OR REPLACE` to update existing records
2. **Skip Mode (`--skip-existing`)**: Uses `INSERT OR IGNORE` to skip duplicates
3. **Smart Merge (`--smart-merge`)**: Checks for existing records and only adds new ones

**Features:**

- Creates comprehensive sample data following Data_types.md specifications
- 31 Maincode records (countries, cities, property types, etc.)
- Sample companies, owners, properties, and photos
- Proper foreign key relationships
- Loads data in correct order to respect constraints
- Handles unique constraint conflicts gracefully

## Sample Data Structure

### Maincode Records (31 total)

- **Countries (recty='01')**: Iraq, Jordan, Syria, Lebanon, Turkey
- **Cities (recty='02')**: Baghdad, Basra, Erbil, Mosul, Najaf, Amman, Zarqa
- **Property Types (recty='03')**: Residential, Commercial, Industrial, Agricultural, Mixed Use
- **Building Types (recty='04')**: House, Apartment, Villa, Office, Shop, Warehouse
- **Unit Specifications (recty='05')**: Studio, 1-4+ Bedroom
- **Offer Types (recty='06')**: For Sale, For Rent, For Lease

### Sample Records

- **1 Company**: Best Real Estate (E901)
- **5 Owners**: A001-A005 with realistic contact information
- **5 Properties**: Various types with proper foreign key references
- **8 Photos**: Sample property images

## Quick Start

1. **Create fresh database:**

   ```bash
   python database_utils/create_database.py
   ```

2. **Load sample data:**

   ```bash
   python database_utils/seed_data.py
   ```

3. **Verify data loaded:**
   Your database will now contain all sample data with proper relationships.
