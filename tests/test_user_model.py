import unittest
import sqlite3
from fitness_tracker.models.user_model import create_user, authenticate_user, change_password
from fitness_tracker.utils.sql_utils import initialize_database, get_db_connection


class TestUserModel(unittest.TestCase):

    def setUp(self):
        """Initialize the database and clear any existing data."""
        initialize_database()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users")
            conn.commit()

    def test_create_user_success(self):
        """Test creating a new user successfully."""
        create_user("testuser", "password123")
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE username = ?", ("testuser",))
            user = cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[0], "testuser")

    def test_create_user_duplicate(self):
        """Test creating a user with a duplicate username."""
        create_user("testuser", "password123")
        with self.assertRaises(ValueError) as context:
            create_user("testuser", "newpassword")
        self.assertEqual(str(context.exception), "Username 'testuser' is already taken.")

    def test_authenticate_user_success(self):
        """Test authenticating a user with the correct password."""
        create_user("testuser", "password123")
        self.assertTrue(authenticate_user("testuser", "password123"))

    def test_authenticate_user_invalid_password(self):
        """Test authenticating a user with an incorrect password."""
        create_user("testuser", "password123")
        self.assertFalse(authenticate_user("testuser", "wrongpassword"))

    def test_authenticate_user_nonexistent(self):
        """Test authenticating a nonexistent user."""
        self.assertFalse(authenticate_user("nonexistentuser", "password123"))

    def test_change_password_success(self):
        """Test changing a user's password successfully."""
        create_user("testuser", "password123")
        change_password("testuser", "newpassword123")
        self.assertTrue(authenticate_user("testuser", "newpassword123"))
        self.assertFalse(authenticate_user("testuser", "password123"))

    def test_change_password_nonexistent_user(self):
        """Test changing the password for a nonexistent user."""
        with self.assertRaises(ValueError) as context:
            change_password("nonexistentuser", "newpassword123")
        self.assertEqual(str(context.exception), "User 'nonexistentuser' does not exist.")



if __name__ == "__main__":
    unittest.main()
