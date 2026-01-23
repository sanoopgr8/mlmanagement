import os 
import sys
import numpy as np
import pandas as pd
import pickle
from src.exception import CustomException
from src.logger import logging


def save_object(file_path, obj):
    try:
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        logging.error("Error occurred while saving object")
        raise CustomException(e, sys)