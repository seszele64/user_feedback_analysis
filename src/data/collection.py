"""
This module handles the collection and processing of user feedback data.

It includes functions for loading CSV data into BigQuery.
"""

from src.database import load_csv_to_bigquery
from src.utils import config, Logger

logger = Logger().logger


def main():
    try:
        # Define the parameters for load_csv_to_bigquery
        bucket_name = config.BUCKET_NAME  # Get bucket name from config
        blob_name = config.BLOB_NAME  # Get blob name from config
        # Assuming you have this in your config
        table_name = config.FEEDBACK_TABLE_NAME

        # Load CSV to BigQuery
        load_csv_to_bigquery(bucket_name, blob_name, table_name)
        logger.info(
            f"Successfully loaded CSV data from gs://{bucket_name}/{blob_name} to BigQuery table {table_name}.")

    except Exception as e:
        logger.error("Error in main function: %s", str(e))
        raise


if __name__ == "__main__":
    main()
