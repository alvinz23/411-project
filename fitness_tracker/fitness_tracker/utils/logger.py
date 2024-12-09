import logging
import sys
from flask import current_app, has_request_context


def configure_logger(logger: logging.Logger, level: int = logging.DEBUG):
    """
    Configures the logging for the Fitness Tracker application.

    Args:
        logger (logging.Logger): The logger to configure.
        level (int): Logging level (e.g., logging.DEBUG, logging.INFO). Default is DEBUG.
    """
    # Set the logger level
    logger.setLevel(level)

    # Create a console handler that logs to stderr
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)

    # Create a formatter with timestamp and additional information
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    # If Flask request context exists, add Flask's logger handlers
    if has_request_context():
        app_logger = current_app.logger
        for handler in app_logger.handlers:
            logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a logger with a pre-configured setup.

    Args:
        name (str): The name of the logger, typically the module name.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(name)
    configure_logger(logger)
    return logger
