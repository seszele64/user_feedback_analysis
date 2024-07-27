from google.cloud import language_v1, bigquery
from src.utils.config import config
from src.utils.logging import logger

def perform_sentiment_analysis(limit=None):
    """
    Performs sentiment analysis on user feedback data.

    Args:
        limit (int): The number of rows to process for sentiment
            analysis. If None, all rows are processed.
    
    Raises:
        Exception: An error occurred when performing sentiment analysis.
    """

    try:
        client = bigquery.Client(project=config.PROJECT_ID)
        language_client = language_v1.LanguageServiceClient()

        feedback_table_id = f"{config.PROJECT_ID}.{config.DATASET_NAME}.{config.FEEDBACK_TABLE_NAME}"
        sentiment_table_id = f"{config.PROJECT_ID}.{config.DATASET_NAME}.{config.SENTIMENT_TABLE_NAME}"

        query = f"""
        SELECT Id, Review
        FROM `{feedback_table_id}`
        WHERE Id NOT IN (SELECT Id FROM `{sentiment_table_id}`)
        """
        if limit:
            query += f" LIMIT {limit}"

        query_job = client.query(query)
        rows = list(query_job.result())

        results = []
        for row in rows:
            document = language_v1.Document(content=row['Review'], type_=language_v1.Document.Type.PLAIN_TEXT)
            sentiment = language_client.analyze_sentiment(request={'document': document}).document_sentiment
            results.append({"Id": row['Id'], "Score": sentiment.score, "Magnitude": sentiment.magnitude})

        if results:
            errors = client.insert_rows_json(sentiment_table_id, results)
            if errors:
                logger.error(f"Errors inserting rows: {errors}")
            else:
                logger.info(f"Inserted {len(results)} rows into {sentiment_table_id}")
        else:
            logger.info("No new rows to process for sentiment analysis.")

    except Exception as e:
        logger.error(f"Error in perform_sentiment_analysis: {str(e)}")
        raise
