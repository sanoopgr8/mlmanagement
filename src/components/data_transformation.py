import os
import sys

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.components import data_ingestion
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            logging.info("Data Transformation: Creating preprocessing object")

            # Define numerical and categorical columns
            numerical_cols = ['writing_score', 'reading_score']
            categorical_cols = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
            
            # Numerical pipeline
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            # Categorical pipeline
            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore')),
                ('scaler', StandardScaler(with_mean=False))
            ])
            # Combine pipelines
            preprocessor = ColumnTransformer(transformers=[
                ('num_pipeline', num_pipeline, numerical_cols),
                ('cat_pipeline', cat_pipeline, categorical_cols)
            ])
            return preprocessor
        except Exception as e:
            logging.error("Error occurred while creating data transformer object")
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self):
        try:
            logging.info("Data Transformation: Starting transformation process")

            # Get paths from data ingestion
            di = data_ingestion.DataIngestion()
            train_path, test_path = di.initiate_data_ingestion()

            # Load datasets
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Data Transformation: Datasets loaded successfully")

            # Separate features and target variable
            target_column_name = 'math_score'
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            # Get preprocessing object
            preprocessor_obj = self.get_data_transformer_object()

            # Fit and transform training data, transform testing data
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]  

            logging.info("Data Transformation: Data transformation completed successfully")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_path,
                obj=preprocessor_obj
            )

            return (
                input_feature_train_arr,
                input_feature_test_arr,
                target_feature_train_df,
                target_feature_test_df,
                train_arr,
                test_arr,
                preprocessor_obj,
                self.data_transformation_config.preprocessor_obj_path
            )

        except Exception as e:
            logging.error("Error occurred during data transformation")
            raise CustomException(e, sys)


if __name__ == "__main__":
    # This block runs when you execute: python src/components/data_transformation.py
    logging.info("Starting Data Transformation Pipeline")

    obj = DataTransformation()
    train_arr, test_arr, _, _, _, _, preprocessor_obj, preprocessor_path = obj.initiate_data_transformation()

    logging.info(f"Data transformation completed. Preprocessor saved at: {preprocessor_path}")
    logging.info(f"Training array shape: {train_arr.shape}")
    logging.info(f"Testing array shape: {test_arr.shape}")