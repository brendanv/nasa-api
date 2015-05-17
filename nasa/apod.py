import requests
from PIL import Image
from nasa.base import NasaApiObject
from io import BytesIO

API_URL = 'https://api.data.gov/nasa/planetary/apod'


class Apod(NasaApiObject):
    """NASA's Astronomy Picture of the Day"""
    class Meta(object):
        properties = ['url', 'title', 'explanation', 'concepts']

    def __init__(self, api, **kwargs):
        super(Apod, self).__init__(api, **kwargs)
        self._image = None
        if self.concepts is not None:
            self.concepts = self.concepts.values()

    @property
    def image(self):
        if self._image is None:
            self._image = Image.open(BytesIO(requests.get(self.url).content))
        return self._image
