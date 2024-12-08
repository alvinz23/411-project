import logging
import random
from fitness_tracker.utils.fitness_logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)


def get_random_workout(workouts: list) -> dict:
    """
    Retrieves a random workout from a list of workouts.

    Args:
        workouts (list): A list of available workouts, each represented as a dictionary.

    Returns:
        dict: A randomly selected workout.

    Raises:
        ValueError: If the workouts list is empty or invalid.
    """
    logger.info("Selecting a random workout from the provided list.")
    if not workouts:
        logger.error("No workouts available to select.")
        raise ValueError("The workouts list is empty.")
    
    selected_workout = random.choice(workouts)
    logger.info("Selected workout: %s", selected_workout)
    return selected_workout


def get_random_number(low: float = 0, high: float = 1) -> float:
    """
    Generates a random float between two bounds.

    Args:
        low (float): The lower bound (inclusive). Default is 0.
        high (float): The upper bound (exclusive). Default is 1.

    Returns:
        float: A randomly generated number within the specified range.
    """
    logger.info("Generating a random number between %.2f and %.2f", low, high)
    random_number = random.uniform(low, high)
    logger.info("Generated random number: %.3f", random_number)
    return random_number


def get_random_integer(low: int, high: int) -> int:
    """
    Generates a random integer between two bounds.

    Args:
        low (int): The lower bound (inclusive).
        high (int): The upper bound (inclusive).

    Returns:
        int: A randomly generated integer within the specified range.
    """
    logger.info("Generating a random integer between %d and %d", low, high)
    random_integer = random.randint(low, high)
    logger.info("Generated random integer: %d", random_integer)
    return random_integer
