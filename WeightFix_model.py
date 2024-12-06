import logging
from typing import List


from meal_max.utils.logger import configure_logger



logger = logging.getLogger(__name__)
configure_logger(logger)


class WeightFix:
    """Allows users to set fitness goals for themselves and get workout recommendations.

    Attributes:
        weight (int): User's current weight.
        age (int): User's age.
        height (int): User's height in inches.
    """

    def __init__(self, weight, age, height):
        """Initializes a new WeightLoss instance with the user's body information.
        
        Raises:
            TypeError: If any inputs are not integers.
        """
        if type(self.height) != int or type(self.weight) != int or type(self.age) != int:
            logger.error("Invalid type input.")
            raise TypeError("All attributes must have integer values.")
        else:
            self.height = height
            self.weight = weight
            self.age = age

    def set_goal(self, weight_goal):
        """Sets the user's weight goal.

        Parameters:
            weight_goal (int): The user's goal weight.
        
        Returns:
            str: String stating the amount of weight the user must lose or gain to reach their goal.

        Raises:
            TypeError: If the weight goal is not an integer.
            ValueError: if the weight goal equals your current weight.
        """

        logger.info("Set your goal weight.")

        if type(weight_goal) != int:
            logger.error("Invalid type input.")
            raise TypeError("Your goal weight must be an integer.")
        else:

            # Log the user's goal weight
            logger.info("Goal weight = ", weight_goal)
            
            #compute the weight gain or loss needed to reach goal
            if weight_goal > self.weight:
                gain = weight_goal - self.weight
                logger.info("You must gain ",gain, " pounds.")
            elif weight_goal < self.weight:
                loss = self.weight - weight_goal
                logger.info("You must lose ", loss, " pounds.")
            else:
                logger.error("You already weigh ", weight_goal, " pounds.")
                raise ValueError("Your goal weight cannot equal your current weight")
    

    def log_workout(self, type, duration):
        """Logs each workout the user inputs, including the type of exercise and its duration
        
        Parameters:
            type (str): Type of exercise done: can either be "cardio" or "lifting".
            duration (float): Time spent on specific exercise in hours (30 mins = 0.5 hours)

        Raises:
            TypeError: If the exercise type is not a string or the duration is not a number.
            ValueError: If the exercise type is not a valid option.
        
        """
        if type(type) != str:
            raise TypeError("Exercise type must be a string.")
        if type(duration) != int or type(duration) != float:
            raise TypeError("Exercise duration must be a number.")
        if type != "cardio" or type != "lifting":
            raise ValueError("Invalid exercise type.")
        
        logger.info("Logging workout data: ", type, " for ", duration, " hours.")
        


    
    