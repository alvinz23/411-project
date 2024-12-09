import requests
import logging


# In-memory storage for workouts
stored_workouts = {}
deleted_workouts = []

# Wger API URL
WGER_API_BASE_URL = "https://wger.de/api/v2/exercise/"


def check_workout_in_api(workout_id):
    """
    Checks if an exercise exists in the wger API by its ID.

    Args:
        workout_id (int): The ID of the workout to check.

    Returns:
        dict: A cleaned dictionary containing workout details if the workout exists.
        None: If the workout is not found in the API.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
    """
    logging.info(f"Fetching workout {workout_id} from wger API.")
    url = f"{WGER_API_BASE_URL}{workout_id}/?language=2"
    response = requests.get(url)
    if response.status_code == 200:
        logging.info(f"Successfully fetched workout {workout_id}.")
        # Extract relevant fields and clean up the JSON response
        workout = response.json()
        cleaned_workout = {
            "id": workout["id"],
            "name": workout["name"],
            "description": workout.get("description", "").replace("<p>", "").replace("</p>", "").strip(),
            "muscles": workout["muscles"],
            "equipment": workout["equipment"],
        }
        return cleaned_workout
    else:
        logging.error(f"Failed to fetch workout {workout_id}. Status code: {response.status_code}")
        return None


def add_workout_to_memory(workout_id):
    """
    Adds a workout to in-memory storage after verifying it exists in the wger API.

    Args:
        workout_id (int): The ID of the workout to add.

    Returns:
        dict: A dictionary indicating the status and details of the operation.

    Raises:
        None
    """
    logging.info(f"Attempting to add workout {workout_id} to memory.")
    if workout_id in stored_workouts:
        logging.warning(f"Workout {workout_id} already exists in memory.")
        return {"status": "error", "message": "Workout already exists in memory."}

    workout = check_workout_in_api(workout_id)
    if workout:
        stored_workouts[workout_id] = workout
        logging.info(f"Workout {workout_id} added to memory successfully.")
        return {"status": "success", "message": "Workout added to memory.", "workout": workout}
    else:
        logging.error(f"Workout {workout_id} not found in the API.")
        return {"status": "error", "message": "Workout not found in API."}


def get_workouts():
    """
    Retrieves all workouts currently stored in memory.

    Args:
        None

    Returns:
        dict: A dictionary containing a list of all stored workouts.

    Raises:
        None
    """
    return {"stored_workouts": list(stored_workouts.values())}


def update_workout(workout_id, new_name, new_description):
    """
    Updates the details of a workout in memory.

    Args:
        workout_id (int): The ID of the workout to update.
        new_name (str): The updated name for the workout.
        new_description (str): The updated description for the workout.

    Returns:
        dict: A dictionary indicating the status and details of the operation.

    Raises:
        None
    """
    logging.info(f"Updating workout {workout_id}.")
    if workout_id in stored_workouts:
        stored_workouts[workout_id]["name"] = new_name
        stored_workouts[workout_id]["description"] = new_description.strip()
        logging.info(f"Workout {workout_id} updated successfully.")
        return {"status": "success", "message": "Workout updated."}
    else:
        logging.error(f"Workout {workout_id} not found in memory.")
        return {"status": "error", "message": "Workout not found."}


def delete_workout(workout_id):
    """
    Deletes a workout from memory and logs it in deleted workouts.

    Args:
        workout_id (int): The ID of the workout to delete.

    Returns:
        dict: A dictionary indicating the status and details of the operation.

    Raises:
        None
    """
    logging.info(f"Attempting to delete workout {workout_id}.")
    if workout_id in stored_workouts:
        deleted_workouts.append(stored_workouts[workout_id])
        del stored_workouts[workout_id]
        logging.info(f"Workout {workout_id} deleted and logged.")
        return {"status": "success", "message": "Workout deleted and logged."}
    else:
        logging.error(f"Workout {workout_id} not found in memory.")
        return {"status": "error", "message": "Workout not found."}


def get_deleted_workouts():
    """
    Retrieves all workouts that have been deleted and logged.

    Args:
        None

    Returns:
        dict: A dictionary containing a list of all deleted workouts.

    Raises:
        None
    """
    logging.info("Fetching all deleted workouts.")
    return {"deleted_workouts": deleted_workouts}
