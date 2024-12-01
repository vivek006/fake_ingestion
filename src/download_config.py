import yaml
import requests
import backoff

API_URL = "https://fakerapi.it/api/v2/persons"
class APIConfig:
    """
    Configuration object for data download.
    """
    def __init__(self, url=API_URL, gender="both", quantity=30000, birthdate_start="1900-01-01"):
        self.url = url
        self.gender = gender
        self.quantity = quantity
        self.birthdate_start = birthdate_start


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=5
)
def download_data(config: APIConfig):
    """
    Downloads data from a third-party system with retry logic and error handling.

    Args:
        config (APIConfig): Configuration object containing download details.

    Returns:
        list: A list of dictionaries representing the downloaded data.
    """
    params = {
        "_quantity": config.quantity,
        "_gender": config.gender,
        "_birthday_start": config.birthdate_start
    }
    response = requests.get(config.url, params=params)
    response.raise_for_status()
    return response.json()["data"]