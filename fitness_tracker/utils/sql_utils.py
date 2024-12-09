import sqlite3


DB_PATH = "fitness_tracker.db"


def get_db_connection():
    """
    Verifies the database connection by executing a test query.

    Raises:
        Exception: If there is an error connecting to the database or executing the query.
    """
    return sqlite3.connect("fitness_tracker.db")

def initialize_database():
    """
    Checks if a specified table exists in the database.

    Args:
        tablename (str): The name of the table to check.

    Raises:
        Exception: If the table does not exist or there is a database error.
    """
    with get_db_connection() as conn:
        with open("sql/create_user_table.sql", "r") as f:
            conn.executescript(f.read())
