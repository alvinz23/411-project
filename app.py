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

@app.route('/create-account', methods=['POST'])
def create_account():
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
    return "Welcome to the Fitness Tracker App!"


# Workout Management Routes
@app.route('/workouts/<int:workout_id>', methods=['POST'])
def add_workout(workout_id):
    result = add_workout_to_memory(workout_id)
    if result["status"] == "success":
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@app.route('/workouts', methods=['GET'])
def list_workouts():
    return jsonify(get_workouts()), 200


@app.route('/workouts/<int:workout_id>', methods=['PUT'])
def update_workout_route(workout_id):
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
    result = delete_workout(workout_id)
    if result["status"] == "success":
        return jsonify(result), 200
    else:
        return jsonify(result), 404


@app.route('/workouts/deleted', methods=['GET'])
def list_deleted_workouts():
    return jsonify(get_deleted_workouts()), 200

if __name__ == "__main__":
    app.run(debug=True)

