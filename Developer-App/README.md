# Developer Desktop App

A modern, professional Kivy desktop application demonstrating best practices for database management, API architecture, and UI design with support for cloud databases.

## 🏗️ Architecture Overview

This application follows a **3-layer architecture** with clear separation of concerns:

### 1. **Database Layer** (`src/core/database.py`)

- **SQLite database**: Local database for development and production
- **Connection management** with context managers and proper error handling
- **Automatic table creation** for CompanyInfo and MainCode tables
- **Robust error handling** and connection recovery

### 2. **API Layer** (`src/api/`)

- **Data Models** (`models.py`): Clean data transfer objects (DTOs)
- **Company API** (`company_api.py`): Full CRUD operations for company data
- **MainCode API** (`maincode_api.py`): Complete management of main codes with bulk operations
- **API Manager** (`api_manager.py`): Centralized access point with transaction handling
- **Standardized responses** for consistent error handling across the application

### 3. **Application Layer** (`src/`)

- **Modern UI** with dashboard, settings, and comprehensive database tools
- **Real-time monitoring** of database connections and data status
- **Professional widgets** including status bars and configuration dialogs
- **Export/Import functionality** for data management

## ✅ Current Status

✅ **COMPLETED**: Project cleanup and streamlining completed successfully!

### Core Features Working:

- **Database Layer**: SQLite-only implementation with proper connection management
- **API Layer**: CompanyInfo and MainCode CRUD operations fully functional
- **Application Layer**: Streamlined Kivy desktop application with proper navigation
- **UI Layer**: Main screen, dashboard, and settings screens working properly

### Test Results:

- ✅ Database connection and table creation
- ✅ CompanyInfo API operations (create, read, update, delete)
- ✅ MainCode API operations (create, read, update, delete)
- ✅ UI application starts without errors
- ✅ Navigation between screens working

### Files Cleaned/Removed:

- Removed demo files: `demo.py`, `QUICKSTART.md`, `launcher.py`, `setup.py`
- Removed test files: `test_basic.py`, `test_api.py`, `test_integration.py`
- Cleaned up unnecessary directories: `src/services`, `src/utils`, `config`, `assets`
- Removed unused components: `config_manager.py`, `window_manager.py`, `custom_toolbar.py`

### Files Fixed/Updated:

- **`src/core/database.py`**: Recreated as clean SQLite-only database manager
- **`src/app.py`**: Fixed imports and streamlined application class
- **`src/ui/screens/main_screen.py`**: Fixed syntax errors and simplified toolbar
- **`src/ui/screens/dashboard_screen.py`**: Fixed formatting and object access
- **`src/api/company_api.py`**: Added inline validation functions
- **`src/__init__.py`**: Cleaned up package imports

## 🚀 Features

### 📊 Dashboard Screen

- **Real-time data display** for companies and main codes
- **Connection status monitoring** with color-coded indicators
- **Database management tools** (backup, restore, optimize)
- **Data export/import** with multiple formats
- **Auto-refresh capabilities** for live data updates

### ⚙️ Settings Screen

- **Database configuration** interface
- **Connection testing** with detailed diagnostics
- **Multi-database support** (SQLite, MySQL, PostgreSQL)
- **Environment management** for different deployment scenarios

### 🔧 Status Bar

- **Real-time API connection monitoring**
- **Periodic connection health checks**
- **Visual status indicators** (Connected/Disconnected/Error)
- **Detailed connection information** display

## 📦 Installation

### Prerequisites

- **Python 3.8+** (tested with Python 3.13)
- **pip** for package management

### Quick Setup

```bash
# Clone the repository
git clone <repository-url>
cd Developer-App

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m src.app
```

### Database Setup

#### SQLite (Default - Ready to Use)

No additional setup required. Database file will be created automatically at `./data/app_database.db` with CompanyInfo and MainCode tables.

#### MySQL (Cloud/Production)

```bash
# Install MySQL connector
pip install mysql-connector-python

# Update .env file with MySQL configuration
DB_TYPE=mysql
MYSQL_HOST=your-mysql-host
MYSQL_PORT=3306
MYSQL_USER=your-username
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=developer_app
```

#### PostgreSQL (Cloud/Production)

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update .env file with PostgreSQL configuration
DB_TYPE=postgresql
POSTGRESQL_HOST=your-postgres-host
POSTGRESQL_PORT=5432
POSTGRESQL_USER=your-username
POSTGRESQL_PASSWORD=your-password
POSTGRESQL_DATABASE=developer_app
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# Application Settings
APP_TITLE=Developer Desktop App
APP_VERSION=1.0.0
DEBUG=False
LOG_LEVEL=INFO

# Database Configuration
DB_TYPE=sqlite  # sqlite, mysql, postgresql

# SQLite Configuration (Default)
DATABASE_PATH=./data/app_database.db

# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=developer_app

# PostgreSQL Configuration
POSTGRESQL_HOST=localhost
POSTGRESQL_PORT=5432
POSTGRESQL_USER=postgres
POSTGRESQL_PASSWORD=
POSTGRESQL_DATABASE=developer_app

# Cloud Database Examples
# AWS RDS MySQL
# MYSQL_HOST=your-rds-endpoint.amazonaws.com
# MYSQL_PORT=3306

# Google Cloud SQL PostgreSQL
# POSTGRESQL_HOST=your-project:region:instance-id
# POSTGRESQL_PORT=5432

# Azure Database
# MYSQL_HOST=your-server.mysql.database.azure.com
# MYSQL_PORT=3306
```

## 🧪 Testing

### Run Available Tests

```bash
# Core functionality test (recommended)
python test_core.py

# Simple database test
python test_simple.py
```

### Expected Test Results

- ✅ **Database Connection**: Validates SQLite database connectivity
- ✅ **API Functionality**: Tests CompanyInfo and MainCode CRUD operations
- ✅ **Data Persistence**: Tests data creation, retrieval, and deletion
- ✅ **Error Handling**: Validates proper error handling and responses

## 📚 API Usage

### Company Management

```python
from src.api import APIManager, CompanyInfo

# Initialize API
api = APIManager()
api.initialize()

# Create a company
company_data = {
    'company_code': 'COMP001',
    'company_name': 'Test Company',
    'city_code': 'NYC',
    'company_address': '123 Main St'
}
result = api.company.create_company(company_data)

# Get all companies
companies = api.company.get_all_companies()

# Search companies
search_results = api.company.search_companies("Test")

# Update company
update_data = {'company_name': 'Updated Company Name'}
api.company.update_company('COMP001', update_data)

# Delete company
api.company.delete_company('COMP001')
```

### MainCode Management

```python
# Create main code
maincode_data = {
    'main_code': 'CODE001',
    'record_type': 'TYPE1',
    'description': 'Test Code'
}
result = api.maincode.create_main_code(maincode_data)

# Get all main codes
codes = api.maincode.get_all_main_codes()

# Get by record type
type_codes = api.maincode.get_all_main_codes(record_type='TYPE1')

# Bulk operations
bulk_data = [
    {'main_code': 'CODE002', 'record_type': 'TYPE1'},
    {'main_code': 'CODE003', 'record_type': 'TYPE2'}
]
api.maincode.bulk_create_main_codes(bulk_data)
```

## 🏗️ Current Project Structure

```
Developer-App/
├── 📁 src/
│   ├── 📁 api/                    # API Layer
│   │   ├── __init__.py
│   │   ├── models.py              # Data models and DTOs
│   │   ├── company_api.py         # Company CRUD operations
│   │   ├── maincode_api.py        # MainCode CRUD operations
│   │   └── api_manager.py         # Central API manager
│   ├── 📁 core/                   # Core Components
│   │   ├── __init__.py
│   │   └── database.py            # SQLite database connection manager
│   ├── 📁 ui/                     # User Interface
│   │   ├── 📁 screens/            # Application screens
│   │   │   ├── __init__.py
│   │   │   ├── main_screen.py     # Main application window
│   │   │   ├── dashboard_screen.py # Dashboard with data display
│   │   │   └── settings_screen.py  # Settings and configuration
│   │   └── 📁 widgets/            # UI Components
│   │       ├── __init__.py
│   │       └── status_bar.py      # Status bar with connection monitoring
│   └── app.py                     # Main application class
├── 📁 data/                       # Database files (SQLite)
│   └── app_database.db           # Main application database
├── 📄 requirements.txt            # Python dependencies
├── 📄 main.py                     # Application entry point (placeholder)
├── 📄 test_core.py               # Core functionality tests
├── 📄 test_simple.py             # Simple database tests
└── 📄 README.md                   # Project documentation
```

## 🔒 Database Schema

### CompanyInfo Table

| Column                | Type                    | Description                   |
| --------------------- | ----------------------- | ----------------------------- |
| company_code          | VARCHAR(50) PRIMARY KEY | Unique company identifier     |
| company_name          | TEXT                    | Company name                  |
| city_code             | VARCHAR(10)             | City code                     |
| company_address       | TEXT                    | Company address               |
| phone_number          | VARCHAR(20)             | Contact phone                 |
| username              | VARCHAR(50)             | Login username                |
| password              | VARCHAR(100)            | Encrypted password            |
| subscription_code     | VARCHAR(50)             | Subscription identifier       |
| last_payment          | DATE                    | Last payment date             |
| subscription_duration | INTEGER                 | Subscription duration in days |
| registration_date     | DATETIME                | Registration timestamp        |
| descriptions          | TEXT                    | Additional descriptions       |

### MainCode Table

| Column        | Type                    | Description            |
| ------------- | ----------------------- | ---------------------- |
| main_code     | VARCHAR(50) PRIMARY KEY | Unique code identifier |
| record_type   | VARCHAR(20)             | Code category/type     |
| description   | TEXT                    | Code description       |
| value         | TEXT                    | Code value             |
| parent_code   | VARCHAR(50)             | Parent code reference  |
| sort_order    | INTEGER                 | Display order          |
| is_active     | BOOLEAN                 | Active status          |
| created_date  | DATETIME                | Creation timestamp     |
| modified_date | DATETIME                | Last modification      |

## 🚀 Deployment

### Development

- Use SQLite database (default configuration)
- Run with `python main.py`
- All data stored locally in `./data/app_database.db`

### Production

1. **Configure cloud database** (MySQL/PostgreSQL)
2. **Update .env file** with production database credentials
3. **Install production dependencies**:
   ```bash
   pip install mysql-connector-python  # For MySQL
   pip install psycopg2-binary         # For PostgreSQL
   ```
4. **Run application** with production configuration

### Cloud Database Examples

#### AWS RDS MySQL

```env
DB_TYPE=mysql
MYSQL_HOST=your-rds-endpoint.amazonaws.com
MYSQL_PORT=3306
MYSQL_USER=admin
MYSQL_PASSWORD=your-secure-password
MYSQL_DATABASE=developer_app
```

#### Google Cloud SQL PostgreSQL

```env
DB_TYPE=postgresql
POSTGRESQL_HOST=your-project:region:instance-id
POSTGRESQL_PORT=5432
POSTGRESQL_USER=postgres
POSTGRESQL_PASSWORD=your-secure-password
POSTGRESQL_DATABASE=developer_app
```

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Failed

1. **Check .env configuration** - Verify database credentials
2. **Test connectivity** - Use settings screen connection test
3. **Verify database server** - Ensure database server is running
4. **Check firewall** - Ensure database port is accessible

#### Import Errors

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Check Python version**: Requires Python 3.8+
3. **Virtual environment**: Consider using `venv` or `conda`

#### UI Not Loading

1. **Check Kivy installation**: `pip install kivy[base]`
2. **Graphics drivers**: Update graphics drivers if needed
3. **Display settings**: Check DPI scaling settings

### Logs and Debugging

- **Application logs**: Check terminal output
- **Kivy logs**: Located in `~/.kivy/logs/`
- **Database logs**: Enable DEBUG in .env for detailed logging

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow coding standards**: Use proper type hints and documentation
4. **Add tests**: Include tests for new functionality
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open Pull Request**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Roadmap

### Current Features ✅

- Multi-database support (SQLite, MySQL, PostgreSQL)
- Complete API layer with CRUD operations
- Modern UI with real-time monitoring
- Comprehensive testing suite
- Cloud database ready

### Planned Enhancements 🚧

- **Advanced Features**:

  - [ ] Data validation and form validation in UI
  - [ ] Audit logging for all data changes
  - [ ] Backup/restore functionality through API
  - [ ] Advanced search and filtering capabilities
  - [ ] Batch data processing tools

- **Performance Optimizations**:

  - [ ] Connection pooling for production environments
  - [ ] Caching layer for frequently accessed data
  - [ ] Async operations for better responsiveness
  - [ ] Database query optimization

- **Enhanced UI/UX**:

  - [ ] Dark mode theme support
  - [ ] Customizable dashboard layouts
  - [ ] Data visualization charts and graphs
  - [ ] Advanced export formats (Excel, PDF)
  - [ ] Drag-and-drop functionality

- **Enterprise Features**:
  - [ ] User authentication and authorization
  - [ ] Role-based access control
  - [ ] Multi-tenant support
  - [ ] API rate limiting and security
  - [ ] Comprehensive logging and monitoring

---

## 📞 Support

For questions, issues, or feature requests, please create an issue in the project repository or contact the development team.

**Happy Coding! 🚀**

- **Settings Panel**: User-friendly settings with real-time updates
- **Modular Architecture**: Well-organized, maintainable codebase
- **Error Handling**: Robust error handling and validation
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Project Structure

```
Developer-App/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── assets/                # Static assets
│   ├── icons/            # Application icons
│   ├── images/           # Images
│   └── themes/           # Theme configurations
├── config/               # Configuration files
├── data/                 # Database and data files
├── logs/                 # Application logs
├── src/                  # Source code
│   ├── app.py           # Main application class
│   ├── core/            # Core functionality
│   │   ├── config_manager.py
│   │   ├── database.py
│   │   └── window_manager.py
│   ├── ui/              # User interface
│   │   ├── screens/     # Application screens
│   │   └── widgets/     # Custom widgets
│   ├── services/        # Business logic services
│   │   ├── file_manager.py
│   │   └── logging_service.py
│   └── utils/           # Utility functions
│       ├── helpers.py
│       └── validators.py
└── tests/               # Unit tests (to be created)
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the project**

   ```bash
   git clone <repository-url>
   cd Developer-App
   ```

2. **Create virtual environment (recommended)**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**

   - Copy `.env` and modify settings as needed
   - The application will create necessary directories on first run

5. **Run the application**
   ```bash
   python main.py
   ```

## Configuration

### Environment Variables

Edit the `.env` file to configure:

- `DATABASE_PATH`: Path to SQLite database file
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `DEBUG_MODE`: Enable/disable debug mode
- `APP_TITLE`: Application window title
- `APP_VERSION`: Application version

### Application Settings

The application includes a settings panel where users can configure:

- UI theme (Light/Dark)
- Font size
- Auto-save preferences
- Database backup settings
- Logging preferences

## Development

### Code Organization

- **`src/core/`**: Core system functionality
- **`src/ui/`**: User interface components
- **`src/services/`**: Business logic and services
- **`src/utils/`**: Utility functions and helpers

### Best Practices Implemented

1. **Separation of Concerns**: Clear separation between UI, business logic, and data
2. **Configuration Management**: Centralized configuration with environment variables
3. **Error Handling**: Comprehensive error handling with proper logging
4. **Data Validation**: Input validation with custom validators
5. **Logging**: Structured logging with rotation and multiple levels
6. **Resource Management**: Proper cleanup and resource management
7. **Documentation**: Comprehensive code documentation and comments

### Adding New Features

1. **Create service modules** in `src/services/` for business logic
2. **Add UI components** in `src/ui/screens/` or `src/ui/widgets/`
3. **Use configuration manager** for settings
4. **Add proper logging** for debugging and monitoring
5. **Include error handling** and validation
6. **Update documentation** and tests

## Database

The application uses SQLite for data storage with:

- **Automatic schema creation**
- **Connection management**
- **Transaction handling**
- **Backup functionality**

### Default Tables

- `users`: User management
- `app_settings`: Application settings storage
- `logs`: Application log storage

## Logging

Comprehensive logging system with:

- **File rotation**: Automatic log file rotation
- **Multiple levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Console and file output**: Dual logging destinations
- **User action tracking**: Audit trail for user actions

## File Management

Built-in file management service with:

- **File operations**: Read, write, copy, move, delete
- **Directory operations**: List, create, search
- **File type detection**: Automatic file type categorization
- **Safety features**: Error handling and validation

## Building for Distribution

### Using PyInstaller

1. **Install PyInstaller**

   ```bash
   pip install pyinstaller
   ```

2. **Create executable**

   ```bash
   pyinstaller --onefile --windowed main.py
   ```

3. **Advanced build with assets**
   ```bash
   pyinstaller --onefile --windowed --add-data "assets;assets" --add-data "config;config" main.py
   ```

### Using cx_Freeze

1. **Install cx_Freeze**

   ```bash
   pip install cx_freeze
   ```

2. **Create setup.py** (example provided in repository)

3. **Build**
   ```bash
   python setup.py build
   ```

## Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Test Structure

- Unit tests for each module
- Integration tests for services
- UI tests for screens and widgets

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Database Issues**: Check database path and permissions
3. **UI Problems**: Verify Kivy installation and graphics drivers
4. **Performance**: Check system resources and log levels

### Debug Mode

Enable debug mode in `.env` file:

```
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the established patterns
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## License

[Add your license information here]

## Support

[Add support information here]

## Changelog

### Version 1.0.0

- Initial release
- Basic application structure
- Core functionality implementation
- UI framework and screens
- Database integration
- Configuration management
- Logging system
