from flask import Flask, request, jsonify
from fitness_tracker.models.user_model import create_user, authenticate_user, change_password
from fitness_tracker.models.workout_model import (
    check_workout_in_api,
    add_workout_to_memory,
    get_workouts,
    update_workout,
    delete_workout,
    get_deleted_workouts,
)

app = Flask(__name__)
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(), 
    ],
)


@app.route('/create-account', methods=['POST'])
def create_account():
    """
    Creates a new user account.

    Args:
        None (expects a JSON payload with 'username' and 'password' fields).

    Returns:
        Response: JSON response with:
            - Success message and status code 201 if the account is created successfully.
            - Error message and status code 400 if validation fails or a duplicate username exists.

    Raises:
        ValueError: If the username is already taken.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    try:
        create_user(username, password)
        return jsonify({"message": "Account created successfully."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user login.

    Args:
        None (expects a JSON payload with 'username' and 'password' fields).

    Returns:
        Response: JSON response with:
            - Success message and status code 200 if authentication is successful.
            - Error message and status code 401 if authentication fails.

    Raises:
        None
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    if authenticate_user(username, password):
        return jsonify({"message": "Login successful."}), 200
    else:
        return jsonify({"error": "Invalid username or password."}), 401

@app.route('/update-password', methods=['POST'])
def update_password():
    """
    Updates a user's password.

    Args:
        None (expects a JSON payload with 'username' and 'new_password' fields).

    Returns:
        Response: JSON response with:
            - Success message and status code 200 if the password is updated successfully.
            - Error message and status code 500 if an error occurs during the update.

    Raises:
        Exception: If the password update process encounters an error.
    """
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')

    if not username or not new_password:
        return jsonify({"error": "Username and new password are required."}), 400

    try:
        change_password(username, new_password)
        return jsonify({"message": "Password updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/')
def home():
    """
    Displays the home page of the Fitness Tracker app.

    Args:
        None

    Returns:
        Response: Plain text message welcoming the user to the app.

    Raises:
        None
    """
    return "Welcome to the Fitness Tracker App!"


# Workout Management Routes
@app.route('/workouts/<int:workout_id>', methods=['POST'])
def add_workout(workout_id):
    """
    Adds a workout to memory.

    Args:
        workout_id (int): The ID of the workout to add.

    Returns:
        Response: JSON response with:
            - The workout details and status code 201 if successful.
            - Error message and status code 400 if the addition fails.

    Raises:
        None
    """ 
    result = add_workout_to_memory(workout_id)
    if result["status"] == "success":
        logger.info("Workout added successfully.")
        return jsonify(result), 201
    else:
        logger.error("Failed to add workout.")
        return jsonify(result), 400


@app.route('/workouts', methods=['GET'])
def list_workouts():
    """
    Retrieves all workouts stored in memory.

    Args:
        None

    Returns:
        Response: JSON response with a list of all stored workouts and status code 200.

    Raises:
        None
    """
    logger.info("Listing workouts:")
    return jsonify(get_workouts()), 200


@app.route('/workouts/<int:workout_id>', methods=['PUT'])
def update_workout_route(workout_id):
    """
    Updates a workout's details.

    Args:
        workout_id (int): The ID of the workout to update.

    Returns:
        Response: JSON response with:
            - Success message and status code 200 if the update is successful.
            - Error message and status code 404 if the workout is not found.

    Raises:
        None
    """
    data = request.json
    new_name = data.get("name")
    new_description = data.get("description")
    if not new_name or not new_description:
        return jsonify({"error": "Name and description are required."}), 400

    result = update_workout(workout_id, new_name, new_description)
    if result["status"] == "success":
        logger.info("Workout updated successfully.")
        return jsonify(result), 200
    else:
        logger.error("Failed to update workout.")
        return jsonify(result), 404


@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout_route(workout_id):
    """
    Deletes a workout from memory.

    Args:
        workout_id (int): The ID of the workout to delete.

    Returns:
        Response: JSON response with:
            - Success message and status code 200 if the deletion is successful.
            - Error message and status code 404 if the workout is not found.

    Raises:
        None
    """
    result = delete_workout(workout_id)
    if result["status"] == "success":
        logger.info("Workout deleted successfully.")
        return jsonify(result), 200
    else:
        logger.error("Failed to delete workout.")
        return jsonify(result), 404


@app.route('/workouts/deleted', methods=['GET'])
def list_deleted_workouts():
    """
    Retrieves all workouts that have been deleted and logged.

    Args:
        None

    Returns:
        Response: JSON response with a list of deleted workouts and status code 200.

    Raises:
        None
    """
    logger.info("List of deleted workouts:")
    return jsonify(get_deleted_workouts()), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check route to verify the app is running."""
    logger.info("App is healthy.")
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
