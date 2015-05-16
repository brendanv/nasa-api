import requests

from nasa.apod import Apod
from nasa.patents import Patents
from nasa.temperature import Temperature
from nasa.sounds import Sound
from nasa.earth import EarthImagery, EarthAsset

DEMO_KEY = 'DEMO_KEY'

class NasaApiException(Exception):
    """Raised for any exception caused by a call to the Nasa API"""

class RateLimitException(NasaApiException):
    """Raised when you have exceeded your rate limit"""

class Api(object):
    """Build an API wrapper for the NASA data API with the given API key"""
    def __init__(self, api_key=DEMO_KEY):
        super(Api, self).__init__()
        self.api_key = api_key
        if api_key is DEMO_KEY:
            print 'Using default API key. This is not recommended.'
        self.ratelimit_limit = None
        self.ratelimit_remaining = None

    def __repr__(self):
        return '<NasaAPI api_key="%s">' % self.api_key

    def get_apod(self, date=None, include_concepts=None):
        payload = {'date': date, 'concept_tags': include_concepts}
        return Apod.from_response(self, self._filter_payload_and_get(
            'https://api.data.gov/nasa/planetary/apod',
            payload,
        ))

    @property
    def patents(self):
        return type('Patents', (Patents,), dict(api=self))

    @property
    def temperatures(self):
        return type('Temperature', (Temperature,), dict(api=self))

    @property
    def sounds(self):
        return type('Sound', (Sound,), dict(api=self))

    @property
    def earth_imagery(self):
        return type('EarthImagery', (EarthImagery,), dict(api=self))

    @property
    def earth_assets(self):
        return type('EarthAsset', (EarthAsset,), dict(api=self))

    @property
    def test(self):
        resp = self._get(
            'https://api.data.gov/nasa/planetary/apod',
            {'date': '2015-03-04'}
        )
        return ApodNew.from_response(self, resp)

    def _filter_payload_and_get(self, url, payload):
        filtered_payload = dict((k, v) for k, v in payload.iteritems() if v)
        return self._get(url, filtered_payload)

    def _get(self, url, payload):
        payload['api_key'] = self.api_key
        response = requests.get(url, params=payload)
        self.ratelimit_limit = int(response.headers['x-ratelimit-limit'])
        self.ratelimit_remaining = int(response.headers['x-ratelimit-remaining'])
        if response.status_code == 429:
            raise RateLimitException('You have exceeded your rate limit')
        response.raise_for_status()
        body = response.json()
        if 'error' in body:
            raise NasaApiException(body['error'])
        return body
