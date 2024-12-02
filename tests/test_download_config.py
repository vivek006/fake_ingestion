import pytest
import requests
from unittest.mock import patch, Mock
from src.download_config import APIConfig, download_data

@pytest.fixture
def mock_api_response():
    """
    Provides a mock API response for testing.
    """
    return {
        "data": [
            {"name": "Alice", "email": "alice@example.com", "gender": "female"},
            {"name": "Bob", "email": "bob@example.com", "gender": "male"}
        ]
    }

def test_api_config_defaults():
    """
    Test the default values of the APIConfig class.
    """
    config = APIConfig()
    assert config.url == "https://fakerapi.it/api/v2/persons"
    assert config.gender == "both"
    assert config.quantity == 30000
    assert config.birthdate_start == "1900-01-01"

def test_api_config_custom_values():
    """
    Test creating an APIConfig object with custom values.
    """
    config = APIConfig(url="https://customapi.com", gender="male", quantity=100, birthdate_start="2000-01-01")
    assert config.url == "https://customapi.com"
    assert config.gender == "male"
    assert config.quantity == 100
    assert config.birthdate_start == "2000-01-01"

@patch("src.download_config.requests.get")
def test_download_data_success(mock_get, mock_api_response):
    """
    Test the download_data function for successful data retrieval.
    """
    # Mock the response object returned by requests.get
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_api_response

    config = APIConfig(quantity=2)  # Only request 2 records for testing
    data = download_data(config)

    # Verify the returned data matches the mocked response
    assert data == mock_api_response["data"]

    # Verify that requests.get was called with the correct parameters
    mock_get.assert_called_once_with(
        config.url,
        params={"_quantity": 2, "_gender": "both", "_birthday_start": "1900-01-01"}
    )

@patch("src.download_config.requests.get")
def test_download_data_retry_logic(mock_get):
    """
    Test the retry logic of the download_data function.
    """
    # Mock the response to fail the first two times, then succeed
    mock_get.side_effect = [
        requests.exceptions.RequestException("Network error"),
        requests.exceptions.RequestException("Network error"),
        Mock(status_code=200, json=lambda: {"data": [{"name": "Alice"}]})
    ]

    config = APIConfig(quantity=1)
    data = download_data(config)

    # Verify the returned data matches the successful response
    assert data == [{"name": "Alice"}]

    # Verify requests.get was called three times due to retries
    assert mock_get.call_count == 3

@patch("src.download_config.requests.get")
def test_download_data_http_error(mock_get):
    """
    Test the download_data function when an HTTP error occurs.
    """
    # Mock the response to return an HTTP error
    mock_get.return_value.status_code = 400
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("Bad Request")

    config = APIConfig()

    with pytest.raises(requests.exceptions.HTTPError, match="Bad Request"):
        download_data(config)

    # Verify requests.get was called the expected number of times due to retries
    assert mock_get.call_count == 5  # Adjust this number based on your retry logic
