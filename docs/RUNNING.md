# Steps to Run the Fitness Tracker App

## Prerequisites
Manage workout routines by interacting with the Wger API, no API key is needed.
Install Python (3.9 or above).
 Install required Python packages:
   pip install -r requirements.txt

1. Ensure you have Docker installed and running.
2. Clone this repository:
   ```bash
   git clone <repo-url>
   cd <project-directory>
3. Build docker image with
   docker build -t fitness-tracker-app .
4. Run with
   docker run -p 5000:5000 fitness-tracker-app
5. Open new terminal and run
   ./smoketest.sh 

## Documentation
For setup, environment variables, and smoke test output, see the [`docs/`](./docs/) directory.


## UNIT TESTING 
1. Navigate to 411-project 
2. Run the python app - python app.py
3. Open a new terminal and run this command to test initially 

curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}' http://127.0.0.1:5000/create-account 

Should create an account successfully, restart if you want to unit test with a new userbase.

To test user_model.py 

4. python -m unittest tests/test_user_model.py

Warnings raised on purpose to account for incorrectly changing passwords on a user that does not exist.

To test workout_model.py 

5. python -m unittest tests/test_workout_model.py


## Full test flow with curl command, make sure python app.py is running and http://127.0.0.1:5000 is active. 

# 1. Add a Workout
curl -X POST http://127.0.0.1:5000/workouts/85

# 2. List All Stored Workouts
curl http://127.0.0.1:5000/workouts

# 3. Update the Workout
curl -X PUT -H "Content-Type: application/json" \
-d '{"name": "Updated Push-Up", "description": "Updated description for Push-Up."}' \
http://127.0.0.1:5000/workouts/85

# 4. Delete the Workout
curl -X DELETE http://127.0.0.1:5000/workouts/85

# 5. View Deleted Workouts
curl http://127.0.0.1:5000/workouts/deleted
