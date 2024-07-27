# file: tests/test_sentiment_analysis.py
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import unittest
from unittest.mock import patch, MagicMock
from src.analysis.sentiment_analysis import evaluate_sentiment, perform_sentiment_analysis
from src.utils.config import config

class TestSentimentAnalysis(unittest.TestCase):

    @patch('src.analysis.sentiment_analysis.OpenAI')
    def test_evaluate_sentiment(self, mock_openai):
        # Mock the OpenAI client and its response
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices[0].message.content = "{'score': 0.8, 'magnitude': 0.9}"
        mock_openai.return_value = mock_client

        # Test the evaluate_sentiment function
        result = evaluate_sentiment("This is a great product!")
        self.assertEqual(result, {'score': 0.8, 'magnitude': 0.9})

        # Verify that the OpenAI API was called with the correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        self.assertEqual(call_args['model'], "gpt-3.5-turbo")
        self.assertIn("This is a great product!", call_args['messages'][1]['content'])

    @patch('src.analysis.sentiment_analysis.get_data')
    @patch('src.analysis.sentiment_analysis.insert_rows')
    @patch('src.analysis.sentiment_analysis.evaluate_sentiment')
    def test_perform_sentiment_analysis(self, mock_evaluate_sentiment, mock_insert_rows, mock_get_data):
        # Mock the database operations
        mock_get_data.return_value = [
            {'Id': '1', 'Review': 'Great product'},
            {'Id': '2', 'Review': 'Bad experience'}
        ]
        mock_insert_rows.return_value = True

        # Mock the sentiment evaluation
        mock_evaluate_sentiment.side_effect = [
            {'score': 0.8, 'magnitude': 0.9},
            {'score': -0.6, 'magnitude': 0.7}
        ]

        # Run the function
        perform_sentiment_analysis(limit=2)

        # Verify that get_data was called with the correct parameters
        mock_get_data.assert_called_once()
        args, kwargs = mock_get_data.call_args
        self.assertEqual(args[0], config.FEEDBACK_TABLE_NAME)
        self.assertEqual(kwargs['limit'], 2)
        self.assertIn("Id NOT IN", kwargs['where_clause'])

        # Verify that evaluate_sentiment was called for each review
        self.assertEqual(mock_evaluate_sentiment.call_count, 2)

        # Verify that insert_rows was called with the correct data
        mock_insert_rows.assert_called_once()
        args, kwargs = mock_insert_rows.call_args
        self.assertEqual(args[0], config.SENTIMENT_TABLE_NAME)
        self.assertEqual(len(args[1]), 2)
        self.assertEqual(args[1][0]['Id'], '1')
        self.assertEqual(args[1][0]['Score'], 0.8)
        self.assertEqual(args[1][1]['Id'], '2')
        self.assertEqual(args[1][1]['Score'], -0.6)

if __name__ == '__main__':
    unittest.main()
