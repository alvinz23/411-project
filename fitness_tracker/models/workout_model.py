import requests
import logging


# In-memory storage for workouts
stored_workouts = {}
deleted_workouts = []

# Wger API URL
WGER_API_BASE_URL = "https://wger.de/api/v2/exercise/"


def check_workout_in_api(workout_id):
    """
    Check if an exercise exists in the Wger API by its ID.

    Sends a request to the Wger API to fetch workout details. If the workout exists,
    it returns a cleaned dictionary containing relevant details. If the workout
    does not exist, returns None.

    Args:
        workout_id (int): The ID of the workout to check.

    Returns:
        dict: A dictionary with the following keys if the workout exists:
            - id (int): The workout's unique ID.
            - name (str): The name of the workout.
            - description (str): A cleaned description of the workout.
            - muscles (list): A list of muscle IDs targeted by the workout.
            - equipment (list): A list of equipment IDs required for the workout.
        None: If the workout is not found in the API.

    Raises:
        requests.exceptions.RequestException: If there is an error with the API request.
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
    Add a workout to memory after verifying it exists.

    Checks if a workout exists in the Wger API by its ID. If the workout is valid
    and not already stored, it is added to the `stored_workouts` dictionary.

    Args:
        workout_id (int): The ID of the workout to add.

    Returns:
        dict: A dictionary with the operation's status and details:
            - status (str): Either "success" or "error".
            - message (str): Description of the operation outcome.
            - workout (dict, optional): The workout details if the operation succeeds.

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
    Retrieve all stored workouts.

    Fetches all workouts currently stored in the `stored_workouts` dictionary.

    Args:
        None

    Returns:
        dict: A dictionary containing:
            - stored_workouts (list): A list of all stored workout details.

    Raises:
        None
    """
    return {"stored_workouts": list(stored_workouts.values())}


def update_workout(workout_id, new_name, new_description):
    """
    Update workout details.

    Updates the name and description of a stored workout identified by its ID.

    Args:
        workout_id (int): The ID of the workout to update.
        new_name (str): The updated name for the workout.
        new_description (str): The updated description for the workout.

    Returns:
        dict: A dictionary with the operation's status and details:
            - status (str): Either "success" or "error".
            - message (str): Description of the operation outcome.

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
    Delete a workout and log it in deleted_workouts.

    Removes the specified workout from `stored_workouts` and appends it to
    the `deleted_workouts` list.

    Args:
        workout_id (int): The ID of the workout to delete.

    Returns:
        dict: A dictionary with the operation's status and details:
            - status (str): Either "success" or "error".
            - message (str): Description of the operation outcome.

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
    Retrieve all deleted workouts.

    Fetches all workouts that have been removed from `stored_workouts` and logged in `deleted_workouts`.

    Args:
        None

    Returns:
        dict: A dictionary containing:
            - deleted_workouts (list): A list of all deleted workout details.

    Raises:
        None
    """
    logging.info("Fetching all deleted workouts.")
    return {"deleted_workouts": deleted_workouts}
