# sentiment_analysis.py

import openai
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_sentiment(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are a sentiment analysis expert. Analyze the sentiment of the given text and respond with a single float value between -1 and 1, where -1 is extremely negative, 0 is neutral, and 1 is extremely positive."},
                {"role": "user", "content": f"Analyze the sentiment of this text: '{text}'"}
            ],
            max_tokens=10,
            n=1,
            temperature=0.5,
        )
        
        sentiment_score = float(response.choices[0].message['content'].strip())
        return max(-1, min(1, sentiment_score))  # Ensure the score is between -1 and 1
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return 0  # Return neutral sentiment in case of error