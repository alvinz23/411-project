from dataclasses import dataclass
import logging
import sqlite3
from typing import Any, List
from fitness_tracker.utils.sql_utils import get_db_connection
from fitness_tracker.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)


@dataclass
class Goal:
    """
    A class to manage fitness goals.

    Attributes:
        id (int): Unique ID of the goal.
        user_id (int): ID of the user associated with the goal.
        goal_type (str): Type of the goal (e.g., "weight_loss").
        target_value (float): Target value for the goal (e.g., weight to lose, hours to exercise).
        progress (float): Current progress toward the goal.
        start_date (str): Date when the goal starts.
        end_date (str): Deadline for achieving the goal.
    """
    id: int
    user_id: int
    goal_type: str
    target_value: float
    progress: float
    start_date: str
    end_date: str

    def __post_init__(self):
        """
        Ensures the target value and progress are non-negative.
        """
        if self.target_value <= 0:
            raise ValueError("Target value must be greater than zero.")
        if self.progress < 0:
            raise ValueError("Progress cannot be negative.")


def create_goal(user_id: int, goal_type: str, target_value: float, end_date: str) -> None:
    """
    Creates a new fitness goal for a user.

    Args:
        user_id (int): ID of the user.
        goal_type (str): Type of the goal (e.g., "weight_loss").
        target_value (float): Target value for the goal.
        end_date (str): Deadline for achieving the goal.

    Raises:
        ValueError: If input values are invalid.
        sqlite3.Error: If there is an issue with the database.
    """
    if target_value <= 0:
        raise ValueError("Target value must be a positive number.")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO goals (user_id, goal_type, target_value, progress, start_date, end_date)
                VALUES (?, ?, ?, 0, DATE('now'), ?)
            """, (user_id, goal_type, target_value, end_date))
            conn.commit()
            logger.info("Goal successfully added for user ID %d", user_id)

    except sqlite3.Error as e:
        logger.error("Database error while creating goal: %s", str(e))
        raise e


def get_goal_by_id(goal_id: int) -> Goal:
    """
    Retrieves a goal by its ID.

    Args:
        goal_id (int): The ID of the goal.

    Returns:
        Goal: The goal object.

    Raises:
        ValueError: If the goal does not exist.
        sqlite3.Error: If there is an issue with the database.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, user_id, goal_type, target_value, progress, start_date, end_date
                FROM goals WHERE id = ?
            """, (goal_id,))
            row = cursor.fetchone()

            if row:
                return Goal(id=row[0], user_id=row[1], goal_type=row[2], target_value=row[3],
                            progress=row[4], start_date=row[5], end_date=row[6])
            else:
                logger.warning("Goal with ID %d not found", goal_id)
                raise ValueError(f"Goal with ID {goal_id} not found")

    except sqlite3.Error as e:
        logger.error("Database error while retrieving goal by ID: %s", str(e))
        raise e


def update_goal_progress(goal_id: int, progress: float) -> None:
    """
    Updates the progress of a specific goal.

    Args:
        goal_id (int): The ID of the goal.
        progress (float): The new progress value.

    Raises:
        ValueError: If the goal does not exist or progress is invalid.
        sqlite3.Error: If there is an issue with the database.
    """
    if progress < 0:
        raise ValueError("Progress cannot be negative.")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM goals WHERE id = ?", (goal_id,))
            if not cursor.fetchone():
                logger.warning("Goal with ID %d not found for progress update.", goal_id)
                raise ValueError(f"Goal with ID {goal_id} not found.")

            cursor.execute("""
                UPDATE goals
                SET progress = ?
                WHERE id = ?
            """, (progress, goal_id))
            conn.commit()
            logger.info("Progress updated for goal ID %d to %.2f", goal_id, progress)

    except sqlite3.Error as e:
        logger.error("Database error while updating goal progress: %s", str(e))
        raise e


def delete_goal(goal_id: int) -> None:
    """
    Deletes a goal by marking it as removed.

    Args:
        goal_id (int): The ID of the goal to delete.

    Raises:
        ValueError: If the goal does not exist.
        sqlite3.Error: If there is an issue with the database.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
            conn.commit()
            logger.info("Goal with ID %d deleted successfully.", goal_id)

    except sqlite3.Error as e:
        logger.error("Database error while deleting goal: %s", str(e))
        raise e


def get_all_goals(user_id: int) -> List[Goal]:
    """
    Retrieves all goals for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Goal]: A list of the user's goals.

    Raises:
        sqlite3.Error: If there is an issue with the database.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, user_id, goal_type, target_value, progress, start_date, end_date
                FROM goals WHERE user_id = ?
            """, (user_id,))
            rows = cursor.fetchall()

            goals = [Goal(id=row[0], user_id=row[1], goal_type=row[2], target_value=row[3],
                          progress=row[4], start_date=row[5], end_date=row[6]) for row in rows]
            logger.info("Retrieved %d goals for user ID %d", len(goals), user_id)
            return goals

    except sqlite3.Error as e:
        logger.error("Database error while retrieving all goals: %s", str(e))
        raise e
    
def log_workout(user_id: int, workout_type: str, duration: int, calories_burned: float, date: str = None):
    """
    Logs a workout for a user.

    Args:
        user_id (int): ID of the user performing the workout.
        workout_type (str): Type of workout (e.g., "Running").
        duration (int): Duration of the workout in minutes.
        calories_burned (float): Estimated calories burned.
        date (str): Date of the workout in 'YYYY-MM-DD' format (defaults to today).

    Raises:
        ValueError: If input values are invalid.
        sqlite3.Error: If there is an issue with the database.
    """
    if duration <= 0 or calories_burned <= 0:
        raise ValueError("Duration and calories burned must be greater than zero.")

    if not date:
        from datetime import date as dt
        date = dt.today().isoformat()

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO workouts (user_id, workout_type, duration, calories_burned, date)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, workout_type, duration, calories_burned, date))
            conn.commit()
            logger.info("Workout logged successfully for user ID %d", user_id)
    except sqlite3.Error as e:
        logger.error("Error logging workout: %s", str(e))
        raise e

