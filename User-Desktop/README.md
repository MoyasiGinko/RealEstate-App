# Real Estate Management System

A desktop application for managing real estate properties, built with Python and Kivy.

## Project Structure

```
├── src/                    # Application source code
│   ├── main.py            # Main application entry point
│   ├── models/            # Data models and database API
│   ├── screens/           # UI screens and forms
│   ├── utils/             # Utility functions
│   └── widgets/           # Custom UI widgets
├── assets/                # Application assets
│   ├── images/           # Image files
│   └── kv/               # Kivy UI definition files
├── configs/              # Configuration files
│   ├── database.py       # Database configuration
│   └── settings.py       # Application settings
├── data/                 # Database files
├── database_utils/       # Database management utilities
├── tests/                # Test files
└── requirements.txt      # Python dependencies
```

## Features

- Property management (CRUD operations)
- Owner management
- Property search and reporting
- Photo management for properties
- Settings configuration
- Dashboard with statistics

## Database

The application uses SQLite with the following main tables:

- **Maincode**: Classification codes (countries, cities, property types, etc.)
- **Realstatspecification**: Property details
- **Owners**: Property owner information
- **Companyinfo**: Company information
- **realstatephotos**: Property photos

## Quick Start

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up database:**

   ```bash
   # Create fresh database with schema
   python database_utils/create_database.py

   # Load sample data
   python database_utils/seed_data.py
   ```

3. **Run application:**
   ```bash
   python src/main.py
   ```

## Database Management

Use the utilities in `database_utils/` folder:

- `create_database.py`: Creates fresh database with proper schema
- `seed_data.py`: Manages sample data creation and loading

See `database_utils/README.md` for detailed usage instructions.

## Requirements

- Python 3.7+
- Kivy 2.0+
- SQLite3 (included with Python)

## License

This project is developed for Luay Al-Kawaz clients.
