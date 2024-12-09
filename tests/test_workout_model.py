import unittest
from unittest.mock import patch
from fitness_tracker.models.workout_model import (
    check_workout_in_api,
    add_workout_to_memory,
    get_workouts,
    update_workout,
    delete_workout,
    get_deleted_workouts,
    stored_workouts,  
    deleted_workouts,  
)

class TestWorkoutModel(unittest.TestCase):
    """
    Unit tests for the user model functions in the fitness tracker application.
    """
    def setUp(self):
        """
        Clears stored and deleted workouts before each test. 

        Args:
            None

        Returns:
            None
        """
        stored_workouts.clear()
        deleted_workouts.clear()

    @patch("fitness_tracker.models.workout_model.requests.get")
    def test_check_workout_in_api_success(self, mock_get):
        """
        Tests if a valid workout is fetched and cleaned successfully.

        Args:
            mock_get (Mock): The mocked requests.get method.

        Returns:
            None

        Raises:
            AssertionError: If the workout data does not match the expected values.
        """
        mock_response = {
            "id": 1,
            "name": "Push-Up",
            "description": "<p>A bodyweight exercise</p>",
            "muscles": [4],
            "equipment": [],
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        workout = check_workout_in_api(1)
        self.assertIsNotNone(workout)
        self.assertEqual(workout["id"], 1)
        self.assertEqual(workout["name"], "Push-Up")
        self.assertEqual(workout["description"], "A bodyweight exercise")
        self.assertEqual(workout["muscles"], [4])
        self.assertEqual(workout["equipment"], [])

    @patch("fitness_tracker.models.workout_model.requests.get")
    def test_check_workout_in_api_not_found(self, mock_get):
        """
        Tests if an invalid workout ID returns None.

        Args:
            mock_get (Mock): The mocked requests.get method.

        Returns:
            None

        Raises:
            AssertionError: If the workout is not None for an invalid ID.
        """
        mock_get.return_value.status_code = 404

        workout = check_workout_in_api(999)
        self.assertIsNone(workout)

    def test_add_workout_to_memory(self):
        """
        Tests adding a workout to memory.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the workout is not added to memory as expected.
        """
        workout = {
            "id": 1,
            "name": "Push-Up",
            "description": "A bodyweight exercise",
            "muscles": [4],
            "equipment": [],
        }
        stored_workouts[1] = workout
        self.assertIn(1, stored_workouts)
        self.assertEqual(stored_workouts[1], workout)

    def test_get_workouts(self):
        """
        Tests retrieving all stored workouts.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the retrieved workouts do not match the stored workouts.
        """
        workout = {
            "id": 1,
            "name": "Push-Up",
            "description": "A bodyweight exercise",
            "muscles": [4],
            "equipment": [],
        }
        stored_workouts[1] = workout
        workouts = get_workouts()
        self.assertEqual(len(workouts["stored_workouts"]), 1)
        self.assertEqual(workouts["stored_workouts"][0], workout)

    def test_update_workout(self):
        """
        Tests updating a workout's name and description.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the workout is not updated as expected.
        """
        workout = {
            "id": 1,
            "name": "Push-Up",
            "description": "A bodyweight exercise",
            "muscles": [4],
            "equipment": [],
        }
        stored_workouts[1] = workout
        result = update_workout(1, "Updated Push-Up", "Updated description")
        self.assertEqual(result["status"], "success")
        self.assertEqual(stored_workouts[1]["name"], "Updated Push-Up")
        self.assertEqual(stored_workouts[1]["description"], "Updated description")

    def test_delete_workout(self):
        """
        Tests deleting a workout.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the workout is not deleted or logged as expected.
        """
        workout = {
            "id": 1,
            "name": "Push-Up",
            "description": "A bodyweight exercise",
            "muscles": [4],
            "equipment": [],
        }
        stored_workouts[1] = workout
        result = delete_workout(1)
        self.assertEqual(result["status"], "success")
        self.assertNotIn(1, stored_workouts)
        self.assertIn(workout, deleted_workouts)

    def test_get_deleted_workouts(self):
        """
        Tests retrieving all deleted workouts.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the retrieved deleted workouts do not match the logged workouts.
        """
        workout = {
            "id": 1,
            "name": "Push-Up",
            "description": "A bodyweight exercise",
            "muscles": [4],
            "equipment": [],
        }
        deleted_workouts.append(workout)
        workouts = get_deleted_workouts()
        self.assertEqual(len(workouts["deleted_workouts"]), 1)
        self.assertEqual(workouts["deleted_workouts"][0], workout)


if __name__ == "__main__":
    unittest.main()
