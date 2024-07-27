
# User Feedback Analysis System

This project collects and analyzes user feedback using Python, Google Cloud Platform (GCP), BigQuery, and sentiment analysis.

## Table of Contents
- [User Feedback Analysis System](#user-feedback-analysis-system)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
  - [License](#license)

## Project Overview

This system is designed to collect user feedback from a CSV file, store it in Google BigQuery, and perform sentiment analysis using the ChatGPT API. It demonstrates skills in data handling, cloud storage, and natural language processing.

## Features

- Load user feedback data from CSV into Google BigQuery
- Perform sentiment analysis on feedback text using ChatGPT API
- Store analyzed data back in BigQuery
- Scalable design for handling large datasets
- Modular architecture with separate modules for data, database, and utility operations

## Requirements

- Python 3.7+
- Google Cloud Platform account with BigQuery and Cloud Storage enabled
- OpenAI API key

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/user-feedback-analysis.git
   cd user-feedback-analysis
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up Google Cloud credentials:
   - Create a service account and download the JSON key
   - Set the environment variable:
     ```
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
     ```

4. Set up OpenAI API key:
   ```
   export OPENAI_API_KEY="your-api-key"
   ```

5. Configure the project:
   - Update the `config.py` file in the `src/utils` directory with your project-specific settings

## Usage

1. Load data into BigQuery:
   ```python
   from src.data import load_csv_to_bigquery
   
   load_csv_to_bigquery()
   ```

2. Set up BigQuery tables:
   ```python
   from src.database import setup_tables
   
   setup_tables()
   ```

3. Perform sentiment analysis:
   ```python
   from src.analysis import analyze_sentiment
   
   analyze_sentiment()
   ```

## Project Structure

```
user_feedback_analysis/
│
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   └── collection.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── data_loading.py
│   │   └── data_operations.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── sentiment_analysis.py
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── logging.py
├── tests/
│   └── ...
├── requirements.txt
└── README.md
```

- `src/data/`: Contains modules for data collection and processing
- `src/database/`: Contains modules for database connection and operations
- `src/analysis/`: Contains modules for sentiment analysis
- `src/utils/`: Contains utility modules for configuration and logging
- `tests/`: Contains test scripts for various modules

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
