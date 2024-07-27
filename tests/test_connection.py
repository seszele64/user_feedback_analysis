# test_connection.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.database.connection import get_bigquery_client, get_storage_client
from src.utils.config import config

import pytest
from unittest.mock import patch, MagicMock
from google.cloud import bigquery, storage

@patch('src.database.connection.config', new_callable=MagicMock)
def test_get_bigquery_client(mock_config):
    mock_config.PROJECT_ID = "dummy-project-id"
    mock_config.SERVICE_ACCOUNT_FILE = "path/to/service/account/file.json"
    
    with patch('google.oauth2.service_account.Credentials.from_service_account_file') as mock_credentials, \
         patch('google.cloud.bigquery.Client') as MockClient:
        
        credentials_instance = mock_credentials.return_value
        mock_client_instance = MockClient.return_value
        
        client = get_bigquery_client()
        assert client == mock_client_instance
        mock_credentials.assert_called_once_with(mock_config.SERVICE_ACCOUNT_FILE)
        MockClient.assert_called_once_with(credentials=credentials_instance, project=mock_config.PROJECT_ID)

@patch('src.database.connection.config', new_callable=MagicMock)
def test_get_storage_client(mock_config):
    mock_config.PROJECT_ID = "dummy-project-id"
    mock_config.SERVICE_ACCOUNT_FILE = "path/to/service/account/file.json"
    
    with patch('google.oauth2.service_account.Credentials.from_service_account_file') as mock_credentials, \
         patch('google.cloud.storage.Client') as MockStorageClient:
        
        credentials_instance = mock_credentials.return_value
        mock_client_instance = MockStorageClient.return_value
        
        client = get_storage_client()
        assert client == mock_client_instance
        mock_credentials.assert_called_once_with(mock_config.SERVICE_ACCOUNT_FILE)
        MockStorageClient.assert_called_once_with(credentials=credentials_instance, project=mock_config.PROJECT_ID)

