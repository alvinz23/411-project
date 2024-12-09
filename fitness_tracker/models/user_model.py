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
    """
    Creates a new user and stores their credentials securely in the database.

    Args:
        username (str): The username of the new user.
        password (str): The plain-text password for the user.

    Returns:
        dict: A dictionary containing the user ID and username upon successful creation.

    Raises:
        sqlite3.Error: If there is an issue with the database connection or insertion.
    """
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
    """
    Authenticates a user by validating their credentials.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The plain-text password entered by the user.

    Returns:
        bool: True if authentication is successful, False otherwise.

    Raises:
        sqlite3.Error: If there is an issue with the database query.
    """
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
    """
    Changes the password for a user after verifying the old password.

    Args:
        user_id (int): The unique identifier of the user.
        old_password (str): The current password of the user.
        new_password (str): The new password to be set.

    Returns:
        bool: True if the password was successfully updated, False otherwise.

    Raises:
        ValueError: If the old password does not match the stored password.
        sqlite3.Error: If there is an issue with the database update.
    """
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
