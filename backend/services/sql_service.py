# backend/services/sql_service.py
import sqlite3

def read_sql_query(sql_query: str, db_path: str = "cars.db"):
    """
    Execute SQL query and return results
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(sql_query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Get column names
        columns = [description[0] for description in cursor.description] if cursor.description else []

        # Close connection
        conn.close()

        return rows, columns

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return [], []
    except Exception as e:
        print(f"Error executing query: {e}")
        return [], []

def test_database_connection(db_path: str = "cars.db"):
    """
    Test if database connection works
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if cars table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cars'")
        table_exists = cursor.fetchone() is not None

        conn.close()
        return table_exists

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return False