Fitness Tracker - This application stores user account info and allows users to log, update, and delete their workouts, as well as track their progress.

Route Documentation

Route: /create-account

- Request type: POST
- Purpose: Creates a new user account with a username and password.
- Request Body:
    - username (String): User's chosen username.
    - password (String): User's chosen password.
- Response Format: JSON
    - Success Response Example:
        - Code 201
        - Content: {"message": "Account created successfully."}
- Example Request:
    {
        "username": "newuser"
        "password": "strongpassword"
    }
- Example Response:
    {
        "message": "Account created successfully."
        "status": "201"
    }


Route: /login

- Request type: POST
- Purpose: Logs in a user with their username and password.
- Request Body:
    - username (String): User's chosen username.
    - password (String): User's chosen password.
- Response Format: JSON
    - Success Response Example:
        - Code 200
        - Content: {"message": "Login successful."}
- Example Request:
    {
        "username": "currentuser"
        "password": "strongpassword"
    }
- Example Response:
    {
        "message": "Login successful."
        "status": "200"
    }


Route: /update-password

- Request type: POST
- Purpose: Updates a user's password.
- Request Body:
    - username (String): User's chosen username.
    - new_password (String): User's chosen new password.
- Response Format: JSON
    - Success Response Example:
        - Code 200
        - Content: {"message": "Password updated successfully."}
- Example Request:
    {
        "username": "currentuser"
        "new_password": "strongpassword"
    }
- Example Response:
    {
        "message": "Password updated successfully."
        "status": "200"
    }


Route: /workouts/<int:workout_id>

- Request type: POST
- Purpose: Logs a user's workout by the corresponding workout id.
- Request Body:
    - workout_id (int): ID number for a specific workout.
- Response Format: JSON
    - Success Response Example:
        - Code 201
        - Content: {"status == success"}
- Example Request:
    {
        "workout_id": 12
    }
- Example Response:
    {
        "status == success"
        "status": "201"
    }


Route: /workouts

- Request type: GET
- Purpose: Retrieves all stored workouts from a user.
- Response Format: JSON
    - Success Response Example:
        - Code 200
        - Content: {"stored_workouts": list(stored_workouts.values())}
- Example Request:
    {
        list_workouts()
    }
- Example Response:
    {
        "stored_workouts": " workout = {
            "id": 1,
            "name": "Push-Up",
            "description": "A bodyweight exercise",
            "muscles": [4],
            "equipment": [],
        }"
        "status": "200"
    }


Route: /workouts/<int:workout_id>

- Request type: PUT
- Purpose: Updates a previously stored workout.
- Request Body:
    - new_name (String): Name of new workout.
    - new_description (String): Description of new workout.
- Response Format: JSON
    - Success Response Example:
        - Code 200
        - Content: {"status == success"}
- Example Request:
    {
        "new_name": "bicep curl"
        "new_description": "A bicep exercise"
    }
- Example Response:
    {
        "status == success"
        "status": "200"
    }

Route: /workouts/<int:workout_id>

- Request type: DELETE
- Purpose: Deletes a previously stored workout.
- Request Body:
    - workout_id (int): ID of a specific workout.
- Response Format: JSON
    - Success Response Example:
        - Code 200
        - Content: {"status == success"}
- Example Request:
    {
        "workout_id": 5
    }
- Example Response:
    {
        "status == success"
        "status": "200"
    }


Route: /workouts/deleted

- Request type: GET
- Purpose: Retrieves all deleted workouts.
- Response Format: JSON
    - Success Response Example:
        - Code 200
        - Content: {"deleted_workouts": deleted_workouts}
- Example Request:
    {
        list_deleted_workouts()
    }
- Example Response:
    {
        "workout = {
            "id": 1,
            "name": "Push-Up",
            "description": "A bodyweight exercise",
            "muscles": [4],
            "equipment": [],
        }"
        "status": "200"
    }


