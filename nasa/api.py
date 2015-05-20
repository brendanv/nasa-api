import os
import requests

class NasaApiException(Exception):
    """Raised for any exception caused by a call to the Nasa API"""

class RateLimitException(NasaApiException):
    """Raised when you have exceeded your rate limit"""

def api_get(url, payload):
    payload = dict((k, v) for k, v in payload.items() if v)
    payload['api_key'] = api_key()
    response = requests.get(url, params=payload)
    if response.status_code == 429:
        raise RateLimitException('You have exceeded your rate limit')
    response.raise_for_status()
    body = response.json()
    if 'error' in body:
        raise NasaApiException(body['error'])

    ratelimit_limit = int(response.headers['x-ratelimit-limit'])
    ratelimit_remaining = int(response.headers['x-ratelimit-remaining'])

    return body

def api_key():
    return os.environ["NASA_API_KEY"]
