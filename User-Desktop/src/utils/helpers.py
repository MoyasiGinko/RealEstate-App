def connect_to_local_db(db_path):
    import sqlite3
    try:
        connection = sqlite3.connect(db_path)
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to local database: {e}")
        return None

def connect_to_cloud_db(cloud_db_url):
    import sqlite3
    try:
        connection = sqlite3.connect(cloud_db_url)
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to cloud database: {e}")
        return None

def test_database_connection(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        return True
    except sqlite3.Error as e:
        print(f"Database connection test failed: {e}")
        return False