# file: src/database/data_operations.py

# Third-party imports
from google.cloud import bigquery
from google.api_core import exceptions

# Local application/library specific imports
from src.utils import config, Logger
from src.database import get_bigquery_client

logger = Logger().logger

def create_table_if_not_exists(client, table_id, schema):
    """
    Creates a table if it doesn't exist in BigQuery.

    Args:
        client (google.cloud.bigquery.Client): The BigQuery client.
        table_id (str): The fully-qualified table ID (project.dataset.table).
        schema (List[bigquery.SchemaField]): The schema of the table.

    Raises:
        Exception: If there's an error during table creation.
    """
    try:
        table = bigquery.Table(table_id, schema=schema)
        client.get_table(table)
        logger.info(f"Table {table_id} already exists.")
    except exceptions.NotFound:
        try:
            table = client.create_table(table)
            logger.info(f"Created table {table_id}")
        except exceptions.Conflict:
            logger.info(f"Table {table_id} was created concurrently.")
    except Exception as e:
        logger.error(f"Error checking/creating table {table_id}: {str(e)}")
        raise

def setup_feedback_table(client):
    """
    Sets up the feedback table in BigQuery.

    Args:
        client (google.cloud.bigquery.Client): The BigQuery client.
    """
    table_id = f"{config.PROJECT_ID}.{config.DATASET_NAME}.{config.FEEDBACK_TABLE_NAME}"
    schema = [
        bigquery.SchemaField("Id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Review", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Label", "STRING", mode="NULLABLE"),
    ]
    create_table_if_not_exists(client, table_id, schema)

def setup_sentiment_table(client):
    """
    Sets up the sentiment table in BigQuery.

    Args:
        client (google.cloud.bigquery.Client): The BigQuery client.
    """
    table_id = f"{config.PROJECT_ID}.{config.DATASET_NAME}.{config.SENTIMENT_TABLE_NAME}"
    schema = [
        bigquery.SchemaField("Id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Score", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("Magnitude", "FLOAT", mode="REQUIRED"),
    ]
    create_table_if_not_exists(client, table_id, schema)

def setup_tables():
    """
    Sets up all required tables in BigQuery.
    """
    client = get_bigquery_client()
    try:
        setup_feedback_table(client)
        setup_sentiment_table(client)
        logger.info("All tables have been set up successfully.")
    except Exception as e:
        logger.error(f"Error in setup_tables: {str(e)}")
        raise

if __name__ == "__main__":
    setup_tables()
