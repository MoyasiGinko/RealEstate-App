import unittest
from configs.database import connect_to_local_db, connect_to_cloud_db

class TestDatabaseConnections(unittest.TestCase):

    def test_local_db_connection(self):
        """Test the connection to the local SQLite database."""
        connection = connect_to_local_db()
        self.assertIsNotNone(connection)
        connection.close()

    def test_cloud_db_connection(self):
        """Test the connection to the cloud SQLite database."""
        connection = connect_to_cloud_db()
        self.assertIsNotNone(connection)
        connection.close()

if __name__ == '__main__':
    unittest.main()