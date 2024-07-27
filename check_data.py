import os
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to query BigQuery table
def query_bigquery_table():
    # Set up credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('SERVICE_ACCOUNT_FILE')

    # Create a client
    client = bigquery.Client()

    # Get table details from environment variables
    project_id = os.getenv('PROJECT_ID')
    dataset_id = os.getenv('DATASET_NAME')
    table_id = os.getenv('FEEDBACK_TABLE_NAME')

    # Construct the query
    query = f"""
    SELECT *
    FROM `{project_id}.{dataset_id}.{table_id}`
    LIMIT 10
    """

    print(f"Executing query: {query}")

    # Run the query
    try:
        query_job = client.query(query)
        
        # Fetch and print results
        results = query_job.result()
        for row in results:
            print(row)
    except Exception as e:
        print(f"An error occurred while querying BigQuery: {e}")

if __name__ == "__main__":
    query_bigquery_table()