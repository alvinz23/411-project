import sqlite3
from fitness_tracker.utils.sql_utils import get_db_connection
import hashlib
import os
import logging

from fitness_tracker.utils.sql_utils import initialize_database

initialize_database()

def hash_password(password: str, salt: str) -> str:
    """
    Hash a password using a salt.

    Combines the provided salt and password, then applies SHA-256 hashing to generate
    a secure hash for storage.

    Args:
        password (str): The plain text password to hash.
        salt (str): A randomly generated salt to add to the password.

    Returns:
        str: The hashed password as a hexadecimal string.

    Raises:
        None
    """
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def create_user(username: str, password: str) -> None:
    """
    Create a new user in the database.

    Generates a random salt and hashes the provided password for secure storage.
    Inserts the user, salt, and hashed password into the database.

    Args:
        username (str): The username of the new user.
        password (str): The plain text password for the user.

    Returns:
        None

    Raises:
        ValueError: If the username is already taken.
        sqlite3.Error: If there is a database error during user creation.
    """
    logging.info(f"Attempting to create user: {username}")
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
        logging.info(f"User '{username}' created successfully.")
    except sqlite3.IntegrityError:
        logging.error(f"Failed to create user: Username '{username}' is already taken.")
        raise ValueError(f"Username '{username}' is already taken.")


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user by verifying their password.

    Retrieves the stored salt and hashed password for the user, hashes the provided
    password with the stored salt, and compares the result to the stored hash.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The plain text password provided by the user.

    Returns:
        bool: True if authentication is successful, False otherwise.

    Raises:
        None
    """
    logging.info(f"Authenticating user: {username}")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT salt, hashed_password FROM users WHERE username = ?
        """, (username,))
        result = cursor.fetchone()

        if not result:
            logging.warning(f"Authentication failed: User '{username}' not found.")
            return False  

        salt, hashed_password = result
        if hash_password(password, salt) == hashed_password:
            logging.info(f"Authentication successful for user: {username}")
            return True
        else:
            logging.warning(f"Authentication failed for user: {username}")
            return False


def change_password(username: str, new_password: str) -> None:
    """
    Change a user's password.

    Generates a new random salt, hashes the new password, and updates the user's
    stored salt and hashed password in the database.

    Args:
        username (str): The username of the user changing their password.
        new_password (str): The new plain text password to be set.

    Returns:
        None

    Raises:
        ValueError: If the username does not exist in the database.
        sqlite3.Error: If there is a database error during the update.
    """
    logging.info(f"Changing password for user: {username}")
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
            logging.error(f"Failed to change password: User '{username}' does not exist.")
            raise ValueError(f"User '{username}' does not exist.")
        else:
            logging.info(f"Password updated successfully for user: {username}")
