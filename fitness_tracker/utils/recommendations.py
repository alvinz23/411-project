import random

# Predefined workout recommendations (example)
WORKOUT_RECOMMENDATIONS = [
    {"type": "cardio", "name": "Running", "duration": "30 minutes", "calories_burned": 300},
    {"type": "strength", "name": "Push-ups", "duration": "10 minutes", "calories_burned": 50},
    {"type": "flexibility", "name": "Yoga", "duration": "20 minutes", "calories_burned": 100},
    {"type": "strength", "name": "Weight Lifting", "duration": "30 minutes", "calories_burned": 250},
    {"type": "cardio", "name": "Cycling", "duration": "45 minutes", "calories_burned": 400},
]

def get_workout_recommendations(goal_type: str = None, num_recommendations: int = 3):
    """
    Get workout recommendations based on goal type.

    Args:
        goal_type (str): Type of the user's goal (e.g., "weight_loss", "exercise").
        num_recommendations (int): Number of recommendations to return.

    Returns:
        list: List of workout recommendations.
    """
    if goal_type:
        filtered_workouts = [w for w in WORKOUT_RECOMMENDATIONS if w["type"] == goal_type.lower()]
    else:
        filtered_workouts = WORKOUT_RECOMMENDATIONS

    return random.sample(filtered_workouts, min(num_recommendations, len(filtered_workouts)))
