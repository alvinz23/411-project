import unittest
import sqlite3
from fitness_tracker.models.user_model import create_user, authenticate_user, change_password
from fitness_tracker.utils.sql_utils import initialize_database, get_db_connection


class TestUserModel(unittest.TestCase):
    """
    Unit tests for the user model functions in the fitness tracker application.
    """
    def setUp(self):
        """
        Sets up the testing environment by initializing the database and clearing user data.

        Args:
            None

        Returns:
            None
        """
        initialize_database()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users")
            conn.commit()

    def test_create_user_success(self):
        """
        Tests the creation of a new user with valid credentials.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the created user is not found in the database.
        """
        create_user("testuser", "password123")
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE username = ?", ("testuser",))
            user = cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[0], "testuser")

    def test_create_user_duplicate(self):
        """
        Tests that creating a user with a duplicate username raises a ValueError.

        Args:
            None

        Returns:
            None

        Raises:
            ValueError: If the username already exists.
        """
        create_user("testuser", "password123")
        with self.assertRaises(ValueError) as context:
            create_user("testuser", "newpassword")
        self.assertEqual(str(context.exception), "Username 'testuser' is already taken.")

    def test_authenticate_user_success(self):
        """
        Tests authenticating a user with the correct username and password.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the authentication fails for valid credentials.
        """
        create_user("testuser", "password123")
        self.assertTrue(authenticate_user("testuser", "password123"))

    def test_authenticate_user_invalid_password(self):
        """
        Tests authenticating a user with an incorrect password.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the authentication succeeds with invalid credentials.
        """
        create_user("testuser", "password123")
        self.assertFalse(authenticate_user("testuser", "wrongpassword"))

    def test_authenticate_user_nonexistent(self):
        """
        Tests authenticating a non-existent user.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the authentication succeeds for a non-existent user.
        """
        self.assertFalse(authenticate_user("nonexistentuser", "password123"))

    def test_change_password_success(self):
        """
        Tests successfully changing a user's password.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the password change does not work as expected.
        """
        create_user("testuser", "password123")
        change_password("testuser", "newpassword123")
        self.assertTrue(authenticate_user("testuser", "newpassword123"))
        self.assertFalse(authenticate_user("testuser", "password123"))

    def test_change_password_nonexistent_user(self):
        """
        Tests attempting to change the password of a non-existent user.

        Args:
            None

        Returns:
            None

        Raises:
            ValueError: If the user does not exist in the database.
        """
        with self.assertRaises(ValueError) as context:
            change_password("nonexistentuser", "newpassword123")
        self.assertEqual(str(context.exception), "User 'nonexistentuser' does not exist.")



if __name__ == "__main__":
    unittest.main()
