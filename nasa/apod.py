import requests
from PIL import Image
from StringIO import StringIO
from nasa.base import NasaApiObject

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
            self._image = Image.open(StringIO(requests.get(self.url).content))
        return self._image
