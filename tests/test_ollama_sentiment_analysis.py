import unittest
from src.sentiment.ollama_sentiment_analysis import evaluate_sentiment_ollama


class TestOllamaSentimentAnalysis(unittest.TestCase):

    def test_evaluate_sentiment_ollama(self):
        # Sample text to check its sentiment
        sample_text = "I love this product! It has exceeded all my expectations."
        sample_text = "I hate this product! It is a waste of money."

        # Call the function to evaluate sentiment
        sentiment = evaluate_sentiment_ollama(sample_text)
        print("Sentiment Analysis Result (Ollama):", sentiment)

        # Check if the response contains 'score' and 'magnitude'
        self.assertIn('score', sentiment)
        self.assertIn('magnitude', sentiment)

        # Check if the score is within the expected range
        self.assertGreaterEqual(sentiment['score'], -1)
        self.assertLessEqual(sentiment['score'], 1)

        # Check if the magnitude is non-negative
        self.assertGreaterEqual(sentiment['magnitude'], 0)


if __name__ == '__main__':
    unittest.main()
