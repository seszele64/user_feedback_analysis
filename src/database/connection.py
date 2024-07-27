from google.cloud import bigquery, storage
from google.oauth2 import service_account
from src.utils.config import config
from src.utils.logging import Logger

logger = Logger().logger

def get_bigquery_client():
    """
    Creates and returns a BigQuery client using the service account credentials.

    Returns:
        google.cloud.bigquery.Client: An authenticated BigQuery client.
    """
    try:
        credentials = service_account.Credentials.from_service_account_file(config.SERVICE_ACCOUNT_FILE)
        return bigquery.Client(credentials=credentials, project=config.PROJECT_ID)
    except Exception as e:
        logger.error(f"Error creating BigQuery client: {str(e)}")
        raise

def get_storage_client():
    """
    Creates and returns a Google Cloud Storage client using the service account credentials.

    Returns:
        google.cloud.storage.Client: An authenticated Google Cloud Storage client.
    """
    try:
        credentials = service_account.Credentials.from_service_account_file(config.SERVICE_ACCOUNT_FILE)
        return storage.Client(credentials=credentials, project=config.PROJECT_ID)
    except Exception as e:
        logger.error(f"Error creating Storage client: {str(e)}")
        raise

def test_connections():
    """
    Tests the BigQuery and Storage connections by creating clients.
    This function can be used to verify that the connections are working correctly.
    """
    try:
        bigquery_client = get_bigquery_client()
        storage_client = get_storage_client()
        logger.info("Connection test successful. Both BigQuery and Storage clients created.")
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_connections()
