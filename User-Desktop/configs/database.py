import sqlite3
import os
from sqlite3 import Error
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('database')

class DatabaseManager:
    """Database manager for handling SQLite connections (both local and cloud)."""

    def __init__(self, db_path=None, cloud_url=None):
        """
        Initialize the database manager.

        Args:
            db_path (str, optional): Path to local SQLite database
            cloud_url (str, optional): URL for cloud SQLite connection
        """
        # Use absolute path for local database
        self.db_path = db_path or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'local.db')
        self.cloud_url = cloud_url
        self.connection = None
        self.cursor = None

    def create_connection(self, db_path):
        """ Create a database connection to the SQLite database specified by db_path. """
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            logger.info(f"Connected to database: {db_path}")
            return conn
        except Error as e:
            logger.error(f"Error connecting to database: {e}")
            return None

    def connect_local(self):
        """Connect to the local SQLite database."""
        try:
            # Ensure data directory exists if not using in-memory database
            if self.db_path != ":memory:":
                os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

            self.connection = self.create_connection(self.db_path)
            if self.connection:
                self.cursor = self.connection.cursor()
                logger.info(f"Connected to local database at {self.db_path}")
                return True
            return False
        except Error as e:
            logger.error(f"Error connecting to local database: {e}")
            return False

    def connect_cloud(self):
        """
        Connect to cloud SQLite database.
        Note: This is a placeholder for actual cloud DB connection logic.
        """
        if not self.cloud_url:
            logger.error("Cloud URL not provided")
            return False

        try:
            self.connection = self.create_connection(self.cloud_url)
            if self.connection:
                self.cursor = self.connection.cursor()
                logger.info(f"Connected to cloud database at {self.cloud_url}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error connecting to cloud database: {e}")
            return False

    def test_connection(self):
        """Test the database connection by executing a simple query."""
        if not self.connection:
            logger.error("No database connection")
            return False

        try:
            self.cursor.execute("SELECT sqlite_version();")
            version = self.cursor.fetchone()[0]
            logger.info(f"SQLite version: {version}")
            return True
        except Error as e:
            logger.error(f"Connection test failed: {e}")
            return False

    def create_tables(self):
        """Create database tables if they don't exist."""
        if not self.connection:
            logger.error("No database connection")
            return False

        try:
            # Create Maincode table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Maincode (
                Recty CHAR(2) NOT NULL,
                Code CHAR(16) NOT NULL,
                Name VARCHAR(50) NOT NULL,
                Description TEXT,
                PRIMARY KEY (Recty, Code)
            )
            ''')

            # Create Companyinfo table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Companyinfo (
                Companyco CHAR(4) PRIMARY KEY,
                Companyna VARCHAR(30) NOT NULL,
                Cityco CHAR(5),
                Caddress VARCHAR(50),
                Cophoneno CHAR(11),
                Username CHAR(12),
                Password CHAR(8),
                SubscriptionTCode CHAR(1),
                Lastpayment DATE,
                Subscriptionduration CHAR(1),
                Registrationdate DATE,
                Descriptions TEXT
            )
            ''')

            # Create Owners table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Owners (
                Ownercode CHAR(4) PRIMARY KEY,
                ownername VARCHAR(30) NOT NULL,
                ownerphone CHAR(11),
                Note TEXT
            )
            ''')

            # Create Realstatspecification table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Realstatspecification (
                Companyco CHAR(4) NOT NULL,
                realstatecode CHAR(8) PRIMARY KEY,
                Rstatetcode CHAR(1),
                Yearmake DATE,
                Buildtcode CHAR(1),
                "Property-area" REAL,
                "Unitm-code" CHAR(1),
                "Property-facade" REAL,
                "Property-depth" REAL,
                "N-of-bedrooms" INTEGER,
                "N-of-bathrooms" INTEGER,
                "Property-corner" BOOLEAN,
                "Offer-Type-Code" CHAR(1),
                "Province-code" CHAR(2),
                "Region-code" CHAR(9),
                "Property-address" TEXT,
                Photosituation BOOLEAN,
                Ownercode CHAR(4),
                Descriptions TEXT,
                FOREIGN KEY (Ownercode) REFERENCES Owners(Ownercode),
                FOREIGN KEY (Companyco) REFERENCES Companyinfo(Companyco)
            )
            ''')

            # Create realstatephotos table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS realstatephotos (
                realstatecode CHAR(8) NOT NULL,
                Storagepath VARCHAR(50),
                photofilename VARCHAR(30),
                Photoextension CHAR(4),
                FOREIGN KEY (realstatecode) REFERENCES Realstatspecification(realstatecode),
                PRIMARY KEY (realstatecode, photofilename)
            )
            ''')

            self.connection.commit()
            logger.info("Database tables created successfully")
            return True
        except Error as e:
            logger.error(f"Error creating tables: {e}")
            return False

    def execute_query(self, query, params=None):
        """
        Execute a SQL query.

        Args:
            query (str): SQL query to execute
            params (tuple, optional): Parameters for the query

        Returns:
            list: Query results or None if error
        """
        if not self.connection:
            logger.error("No database connection")
            return None

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if query.strip().upper().startswith(('SELECT', 'PRAGMA')):
                return [dict(row) for row in self.cursor.fetchall()]
            else:
                self.connection.commit()
                return True
        except Error as e:
            logger.error(f"Query execution error: {e}")
            return None

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

# For backward compatibility with older code
def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file. """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def test_connection(conn):
    """ Test the database connection. """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print("Database connection test successful.")
    except Error as e:
        print(f"Database connection test failed: {e}")

def connect_to_local_db():
    """ Connect to the local SQLite database. """
    local_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'local.db')
    conn = create_connection(local_db_path)
    if conn:
        test_connection(conn)
        conn.close()
        return True
    return False

def connect_to_cloud_db(cloud_db_url):
    """ Connect to the cloud SQLite database. """
    conn = create_connection(cloud_db_url)
    if conn:
        test_connection(conn)
        conn.close()
        return True
    return False