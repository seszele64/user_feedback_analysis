# file: load_first_10_rows.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from src.database.data_loading import load_csv_to_bigquery
from src.utils.config import config

def main():
    try:
        load_csv_to_bigquery(config.BUCKET_NAME, config.BLOB_NAME, config.FEEDBACK_TABLE_NAME, num_rows=10)
        print("Successfully loaded first 10 rows from GCS to BigQuery.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()