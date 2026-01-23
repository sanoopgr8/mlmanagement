"""
Test script to verify logging is working
Run this from terminal: python test_logging.py
"""
from src.logger import logging

logging.info("Test 1: This is a test info message")
logging.warning("Test 2: This is a test warning message")
logging.error("Test 3: This is a test error message")

print("\nTest complete! Check the latest log file in src/logs/")
print("The log file will have a timestamp in its name: app_YYYYMMDD_HHMMSS.log")
