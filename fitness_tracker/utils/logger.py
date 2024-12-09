import logging

def configure_logger(logger_name: str):
    """
    Configures and returns a logger instance with the specified name and log level.

    Args:
        logger_name (str): The name of the logger.
        level (int): The log level (default is logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.

    Raises:
        ValueError: If an invalid log level is provided.
    """
    logger = logging.getLogger(logger_name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
