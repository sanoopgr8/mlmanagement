import logging
import os
import datetime


LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'app.log')
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
LOG_FILE = f"app_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"



def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name and logging level.

    Parameters:
    name (str): The name of the logger.
    level (int): The logging level (default is logging.INFO).

    Returns:
    logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger