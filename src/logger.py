import logging
import os
import datetime

# 1. Setup the Log Directory and Filename
# Create a 'logs' folder in the same directory as this script
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Generate the full path with a timestamped filename
log_filename = f"app_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, log_filename)


def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger that writes to both console and a file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Check if handlers already exist to prevent duplicate logs if function is called twice
    if not logger.hasHandlers():
        # --- Handler 1: Console (StreamHandler) ---
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # --- Handler 2: File (FileHandler) ---
        # This is the new part that writes to the file
        fh = logging.FileHandler(log_file)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
