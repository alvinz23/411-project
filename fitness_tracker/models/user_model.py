import sqlite3
from fitness_tracker.utils.sql_utils import get_db_connection
import hashlib
import os

from fitness_tracker.utils.sql_utils import initialize_database

initialize_database()

def hash_password(password: str, salt: str) -> str:
    """Hashes the password with the given salt."""
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def create_user(username: str, password: str) -> None:
    """Creates a new user in the database."""
    salt = os.urandom(16).hex()  # Generate a random salt
    hashed_password = hash_password(password, salt)

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, salt, hashed_password)
                VALUES (?, ?, ?)
            """, (username, salt, hashed_password))
            conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"Username '{username}' is already taken.")


def authenticate_user(username: str, password: str) -> bool:
    """Authenticates a user by checking the provided password."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT salt, hashed_password FROM users WHERE username = ?
        """, (username,))
        result = cursor.fetchone()

        if not result:
            return False  

        salt, hashed_password = result
        return hash_password(password, salt) == hashed_password


def change_password(username: str, new_password: str) -> None:
    """Allows a user to change their password."""
    salt = os.urandom(16).hex()  # Generate a new salt
    hashed_password = hash_password(new_password, salt)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET salt = ?, hashed_password = ? WHERE username = ?
        """, (salt, hashed_password, username))
        conn.commit()

        # Check if any rows were updated
        if cursor.rowcount == 0:
            raise ValueError(f"User '{username}' does not exist.")
