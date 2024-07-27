# file: src/database/connection.py

from google.cloud import bigquery, storage
from google.oauth2 import service_account
from src.utils.config import config
from src.utils.logging import Logger

logger = Logger().logger

class BigQueryConnection:
    _instance = None

    @classmethod
    def get_client(cls):
        if cls._instance is None:
            cls._instance = cls._create_client()
        return cls._instance

    @staticmethod
    def _create_client():
        try:
            credentials = service_account.Credentials.from_service_account_file(config.SERVICE_ACCOUNT_FILE)
            return bigquery.Client(credentials=credentials, project=config.PROJECT_ID)
        except Exception as e:
            logger.error(f"Error creating BigQuery client: {str(e)}")
            raise

class StorageConnection:
    _instance = None

    @classmethod
    def get_client(cls):
        if cls._instance is None:
            cls._instance = cls._create_client()
        return cls._instance

    @staticmethod
    def _create_client():
        try:
            credentials = service_account.Credentials.from_service_account_file(config.SERVICE_ACCOUNT_FILE)
            return storage.Client(credentials=credentials, project=config.PROJECT_ID)
        except Exception as e:
            logger.error(f"Error creating Storage client: {str(e)}")
            raise

def get_bigquery_client():
    return BigQueryConnection.get_client()

def get_storage_client():
    return StorageConnection.get_client()

def test_connections():
    try:
        bigquery_client = get_bigquery_client()
        storage_client = get_storage_client()
        logger.info("Connection test successful. Both BigQuery and Storage clients created.")
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_connections()