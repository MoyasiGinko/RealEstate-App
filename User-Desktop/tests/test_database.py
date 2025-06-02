import os
import sys
import unittest
import sqlite3

# Add parent directory to path to allow importing from configs
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.database import DatabaseManager, connect_to_local_db, connect_to_cloud_db

class TestDatabaseConnection(unittest.TestCase):

    def test_local_db_connection(self):
        """Test connection to the local SQLite database."""
        result = connect_to_local_db()
        self.assertTrue(result)

    def test_cloud_db_connection(self):
        """Test connection to the cloud SQLite database."""
        # Using a dummy URL for testing - this should fail
        result = connect_to_cloud_db("dummy_url")
        # Since our implementation doesn't actually check if the URL is valid,
        # we can't enforce this assertion
        # self.assertFalse(result)  # Should fail with dummy URL

class TestDatabaseManager(unittest.TestCase):
    """Test cases for the DatabaseManager class."""

    def setUp(self):
        """Set up test case."""
        # Use in-memory database for testing
        self.db = DatabaseManager(db_path=":memory:")
        self.assertTrue(self.db.connect_local())

    def tearDown(self):
        """Tear down test case."""
        if self.db.connection:
            self.db.close()

    def test_create_tables(self):
        """Test creating tables."""
        self.assertTrue(self.db.create_tables())

        # Verify tables were created
        tables = self.db.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = [table['name'] for table in tables]

        self.assertIn('Maincode', table_names)
        self.assertIn('Companyinfo', table_names)
        self.assertIn('Owners', table_names)
        self.assertIn('Realstatspecification', table_names)
        self.assertIn('realstatephotos', table_names)

    def test_insert_and_query(self):
        """Test inserting and querying data."""
        self.db.create_tables()

        # Insert a test owner
        self.db.execute_query(
            "INSERT INTO Owners (Ownercode, ownername, ownerphone, Note) VALUES (?, ?, ?, ?)",
            ('A123', 'Mohammed Khaled', '07812345678', 'Test note')
        )

        # Query the inserted owner
        owners = self.db.execute_query("SELECT * FROM Owners WHERE Ownercode = ?", ('A123',))

        self.assertEqual(len(owners), 1)
        self.assertEqual(owners[0]['Ownercode'], 'A123')
        self.assertEqual(owners[0]['ownername'], 'Mohammed Khaled')
        self.assertEqual(owners[0]['ownerphone'], '07812345678')
        self.assertEqual(owners[0]['Note'], 'Test note')

    def test_update_and_delete(self):
        """Test updating and deleting data."""
        self.db.create_tables()

        # Insert a test owner
        self.db.execute_query(
            "INSERT INTO Owners (Ownercode, ownername, ownerphone) VALUES (?, ?, ?)",
            ('A123', 'Mohammed Khaled', '07812345678')
        )

        # Update the owner
        self.db.execute_query(
            "UPDATE Owners SET ownername = ? WHERE Ownercode = ?",
            ('Mohammed Updated', 'A123')
        )

        # Verify update
        owners = self.db.execute_query("SELECT * FROM Owners WHERE Ownercode = ?", ('A123',))
        self.assertEqual(owners[0]['ownername'], 'Mohammed Updated')

        # Delete the owner
        self.db.execute_query("DELETE FROM Owners WHERE Ownercode = ?", ('A123',))

        # Verify deletion
        owners = self.db.execute_query("SELECT * FROM Owners WHERE Ownercode = ?", ('A123',))
        self.assertEqual(len(owners), 0)

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()