import requests
from PIL import Image
from nasa.base import NasaApiObject
from nasa import api
from io import BytesIO

API_URL = 'https://api.data.gov/nasa/planetary/apod'

def apod(date=None, concept_tags=None):
    payload = {'date': date, 'concept_tags': concept_tags}
    return Apod.from_response(api.api_get(
        'https://api.data.gov/nasa/planetary/apod',
        payload,
    ))

class Apod(NasaApiObject):
    """NASA's Astronomy Picture of the Day"""
    class Meta(object):
        properties = ['url', 'title', 'explanation', 'concepts']

    def __init__(self, **kwargs):
        super(Apod, self).__init__(**kwargs)
        self._image = None
        if self.concepts is not None:
            self.concepts = self.concepts.values()

    @property
    def image(self):
        if self._image is None:
            self._image = Image.open(BytesIO(requests.get(self.url).content))
        return self._image
