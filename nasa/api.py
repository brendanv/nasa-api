from __future__ import division
import logging
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
    percent = ratelimit_remaining / ratelimit_limit
    if percent < 0.1:
        api_logger().warn(
            "Only {:3.1f}% of your rate limit is remaining!".format(percent * 100)
        )

    return body

''' For API calls that don't strictly fall into the api.nasa.gov set and
therefore don't require an API key, and don't enforce the same rate limits.
'''
def external_api_get(url, payload):
    payload = dict((k, v) for k, v in payload.items() if v)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    body = response.json()
    return body

def api_key():
    return os.environ["NASA_API_KEY"]

def api_logger():
    return logging.getLogger('nasa_logger')
