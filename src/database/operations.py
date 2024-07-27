"""
This module contains operations for interacting with BigQuery tables.

It provides functions for loading data, setting up tables, inserting rows,
and querying data from BigQuery tables. The module is designed to work with
feedback and sentiment analysis data.

Functions:
    - Data Loading:
        - get_job_config
        - load_csv_to_bigquery
    - Table Operations:
        - create_table_if_not_exists
        - setup_feedback_table
        - setup_sentiment_table
        - setup_tables
        - insert_rows
    - Query Operations:
        - execute_query
        - get_data
        - get_feedback_data
        - get_sentiment_data
        - get_joined_feedback_sentiment_data
        - run_query
"""

# file: src/database/operations.py

from google.cloud import bigquery
from google.api_core import exceptions
from src.utils.config import config
from src.utils.logging import Logger
from src.database.connection import get_bigquery_client, get_storage_client

logger = Logger().logger

# Data Loading Operations

def get_job_config(num_rows=None):
    """
    Create a job configuration for loading CSV data into BigQuery.

    Args:
        num_rows (int, optional): Maximum number of bad records allowed. Defaults to None.

    Returns:
        google.cloud.bigquery.job.LoadJobConfig: Job configuration for data loading.
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
    Load CSV data from Google Cloud Storage into a BigQuery table.

    Args:
        bucket_name (str): Name of the GCS bucket containing the CSV file.
        blob_name (str): Name of the CSV file in the GCS bucket.
        table_name (str): Name of the BigQuery table to load data into.
        num_rows (int, optional): Maximum number of rows to load. Defaults to None.

    Raises:
        Exception: If there's an error during the loading process.
    """

    client = get_bigquery_client()
    try:
        table_id = f"{config.PROJECT_ID}.{config.DATASET_NAME}.{table_name}"
        uri = f"gs://{bucket_name}/{blob_name}"
        job_config = get_job_config(num_rows)

        load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
        load_job.result()

        destination_table = client.get_table(table_id)
        logger.info(f"Loaded {destination_table.num_rows} rows into {table_id}")
    except Exception as e:
        logger.error(f"Error in load_csv_to_bigquery: {str(e)}")
        raise

# Table Operations

def create_table_if_not_exists(table_id, schema):
    """
    Create a BigQuery table if it doesn't already exist.

    Args:
        table_id (str): Full ID of the BigQuery table.
        schema (list): List of SchemaField objects defining the table schema.

    Raises:
        Exception: If there's an error during table creation.
    """

    client = get_bigquery_client()
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

def setup_feedback_table():
    """
    Set up the feedback table in BigQuery.

    This function creates the feedback table if it doesn't exist.
    """

    table_id = f"{config.PROJECT_ID}.{config.DATASET_NAME}.{config.FEEDBACK_TABLE_NAME}"
    schema = [
        bigquery.SchemaField("Id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Review", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Label", "STRING", mode="NULLABLE"),
    ]
    create_table_if_not_exists(table_id, schema)

def setup_sentiment_table():
    """
    Set up the sentiment table in BigQuery.

    This function creates the sentiment table if it doesn't exist.
    """

    table_id = f"{config.PROJECT_ID}.{config.DATASET_NAME}.{config.SENTIMENT_TABLE_NAME}"
    schema = [
        bigquery.SchemaField("Id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Score", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("Magnitude", "FLOAT", mode="REQUIRED"),
    ]
    create_table_if_not_exists(table_id, schema)

def setup_tables():
    """
    Set up all required tables in BigQuery.

    This function sets up both the feedback and sentiment tables.

    Raises:
        Exception: If there's an error during table setup.
    """

    try:
        setup_feedback_table()
        setup_sentiment_table()
        logger.info("All tables have been set up successfully.")
    except Exception as e:
        logger.error(f"Error in setup_tables: {str(e)}")
        raise

def insert_rows(table_name, rows):
    """
    Insert rows into a BigQuery table.

    Args:
        table_name (str): Name of the BigQuery table to insert rows into.
        rows (list): List of dictionaries representing the rows to insert.

    Returns:
        bool: True if insertion was successful, False otherwise.
    """

    

    client = get_bigquery_client()
    table_id = f"{config.PROJECT_ID}.{config.DATASET_NAME}.{table_name}"
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        logger.error(f"Errors inserting rows: {errors}")
        return False
    else:
        logger.info(f"Inserted {len(rows)} rows into {table_id}")
        return True

# Query Operations

def execute_query(query):
    """
    Execute a BigQuery SQL query.

    Args:
        query (str): The SQL query to execute.

    Returns:
        list: A list of dictionaries representing the query results.

    Raises:
        Exception: If there's an error during query execution.
    """
    client = get_bigquery_client()
    try:
        query_job = client.query(query)
        results = query_job.result()
        return [dict(row) for row in results]
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        raise

def get_data(table_name, limit=None, where_clause=None):
    """
    Retrieve data from a specified BigQuery table.

    Args:
        table_name (str): Name of the table to query.
        limit (int, optional): Maximum number of rows to return. Defaults to None.
        where_clause (str, optional): WHERE clause for the query. Defaults to None.

    Returns:
        list: A list of dictionaries containing the query results.
    """
    table_id = f"`{config.PROJECT_ID}.{config.DATASET_NAME}.{table_name}`"
    query = f"SELECT * FROM {table_id}"
    
    if where_clause:
        query += f" WHERE {where_clause}"
    
    if limit:
        query += f" LIMIT {limit}"

    return execute_query(query)

def get_feedback_data(limit=None, where_clause=None):
    """
    Retrieve data from the feedback table.

    Args:
        limit (int, optional): Maximum number of rows to return. Defaults to None.
        where_clause (str, optional): WHERE clause for the query. Defaults to None.

    Returns:
        list: A list of dictionaries containing the feedback data.
    """
    return get_data(config.FEEDBACK_TABLE_NAME, limit, where_clause)

def get_sentiment_data(limit=None, where_clause=None):
    """
    Retrieve data from the sentiment table.

    Args:
        limit (int, optional): Maximum number of rows to return. Defaults to None.
        where_clause (str, optional): WHERE clause for the query. Defaults to None.

    Returns:
        list: A list of dictionaries containing the sentiment data.
    """
    return get_data(config.SENTIMENT_TABLE_NAME, limit, where_clause)

def get_joined_feedback_sentiment_data(limit=None, where_clause=None):
    """
    Retrieve joined data from both feedback and sentiment tables.

    Args:
        limit (int, optional): Maximum number of rows to return. Defaults to None.
        where_clause (str, optional): WHERE clause for the query. Defaults to None.

    Returns:
        list: A list of dictionaries containing the joined data.
    """
    feedback_table = f"`{config.PROJECT_ID}.{config.DATASET_NAME}.{config.FEEDBACK_TABLE_NAME}`"
    sentiment_table = f"`{config.PROJECT_ID}.{config.DATASET_NAME}.{config.SENTIMENT_TABLE_NAME}`"
    
    query = f"""
    SELECT f.*, s.Score, s.Magnitude
    FROM {feedback_table} f
    LEFT JOIN {sentiment_table} s ON f.Id = s.Id
    """
    
    if where_clause:
        query += f" WHERE {where_clause}"
    
    if limit:
        query += f" LIMIT {limit}"

    return execute_query(query)

def run_query(query):
    """
    Execute a full SQL query.

    Args:
        query (str): The full SQL query to execute.

    Returns:
        list: A list of dictionaries containing the query results.
    """
    return execute_query(query)

# Main execution block for testing and demonstration
if __name__ == "__main__":
    # Test data loading
    load_csv_to_bigquery(config.BUCKET_NAME, config.BLOB_NAME, config.FEEDBACK_TABLE_NAME, num_rows=10)

    # Test table setup
    setup_tables()

    # Test querying
    print("Fetching 5 rows from feedback table:")
    print(get_feedback_data(limit=5))
    
    print("\nFetching 5 rows from sentiment table:")
    print(get_sentiment_data(limit=5))
    
    print("\nFetching 5 rows of joined feedback and sentiment data:")
    print(get_joined_feedback_sentiment_data(limit=5))
    
    print("\nExecuting a full SQL query:")
    full_sql_query = f"""
    SELECT f.Id, f.Review, s.Score
    FROM `{config.PROJECT_ID}.{config.DATASET_NAME}.{config.FEEDBACK_TABLE_NAME}` f
    JOIN `{config.PROJECT_ID}.{config.DATASET_NAME}.{config.SENTIMENT_TABLE_NAME}` s
    ON f.Id = s.Id
    WHERE s.Score > 0.5
    ORDER BY s.Score DESC
    LIMIT 5
    """
    print(run_query(full_sql_query))

    # Test data insertion
    test_rows = [
        {"Id": "test1", "Review": "This is a test review", "Label": "positive"},
        {"Id": "test2", "Review": "Another test review", "Label": "negative"}
    ]
    insert_rows(config.FEEDBACK_TABLE_NAME, test_rows)
