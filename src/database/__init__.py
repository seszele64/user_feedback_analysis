# file: src/database/__init__.py

from .connection import get_bigquery_client, get_storage_client, test_connections
from .operations import (
    # Data Loading Operations
    load_csv_to_bigquery,
    
    # Table Operations
    setup_tables,
    setup_feedback_table,
    setup_sentiment_table,
    insert_rows,
    
    # Query Operations
    get_data,
    get_feedback_data,
    get_sentiment_data,
    get_joined_feedback_sentiment_data,
    run_query
)

__all__ = [
    # Connection functions
    'get_bigquery_client',
    'get_storage_client',
    'test_connections',
    
    # Data Loading Operations
    'load_csv_to_bigquery',
    
    # Table Operations
    'setup_tables',
    'setup_feedback_table',
    'setup_sentiment_table',
    'insert_rows',
    
    # Query Operations
    'get_data',
    'get_feedback_data',
    'get_sentiment_data',
    'get_joined_feedback_sentiment_data',
    'run_query'
]