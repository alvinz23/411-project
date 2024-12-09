import logging
from typing import List, Dict
from fitness_tracker.models.goal_model import Goal, update_goal_progress
from fitness_tracker.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


class ProgressTracker:
    """
    A class managing user fitness progress.

    Attributes:
        goals (List[Goal]): The list of goals being tracked for the user.
    """

    def __init__(self):
        """
        Initializes the ProgressTracker with an empty list of goals.
        """
        self.goals: List[Goal] = []

    def add_goal(self, goal: Goal):
        """
        Adds a fitness goal to the tracker.

        Args:
            goal (Goal): The goal to add to the tracker.

        Raises:
            ValueError: If the goal list is full or the goal is invalid.
        """
        logger.info("Adding a new fitness goal: %s", goal.goal_type)
        self.goals.append(goal)

    def track_progress(self) -> Dict[str, str]:
        """
        Evaluates progress for all goals and provides recommendations.

        Returns:
            Dict[str, str]: A dictionary with goal statuses and recommendations.
        """
        if not self.goals:
            logger.warning("No goals to track progress for.")
            return {"error": "No goals available to track progress."}

        progress_summary = {}
        for goal in self.goals:
            logger.info("Tracking progress for goal: %s", goal.goal_type)
            status = self.evaluate_goal(goal)
            progress_summary[goal.goal_type] = status

        return progress_summary

    def evaluate_goal(self, goal: Goal) -> str:
        """
        Evaluates a specific goal and determines the progress.

        Args:
            goal (Goal): The goal to evaluate.

        Returns:
            str: Status message about the goal's progress.
        """
        progress_percentage = (goal.progress / goal.target_value) * 100
        logger.info("Progress for goal '%s': %.2f%%", goal.goal_type, progress_percentage)

        if progress_percentage >= 100:
            return f"Goal '{goal.goal_type}' achieved! Congratulations!"
        elif progress_percentage >= 50:
            return f"Goal '{goal.goal_type}' is on track. Keep going!"
        else:
            return f"Goal '{goal.goal_type}' needs attention. Stay focused!"

    def update_progress(self, goal_id: int, progress: float):
        """
        Updates the progress of a specific goal.

        Args:
            goal_id (int): The ID of the goal to update.
            progress (float): The amount of progress to add.

        Raises:
            ValueError: If the goal does not exist.
        """
        logger.info("Updating progress for goal ID: %d", goal_id)
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            logger.error("Goal with ID %d not found.", goal_id)
            raise ValueError(f"Goal with ID {goal_id} not found.")

        goal.progress += progress
        logger.info("New progress for goal '%s': %.2f", goal.goal_type, goal.progress)
        update_goal_progress(goal.id, goal.progress)

    def get_goal_by_id(self, goal_id: int) -> Goal:
        """
        Retrieves a goal by its ID.

        Args:
            goal_id (int): The ID of the goal to retrieve.

        Returns:
            Goal: The goal with the specified ID, or None if not found.
        """
        logger.info("Retrieving goal by ID: %d", goal_id)
        for goal in self.goals:
            if goal.id == goal_id:
                return goal
        return None

    def remove_goal(self, goal_id: int):
        """
        Removes a goal by its ID.

        Args:
            goal_id (int): The ID of the goal to remove.

        Raises:
            ValueError: If the goal does not exist.
        """
        logger.info("Removing goal ID: %d", goal_id)
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            logger.error("Goal with ID %d not found.", goal_id)
            raise ValueError(f"Goal with ID {goal_id} not found.")

        self.goals.remove(goal)
        logger.info("Goal '%s' removed successfully.", goal.goal_type)