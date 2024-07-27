# file: src/utils/config.py

import os
from dotenv import load_dotenv
from pathlib import Path

class Config:
    def __init__(self, load_env=True):
        if load_env:
            # Get the path to the directory containing this file
            base_dir = Path(__file__).resolve().parent.parent.parent
            # Construct the path to the .env file
            dotenv_path = base_dir / '.env'
            # Load the .env file
            load_dotenv(dotenv_path)

        self.SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
        self.PROJECT_ID = os.getenv('PROJECT_ID')
        self.BUCKET_NAME = os.getenv('BUCKET_NAME')
        self.BLOB_NAME = os.getenv('BLOB_NAME')
        self.DATASET_NAME = os.getenv('DATASET_NAME')
        self.FEEDBACK_TABLE_NAME = os.getenv('FEEDBACK_TABLE_NAME')
        self.SENTIMENT_TABLE_NAME = os.getenv('SENTIMENT_TABLE_NAME')
        self.TEMP_TABLE_NAME = os.getenv('TEMP_TABLE_NAME')

        self.DEFAULT_ROW_LIMIT = int(os.getenv('DEFAULT_ROW_LIMIT', 100))
        self.SENTIMENT_BATCH_SIZE = int(os.getenv('SENTIMENT_BATCH_SIZE', 1000))

        self.FEEDBACK_SCHEMA = [
            {"name": "Id", "type": "STRING", "mode": "REQUIRED"},
            {"name": "Review", "type": "STRING", "mode": "REQUIRED"},
            {"name": "Label", "type": "STRING", "mode": "NULLABLE"},
        ]

        self.SENTIMENT_SCHEMA = [
            {"name": "Id", "type": "STRING", "mode": "REQUIRED"},
            {"name": "Score", "type": "FLOAT", "mode": "REQUIRED"},
            {"name": "Magnitude", "type": "FLOAT", "mode": "REQUIRED"},
        ]

        self.GCS_CSV_PATH = f"gs://{self.BUCKET_NAME}/{self.BLOB_NAME}" if self.BUCKET_NAME and self.BLOB_NAME else None

        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

config = Config()
