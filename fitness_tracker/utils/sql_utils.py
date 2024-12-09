import sqlite3
import os
from dotenv import load_dotenv



DB_PATH = os.getenv("DB_PATH")

def get_db_connection():
    """
    Establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: An active SQLite database connection.

    Raises:
        sqlite3.Error: If there is an error connecting to the database.
    """
    return sqlite3.connect("DB_PATH")

def initialize_database():
    """
    Initializes the database with required tables.

    Returns:
        None

    Raises:
        FileNotFoundError: If the SQL file is not found.
        sqlite3.Error: If there is an error executing the SQL script.
    """
    with get_db_connection() as conn:
        with open("sql/create_user_table.sql", "r") as f:
            conn.executescript(f.read())
