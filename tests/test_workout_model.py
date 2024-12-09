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

    def setUp(self):
        """Clear stored and deleted workouts before each test."""
        stored_workouts.clear()
        deleted_workouts.clear()

    @patch("fitness_tracker.models.workout_model.requests.get")
    def test_check_workout_in_api_success(self, mock_get):
        """Test if a valid workout is fetched and cleaned successfully."""
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
        """Test if an invalid workout ID returns None."""
        mock_get.return_value.status_code = 404

        workout = check_workout_in_api(999)
        self.assertIsNone(workout)

    def test_add_workout_to_memory(self):
        """Test adding a workout to memory."""
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
        """Test retrieving all stored workouts."""
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
        """Test updating a workout's name and description."""
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
        """Test deleting a workout."""
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
        """Test retrieving all deleted workouts."""
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
