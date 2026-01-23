import os
import sys

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion started")
        try:
            # Load dataset
            df = pd.read_csv('notebook\data\stud.csv') 
            logging.info("Dataset loaded successfully")

            # Create artifacts directory if it doesn't exist
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            # Save raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Raw data saved")

            # Split dataset into training and testing sets
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            logging.info("Dataset split into training and testing sets")

            # Save training data
            train_set.to_csv(self.ingestion_config.train_data_path, index=False)
            logging.info("Training data saved")

            # Save testing data
            test_set.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("Testing data saved")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.error("Error occurred during data ingestion")
            raise CustomException(e, sys)


if __name__ == "__main__":
    # This block runs when you execute: python src/components/data_ingestion.py
    logging.info("Starting Data Ingestion Pipeline")

    obj = DataIngestion()
    train_path, test_path = obj.initiate_data_ingestion()

    logging.info(f"Data ingestion completed successfully")
    logging.info(f"Training data saved at: {train_path}")
    logging.info(f"Testing data saved at: {test_path}")
