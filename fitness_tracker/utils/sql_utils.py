import sqlite3


DB_PATH = "fitness_tracker.db"


def get_db_connection():
    """Gets a connection to the SQLite database."""
    return sqlite3.connect("fitness_tracker.db")

def initialize_database():
    """Initializes the database with required tables."""
    with get_db_connection() as conn:
        with open("sql/create_user_table.sql", "r") as f:
            conn.executescript(f.read())
