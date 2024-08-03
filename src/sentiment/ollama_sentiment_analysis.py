import ollama
from src.utils.config import config
from src.utils.logging import logger
from src.database import get_data, insert_rows


def evaluate_sentiment_ollama(review):
    """
    Evaluates the sentiment of a given review using the phi3:medium-128k model from Ollama.

    Args:
        review (str): The review text to analyze.

    Returns:
        dict: A dictionary containing 'score' and 'magnitude'.
    """
    prompt = f"Analyze the sentiment of the following review. Respond with a JSON object containing 'score' (a float between -1 and 1, where -1 is very negative and 1 is very positive) and 'magnitude' (a float representing the strength of the sentiment, where 0 is neutral and higher values indicate stronger sentiment):\n\n{review}"

    ollama_response = ollama.chat(model='phi3:medium-128k', messages=[
        {
            'role': 'system',
            'content': 'You are a sentiment analysis expert. Analyze the sentiment of the given text and provide a score and magnitude.',
        },
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    return eval(ollama_response['message']['content'])


def perform_sentiment_analysis_ollama(limit=None):
    """
    Performs sentiment analysis on user feedback data using the phi3:medium-128k model from Ollama.

    Args:
        limit (int): The number of rows to process for sentiment analysis. If None, all rows are processed.

    Raises:
        Exception: An error occurred when performing sentiment analysis.
    """
    try:
        # Get unprocessed reviews
        where_clause = f"Id NOT IN (SELECT Id FROM `{config.PROJECT_ID}.{config.DATASET_NAME}.{config.SENTIMENT_TABLE_NAME}`)"
        unprocessed_reviews = get_data(
            config.FEEDBACK_TABLE_NAME, limit=limit, where_clause=where_clause)

        results = []
        for review in unprocessed_reviews:
            sentiment = evaluate_sentiment_ollama(review['Review'])
            results.append({
                "Id": review['Id'],
                "Score": sentiment['score'],
                "Magnitude": sentiment['magnitude']
            })

        if results:
            success = insert_rows(config.SENTIMENT_TABLE_NAME, results)
            if not success:
                logger.error("Failed to insert sentiment results.")
        else:
            logger.info("No new rows to process for sentiment analysis.")

    except Exception as e:
        logger.error(f"Error in perform_sentiment_analysis_ollama: {str(e)}")
        raise
