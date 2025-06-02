# User Desktop App

## Overview

The User Desktop App is a Kivy-based application designed for managing real estate properties and owners. It provides a user-friendly interface for property management, owner management, reporting, and settings configuration.

## Features

- **Owner Management**: Add, edit, and delete property owners.
- **Property Management**: Manage property listings, including details such as type, area, and photos.
- **Search & Report**: Search properties based on various criteria and generate reports.
- **Settings**: Configure application settings and preferences.
- **Recent Activity**: Track recent actions performed within the application.

## Project Structure

```
user-desktop-app
├── src
│   ├── main.py
│   ├── screens
│   ├── widgets
│   ├── models
│   └── utils
├── configs
│   ├── database.py
│   └── settings.py
├── assets
│   ├── kv
│   └── images
├── tests
│   ├── test_database.py
│   └── test_models.py
├── data
│   └── local.db
├── requirements.txt
├── setup.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd user-desktop-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:

```
python src/main.py
```

## Database Setup

Before running the application, you need to initialize the database:

```
python init_db.py
```

This will create the necessary tables and insert initial reference data.

## Database API

The application uses a comprehensive database API located in `src/models/database_api.py`. This API provides methods for:

- Owner management (add, update, delete, query)
- Property management (add, update, delete, query)
- Photo management
- Reference data access
- Search functionality

Example usage:

```python
from src.models.database_api import get_api

# Get the API instance
api = get_api()

# Connect to the database
api.connect()

# Set the company code
api.set_company_code('E901')

# Get all owners
owners = api.get_all_owners()

# Close the connection when done
api.close()
```

## Configuration

Database connection settings can be configured in `configs/settings.py`. The application supports both local and cloud SQLite3 connections.

## Testing

To run the tests, use the following command:

```
python -m unittest discover tests
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
