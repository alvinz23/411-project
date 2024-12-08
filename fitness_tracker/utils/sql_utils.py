from contextlib import contextmanager
import logging
import os
import sqlite3
from fitness_tracker.utils.fitness_logger import configure_logger

# Set up logging
logger = logging.getLogger(__name__)
configure_logger(logger)

# Load the database path from environment or set a default
DB_PATH = os.getenv("DB_PATH", "/app/sql/fitness_tracker.db")


def check_database_connection():
    """
    Checks if the database connection is active and functioning.

    Raises:
        Exception: If there is a connection or query error.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")  # Simple query to verify connection
            logger.info("Database connection verified successfully.")
    except sqlite3.Error as e:
        error_message = f"Database connection error: {e}"
        logger.error(error_message)
        raise Exception(error_message) from e


def check_table_exists(tablename: str):
    """
    Checks if a specific table exists in the database.

    Args:
        tablename (str): The name of the table to check.

    Raises:
        Exception: If the table does not exist or there is a query error.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT 1 FROM {tablename} LIMIT 1;")  # Attempt to query the table
            logger.info("Table '%s' exists in the database.", tablename)
    except sqlite3.Error as e:
        error_message = f"Error checking table '{tablename}': {e}"
        logger.error(error_message)
        raise Exception(error_message) from e


@contextmanager
def get_db_connection():
    """
    Provides a database connection using a context manager.

    Yields:
        sqlite3.Connection: The SQLite connection object.

    Raises:
        sqlite3.Error: If there is a database connection error.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        logger.info("Database connection opened.")
        yield conn
    except sqlite3.Error as e:
        logger.error("Database connection error: %s", str(e))
        raise e
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")


def initialize_database():
    """
    Initializes the database by creating necessary tables if they don't exist.

    Raises:
        sqlite3.Error: If there is a database query error.
    """
    create_goals_table = """
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        goal_type TEXT NOT NULL,
        target_value REAL NOT NULL,
        progress REAL DEFAULT 0,
        start_date TEXT DEFAULT (DATE('now')),
        end_date TEXT NOT NULL
    );
    """

    create_workouts_table = """
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        workout_type TEXT NOT NULL,
        duration INTEGER NOT NULL,  -- Duration in minutes
        calories_burned REAL NOT NULL,
        date TEXT DEFAULT (DATE('now'))
    );
    """

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(f"{create_goals_table}\n{create_workouts_table}")
            conn.commit()
            logger.info("Database initialized successfully with required tables.")
    except sqlite3.Error as e:
        logger.error("Error initializing database: %s", str(e))
        raise e
