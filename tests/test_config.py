# file: tests/test_config.py

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from src.utils.config import Config

@pytest.fixture
def mock_env(monkeypatch):
    """Fixture to set up mock environment variables"""
    env_vars = {
        'SERVICE_ACCOUNT_FILE': '/path/to/service_account.json',
        'PROJECT_ID': 'test-project',
        'BUCKET_NAME': 'test-bucket',
        'BLOB_NAME': 'test.csv',
        'DATASET_NAME': 'test_dataset',
        'FEEDBACK_TABLE_NAME': 'test_feedback',
        'SENTIMENT_TABLE_NAME': 'test_sentiment',
        'TEMP_TABLE_NAME': 'test_temp',
        'DEFAULT_ROW_LIMIT': '200',
        'SENTIMENT_BATCH_SIZE': '2000'
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)

def test_config_initialization(mock_env):
    """Test that Config initializes correctly with environment variables"""
    config = Config(load_env=False)
    
    assert config.SERVICE_ACCOUNT_FILE == '/path/to/service_account.json'
    assert config.PROJECT_ID == 'test-project'
    assert config.BUCKET_NAME == 'test-bucket'
    assert config.BLOB_NAME == 'test.csv'
    assert config.DATASET_NAME == 'test_dataset'
    assert config.FEEDBACK_TABLE_NAME == 'test_feedback'
    assert config.SENTIMENT_TABLE_NAME == 'test_sentiment'
    assert config.TEMP_TABLE_NAME == 'test_temp'
    assert config.DEFAULT_ROW_LIMIT == 200
    assert config.SENTIMENT_BATCH_SIZE == 2000
    assert config.GCS_CSV_PATH == 'gs://test-bucket/test.csv'

def test_config_default_values(monkeypatch):
    """Test that Config uses default values when environment variables are not set"""
    for var in ['DEFAULT_ROW_LIMIT', 'SENTIMENT_BATCH_SIZE']:
        monkeypatch.delenv(var, raising=False)
    
    config = Config(load_env=False)
    
    assert config.DEFAULT_ROW_LIMIT == 100
    assert config.SENTIMENT_BATCH_SIZE == 1000

def test_config_schemas():
    """Test that Config has correct schema definitions"""
    config = Config(load_env=False)
    
    assert config.FEEDBACK_SCHEMA == [
        {"name": "Id", "type": "STRING", "mode": "REQUIRED"},
        {"name": "Review", "type": "STRING", "mode": "REQUIRED"},
        {"name": "Label", "type": "STRING", "mode": "NULLABLE"},
    ]
    
    assert config.SENTIMENT_SCHEMA == [
        {"name": "Id", "type": "STRING", "mode": "REQUIRED"},
        {"name": "Score", "type": "FLOAT", "mode": "REQUIRED"},
        {"name": "Magnitude", "type": "FLOAT", "mode": "REQUIRED"},
    ]

def test_config_gcs_csv_path(monkeypatch):
    """Test that GCS_CSV_PATH is correctly derived"""
    monkeypatch.setenv('BUCKET_NAME', 'test-bucket')
    monkeypatch.setenv('BLOB_NAME', 'test.csv')
    
    config = Config(load_env=False)
    assert config.GCS_CSV_PATH == 'gs://test-bucket/test.csv'

def test_config_missing_env_vars(monkeypatch):
    """Test that Config handles missing environment variables gracefully"""
    for var in ['SERVICE_ACCOUNT_FILE', 'PROJECT_ID', 'BUCKET_NAME', 'BLOB_NAME', 
                'DATASET_NAME', 'FEEDBACK_TABLE_NAME', 'SENTIMENT_TABLE_NAME', 'TEMP_TABLE_NAME']:
        monkeypatch.delenv(var, raising=False)
    
    config = Config(load_env=False)
    
    assert config.SERVICE_ACCOUNT_FILE is None
    assert config.PROJECT_ID is None
    assert config.BUCKET_NAME is None
    assert config.BLOB_NAME is None
    assert config.DATASET_NAME is None
    assert config.FEEDBACK_TABLE_NAME is None
    assert config.SENTIMENT_TABLE_NAME is None
    assert config.TEMP_TABLE_NAME is None
    assert config.GCS_CSV_PATH is None