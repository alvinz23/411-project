import requests

# In-memory storage for workouts
stored_workouts = {}
deleted_workouts = []

# Wger API URL
WGER_API_BASE_URL = "https://wger.de/api/v2/exercise/"


def check_workout_in_api(workout_id):
    """Check if an exercise exists in the wger API by ID."""
    url = f"{WGER_API_BASE_URL}{workout_id}/?language=2"
    response = requests.get(url)
    if response.status_code == 200:
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
        return None


def add_workout_to_memory(workout_id):
    """Add a workout to memory after verifying it exists."""
    if workout_id in stored_workouts:
        return {"status": "error", "message": "Workout already exists in memory."}

    workout = check_workout_in_api(workout_id)
    if workout:
        stored_workouts[workout_id] = workout
        return {"status": "success", "message": "Workout added to memory.", "workout": workout}
    else:
        return {"status": "error", "message": "Workout not found in API."}


def get_workouts():
    """Retrieve all stored workouts."""
    return {"stored_workouts": list(stored_workouts.values())}


def update_workout(workout_id, new_name, new_description):
    """Update workout details."""
    if workout_id in stored_workouts:
        stored_workouts[workout_id]["name"] = new_name
        stored_workouts[workout_id]["description"] = new_description.strip()
        return {"status": "success", "message": "Workout updated."}
    else:
        return {"status": "error", "message": "Workout not found."}


def delete_workout(workout_id):
    """Delete a workout and log it in deleted_workouts."""
    if workout_id in stored_workouts:
        deleted_workouts.append(stored_workouts[workout_id])
        del stored_workouts[workout_id]
        return {"status": "success", "message": "Workout deleted and logged."}
    else:
        return {"status": "error", "message": "Workout not found."}


def get_deleted_workouts():
    """Retrieve all deleted workouts."""
    return {"deleted_workouts": deleted_workouts}
