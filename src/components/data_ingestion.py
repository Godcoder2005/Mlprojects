import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# 🧠 STEP 1: Dynamically find the project root directory
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# 🧩 STEP 2: Define config paths relative to project root
@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join(ROOT_DIR, 'artifacts', 'train.csv')
    test_data_path: str = os.path.join(ROOT_DIR, 'artifacts', 'test.csv')  # fixed 'text.csv' typo
    raw_data_path: str = os.path.join(ROOT_DIR, 'artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # 🧠 STEP 3: Define full absolute path to your input file
            file_path = os.path.join(ROOT_DIR, 'notebook', 'data', 'stud.csv')
            logging.info(f"Reading dataset from: {file_path}")
            
            df = pd.read_csv(file_path)
            logging.info('Read the dataset as dataframe')

            # 🧱 STEP 4: Ensure the artifacts directory exists
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # 🗂️ STEP 5: Save raw data snapshot
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Train test split initiated")

            # 🧪 STEP 6: Split data into train and test sets
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # 💾 STEP 7: Save the train and test CSVs
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            # ✅ STEP 8: Return file paths for next steps
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.info("Exception occurred at data ingestion stage")
            raise CustomException(e, sys)
        

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    print("Data ingestion completed successfully!")
    print("Train file:", train_data)
    print("Test file:", test_data)
