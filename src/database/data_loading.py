# file: src/database/data_loading.py

from google.cloud import bigquery
from src.utils.config import config
from src.database.connection import get_bigquery_client
from src.utils.logging import Logger

# Get the logger instance
logger = Logger().logger

def get_job_config(num_rows=None):
    """
    Creates and returns a job configuration for loading CSV data into BigQuery.

    Args:
        num_rows (int, optional): Number of rows to load. If None, loads all rows.

    Returns:
        google.cloud.bigquery.LoadJobConfig: A job configuration for CSV loading.
    """
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    if num_rows:
        job_config.max_bad_records = num_rows
    return job_config

def load_csv_to_bigquery(bucket_name, blob_name, table_name, num_rows=None):
    """
    Loads CSV data from Google Cloud Storage into a BigQuery table.

    Args:
        bucket_name (str): The name of the GCS bucket containing the CSV file.
        blob_name (str): The name of the CSV file in the GCS bucket.
        table_name (str): The name of the BigQuery table to load data into.
        num_rows (int, optional): Number of rows to load. If None, loads all rows.

    Raises:
        Exception: If there's an error during the loading process.
    """
    client = get_bigquery_client()
    try:
        table_id = f"{config.PROJECT_ID}.{config.DATASET_NAME}.{table_name}"
        uri = f"gs://{bucket_name}/{blob_name}"
        job_config = get_job_config(num_rows)

        load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
        load_job.result()  # Wait for the job to complete

        destination_table = client.get_table(table_id)
        logger.info(f"Loaded {destination_table.num_rows} rows into {table_id}")
    except Exception as e:
        logger.error(f"Error in load_csv_to_bigquery: {str(e)}")
        raise

if __name__ == "__main__":
    # This block will be executed when the script is run directly
    load_csv_to_bigquery(config.BUCKET_NAME, config.BLOB_NAME, config.FEEDBACK_TABLE_NAME, num_rows=10)
