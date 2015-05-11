import requests
import time
from PIL import Image
from StringIO import StringIO

API_URL = 'https://api.data.gov/nasa/planetary/apod'


class Apod(object):
    """NASA's Astronomy Picture of the Day"""

    def __init__(self, url, title='', explanation='', concepts=[], raw=None):
        super(Apod, self).__init__()
        self.url = url
        self.title = title
        self.explanation = explanation
        self.concepts = concepts
        self._raw = raw
        self._image = None

    @classmethod
    def get(cls, url, payload):
        return Apod.from_response(cls.api._get(url, payload))

    @classmethod
    def current(cls, include_concepts=False):
        return cls.on_date(time.strftime("%Y-%m-%d"), include_concepts)

    @classmethod
    def on_date(cls, date, include_concepts=False):
        return cls.get(API_URL,
                       {'date': date, 'concept_tags': include_concepts})

    @classmethod
    def from_response(cls, content):
        try:
            concepts = content['concepts'].values()
        except KeyError:
            concepts = []
        return Apod(
            content['url'], content['title'], content['explanation'],
            concepts, content)

    @property
    def image(self):
        if self._image is None:
            self._image = Image.open(StringIO(requests.get(self.url).content))
        return self._image


