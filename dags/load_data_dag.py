from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'gcs_to_bigquery_append',
    default_args=default_args,
    description='A DAG to load data from GCS to BigQuery and append',
    schedule_interval=timedelta(days=1),
)

# Task to load data from GCS to BigQuery
load_gcs_to_bq = GCSToBigQueryOperator(
    task_id='load_gcs_to_bq',
    bucket='your_gcs_bucket',
    source_objects=['path/to/your/file*.csv'],
    destination_project_dataset_table='your_project.your_dataset.your_temp_table',
    schema_fields=[
        {'name': 'column1', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'column2', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        # Add more fields as per your schema
    ],
    write_disposition='WRITE_TRUNCATE',
    source_format='CSV',
    skip_leading_rows=1,
    dag=dag,
)

# Task to append data from temporary table to main table
append_data = BigQueryInsertJobOperator(
    task_id='append_data_to_main_table',
    configuration={
        'query': {
            'query': """
            INSERT INTO `your_project.your_dataset.your_main_table`
            SELECT * FROM `your_project.your_dataset.your_temp_table`
            """,
            'useLegacySql': False,
        }
    },
    dag=dag,
)

load_gcs_to_bq >> append_data
