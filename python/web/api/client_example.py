import time
import random

import requests
from requests.exceptions import HTTPError
from http import HTTPStatus


class ClientConfig(BaseModel):
    url: str
    bearer: str
    max_retries: int = 5


class Client:

    retry_codes = [
        HTTPStatus.TOO_MANY_REQUESTS,
        HTTPStatus.INTERNAL_SERVER_ERROR,
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.GATEWAY_TIMEOUT,
    ]

    def __init__(self, config: ClientConfig):
        self._config = config

    @property
    def url(self):
        return self._config.url

    def get(self, url):

        retry_delay = 1  # Initial delay in seconds

        for attempt in range(self._config.max_retries):
            try:
                response = requests.get(url=url, headers={
                    'Authorization': f'Bearer {self._config.bearer}'
                })
                response.raise_for_status()
                return response

            except HTTPError as exc:
                code = exc.response.status_code

                if code in self.retry_codes:
                    print(f'Retrying in {retry_delay} second/s. {attempt+1} of {self._config.max_retries}.')
                    # Retry after n seconds
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Double the delay for the next attempt
                    retry_delay += random.uniform(0, 1)  # Add jitter
                    continue

                raise

        raise RuntimeError("Maximum retry attempts reached.")

    def put(self, url, kwargs**):

        retry_delay = 1  # Initial delay in seconds

        for attempt in range(self._config.max_retries):
            try:
                response = requests.put(url=url, headers={
                    'Authorization': f'Bearer {self._config.bearer}'
                })
                response.raise_for_status()
                return response

            except HTTPError as exc:
                code = exc.response.status_code

                if code in self.retry_codes:
                    print(f'Retrying in {retry_delay} second/s. {attempt+1} of {self._config.max_retries}.')
                    # Retry after n seconds
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Double the delay for the next attempt
                    retry_delay += random.uniform(0, 1)  # Add jitter
                    continue

                raise

        raise RuntimeError("Maximum retry attempts reached.")
