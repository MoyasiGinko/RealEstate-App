"""
Database Connection Manager
Handles database connections for SQLite
Focused on CompanyInfo and MainCode tables only
"""

import sqlite3
import os
from pathlib import Path
from kivy.logger import Logger
from contextlib import contextmanager
from typing import Optional, Dict, Any


class DatabaseManager:
    """Manages database connections for local databases"""

    def __init__(self):
        self.connection = None
        self.db_type = 'sqlite'
        self.db_path = os.getenv('DATABASE_PATH', './data/local.db')
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False
            )
            self.connection.row_factory = sqlite3.Row
            self._create_tables()
            Logger.info(f"Database connected successfully: {self.db_path}")
            return True
        except Exception as e:
            Logger.error(f"Database connection failed: {e}")
            return False

    def _create_tables(self):
        """Create CompanyInfo and MainCode tables if they don't exist"""
        cursor = self.connection.cursor()
        try:
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

            self.connection.commit()
            Logger.info("Database tables created/verified successfully")
        except Exception as e:
            Logger.error(f"Failed to create tables: {e}")
            raise e
        finally:
            cursor.close()

    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor"""
        if not self.connection:
            raise Exception("Database not connected. Call connect() first.")

        cursor = self.connection.cursor()
        try:
            yield cursor
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cursor.close()

    def execute_query(self, query: str, params: tuple = ()) -> list:
        """Execute a SELECT query and return results"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_command(self, command: str, params: tuple = ()) -> int:
        """Execute an INSERT, UPDATE, or DELETE command"""
        with self.get_cursor() as cursor:
            cursor.execute(command, params)
            return cursor.rowcount

    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.connection is not None

    def test_connection(self) -> bool:
        """Test if database connection is working"""
        try:
            if not self.connection:
                return False
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
                return True
        except Exception as e:
            Logger.error(f"Connection test failed: {e}")
            return False

    def get_info(self) -> Dict[str, Any]:
        """Get database connection information"""
        return {
            'type': self.db_type,
            'connected': self.connection is not None,
            'database_path': self.db_path
        }

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            Logger.info("Database connection closed")
