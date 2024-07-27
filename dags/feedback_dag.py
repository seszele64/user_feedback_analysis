from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add the path to your project directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your functions from data_collection.py

from src.data.collection import create_table_if_not_exists, perform_sentiment_analysis

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 21),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'user_feedback_analysis',
    default_args=default_args,
    description='A DAG to analyze user feedback daily',
    schedule_interval='@daily',  # Run daily
)

def run_sentiment_analysis(**kwargs):
    """
    Ensures the BigQuery table exists and performs sentiment analysis on a fixed number of rows.

    Args:
        **kwargs: Additional keyword arguments passed by Airflow.
    """
    # Ensure the table exists
    create_table_if_not_exists()
    
    # Perform sentiment analysis on a fixed number of rows (e.g., 100)
    perform_sentiment_analysis(limit=100)

analyze_feedback = PythonOperator(
    task_id='analyze_feedback',
    python_callable=run_sentiment_analysis,
    dag=dag,
)

analyze_feedback