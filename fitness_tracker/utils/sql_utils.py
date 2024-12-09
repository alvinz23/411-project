import sqlite3
import os
from dotenv import load_dotenv



DB_PATH = os.getenv("DB_PATH")

def get_db_connection():
    """Gets a connection to the SQLite database."""
    return sqlite3.connect("DB_PATH")

def initialize_database():
    """Initializes the database with required tables."""
    with get_db_connection() as conn:
        with open("sql/create_user_table.sql", "r") as f:
            conn.executescript(f.read())
