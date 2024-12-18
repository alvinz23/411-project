import logging

def configure_logger(logger_name: str):
    """
    Configures and returns a logger with a specific name.

    Args:
        logger_name (str): String representing the logger name.

    Returns:
        Configured logger.
    """
    logger = logging.getLogger(logger_name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
