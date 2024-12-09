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
    Create a new user account.

    Accepts a JSON payload with 'username' and 'password' to create a new user.

    Args:
        None (expects a JSON payload with 'username' and 'password').

    Returns:
        Response: JSON response indicating success or failure.
            - 201: Account created successfully.
            - 400: Validation error or username already taken.

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
    Authenticate a user login.

    Accepts a JSON payload with 'username' and 'password' to authenticate the user.

    Args:
        None (expects a JSON payload with 'username' and 'password').

    Returns:
        Response: JSON response indicating success or failure.
            - 200: Login successful.
            - 401: Invalid username or password.

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
    Update a user's password.

    Accepts a JSON payload with 'username' and 'new_password' to update the password.

    Args:
        None (expects a JSON payload with 'username' and 'new_password').

    Returns:
        Response: JSON response indicating success or failure.
            - 200: Password updated successfully.
            - 400: Validation error.
            - 500: Internal error during the update.

    Raises:
        Exception: If an error occurs during the password update.
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
    Display the home page of the Fitness Tracker app.

    Args:
        None

    Returns:
        Response: A plain text welcome message.
    """
    return "Welcome to the Fitness Tracker App!"


# Workout Management Routes
@app.route('/workouts/<int:workout_id>', methods=['POST'])
def add_workout(workout_id):
    """
    Add a workout to memory.

    Args:
        workout_id (int): The ID of the workout to add.

    Returns:
        Response: JSON response indicating success or failure.
            - 201: Workout added successfully.
            - 400: Workout not found or already exists.

    Raises:
        None
    """
    result = add_workout_to_memory(workout_id)
    if result["status"] == "success":
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@app.route('/workouts', methods=['GET'])
def list_workouts():
    """
    Retrieve all stored workouts.

    Args:
        None

    Returns:
        Response: JSON response containing a list of all stored workouts.
    """
    return jsonify(get_workouts()), 200


@app.route('/workouts/<int:workout_id>', methods=['PUT'])
def update_workout_route(workout_id):
    """
    Update workout details.

    Args:
        workout_id (int): The ID of the workout to update.

    Returns:
        Response: JSON response indicating success or failure.
            - 200: Workout updated successfully.
            - 400: Validation error.
            - 404: Workout not found.

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
        return jsonify(result), 200
    else:
        return jsonify(result), 404


@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout_route(workout_id):
    """
    Delete a workout from memory.

    Args:
        workout_id (int): The ID of the workout to delete.

    Returns:
        Response: JSON response indicating success or failure.
            - 200: Workout deleted successfully.
            - 404: Workout not found.

    Raises:
        None
    """
    result = delete_workout(workout_id)
    if result["status"] == "success":
        return jsonify(result), 200
    else:
        return jsonify(result), 404


@app.route('/workouts/deleted', methods=['GET'])
def list_deleted_workouts():
    """
    Retrieve all deleted workouts.

    Args:
        None

    Returns:
        Response: JSON response containing a list of all deleted workouts.
    """
    return jsonify(get_deleted_workouts()), 200


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check route to verify the app is running.

    Args:
        None

    Returns:
        Response: JSON response indicating the health status.
            - 200: App is running and healthy.
    """
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
