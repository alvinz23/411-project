from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request, Response
from fitness_tracker.models.goal_model import create_goal, get_goal_by_id, update_goal_progress, get_all_goals
from fitness_tracker.models.progress_tracker_model import ProgressTracker
from fitness_tracker.utils.sql_utils import check_database_connection, check_table_exists, initialize_database
from fitness_tracker.utils.fitness_logger import configure_logger
from fitness_tracker.utils.recommendations import get_workout_recommendations

# Load environment variables from .env file
load_dotenv()

# Configure Flask app
app = Flask(__name__)
logger = app.logger
configure_logger(logger)

# Initialize database
initialize_database()

####################################################
#
# Healthchecks
#
####################################################

@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return make_response(jsonify({'status': 'healthy'}), 200)


@app.route('/api/db-check', methods=['GET'])
def db_check() -> Response:
    """
    Route to check if the database connection and tables are functional.

    Returns:
        JSON response indicating the database health status.
    Raises:
        404 error if there is an issue with the database.
    """
    try:
        app.logger.info("Checking database connection...")
        check_database_connection()
        app.logger.info("Database connection is OK.")
        app.logger.info("Checking if goals table exists...")
        check_table_exists("goals")
        app.logger.info("Goals table exists.")
        return make_response(jsonify({'database_status': 'healthy'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 404)


####################################################
#
# Fitness Tracker Endpoints
#
####################################################

@app.route('/api/set-goals', methods=['POST'])
def set_goal() -> Response:
    """
    Route to set a fitness goal for a user.

    Expected JSON Input:
        - user_id (int): User ID.
        - goal_type (str): Type of the goal (e.g., "weight_loss").
        - target_value (float): Target value for the goal.
        - end_date (str): Deadline in 'YYYY-MM-DD' format.

    Returns:
        JSON response indicating success or failure.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    goal_type = data.get('goal_type')
    target_value = data.get('target_value')
    end_date = data.get('end_date')

    if not all([user_id, goal_type, target_value, end_date]):
        return make_response(jsonify({'error': 'Missing required fields'}), 400)

    try:
        create_goal(user_id, goal_type, target_value, end_date)
        return make_response(jsonify({'status': 'success'}), 201)
    except Exception as e:
        app.logger.error("Failed to set goal: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/get-goals/<int:user_id>', methods=['GET'])
def get_goals(user_id: int) -> Response:
    """
    Route to get all fitness goals for a user.

    Path Parameter:
        - user_id (int): The ID of the user.

    Returns:
        JSON response with the list of goals or an error message.
    """
    try:
        app.logger.info("Fetching goals for user ID: %d", user_id)
        goals = get_all_goals(user_id)
        return make_response(jsonify({'status': 'success', 'goals': [
            {
                'id': goal.id,
                'goal_type': goal.goal_type,
                'target_value': goal.target_value,
                'progress': goal.progress,
                'start_date': goal.start_date,
                'end_date': goal.end_date
            } for goal in goals
        ]}), 200)
    except Exception as e:
        app.logger.error("Error fetching goals: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/update-progress', methods=['PUT'])
def update_progress() -> Response:
    """
    Route to update progress for a fitness goal.

    Expected JSON Input:
        - goal_id (int): The ID of the goal to update.
        - progress (float): The amount of progress to add.

    Returns:
        JSON response indicating success or failure.
    """
    data = request.get_json()
    goal_id = data.get('goal_id')
    progress = data.get('progress')

    if not all([goal_id, progress]):
        return make_response(jsonify({'error': 'Missing required fields'}), 400)

    try:
        update_goal_progress(goal_id, progress)
        return make_response(jsonify({'status': 'success'}), 200)
    except Exception as e:
        app.logger.error("Failed to update progress: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/track-progress/<int:user_id>', methods=['GET'])
def track_progress(user_id: int) -> Response:
    """
    Route to track progress for all goals of a user.

    Path Parameter:
        - user_id (int): The ID of the user.

    Returns:
        JSON response with the progress report.
    """
    try:
        app.logger.info("Tracking progress for user ID: %d", user_id)
        tracker = ProgressTracker()
        goals = get_all_goals(user_id)
        for goal in goals:
            tracker.add_goal(goal)

        progress_summary = tracker.track_progress()
        return make_response(jsonify({'status': 'success', 'progress': progress_summary}), 200)
    except Exception as e:
        app.logger.error("Error tracking progress: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)
    
@app.route('/api/get-recommendations', methods=['GET'])
def get_recommendations() -> Response:
    """
    Get workout recommendations based on user goals.

    Query Parameters:
        - goal_type (str): Optional. Type of the user's goal (e.g., "weight_loss", "exercise").
        - num_recommendations (int): Optional. Number of recommendations to fetch (default is 3).

    Returns:
        JSON response with the workout recommendations.
    """
    goal_type = request.args.get('goal_type', None)
    num_recommendations = request.args.get('num_recommendations', 3)

    try:
        num_recommendations = int(num_recommendations)
    except ValueError:
        return make_response(jsonify({'error': 'num_recommendations must be an integer'}), 400)

    recommendations = get_workout_recommendations(goal_type, num_recommendations)

    return make_response(jsonify({'status': 'success', 'recommendations': recommendations}), 200)

@app.route('/api/log-workout', methods=['POST'])
def log_workout_endpoint() -> Response:
    """
    Logs a workout for a user.

    Expected JSON Input:
        - user_id (int): ID of the user.
        - workout_type (str): Type of the workout (e.g., "Running").
        - duration (int): Duration of the workout in minutes.
        - calories_burned (float): Estimated calories burned.
        - date (str): Date of the workout in 'YYYY-MM-DD' format (optional).

    Returns:
        JSON response indicating success or failure.
    """
    try:
        data = request.get_json()

        # Extract and validate input fields
        user_id = data.get('user_id')
        workout_type = data.get('workout_type')
        duration = data.get('duration')
        calories_burned = data.get('calories_burned')
        date = data.get('date', None)

        if not all([user_id, workout_type, duration, calories_burned]):
            return make_response(jsonify({'error': 'Missing required fields'}), 400)

        log_workout(user_id, workout_type, duration, calories_burned, date)

        return make_response(jsonify({'status': 'success'}), 201)
    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    except Exception as e:
        app.logger.error("Failed to log workout: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)
    
@app.route('/api/update-goal', methods=['PUT'])
def update_goal_endpoint() -> Response:
    """
    Updates an existing fitness goal.

    Expected JSON Input:
        - goal_id (int): ID of the goal to update.
        - goal_type (str): New goal type (optional).
        - target_value (float): New target value (optional).
        - end_date (str): New end date in 'YYYY-MM-DD' format (optional).

    Returns:
        JSON response indicating success or failure.
    """
    try:
        data = request.get_json()

        # Extract and validate input fields
        goal_id = data.get('goal_id')
        goal_type = data.get('goal_type')
        target_value = data.get('target_value')
        end_date = data.get('end_date')

        if not goal_id:
            return make_response(jsonify({'error': 'goal_id is required'}), 400)

        update_goal(goal_id, goal_type, target_value, end_date)

        return make_response(jsonify({'status': 'success'}), 200)
    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    except Exception as e:
        app.logger.error("Failed to update goal: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

############################################################
#
# Run the Application
#
############################################################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
