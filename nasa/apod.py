import requests
from nasa import api, validations
from nasa.base import NasaApiObject
from PIL import Image
from io import BytesIO

''' Retrieves NASA Astronomy Picture of the Day

Query Parameters:
date            YYYY-MM-DD  The date of the APOD image to retrieve
concept_tags    bool        Return an ordered dictionary of concepts
                            from the APOD explanation
'''
def apod(date=None, concept_tags=None):
    payload = {
        'date': validations.optional_date(date),
        'concept_tags': concept_tags,
    }
    return Apod.from_response(api.api_get(
        'https://api.nasa.gov/planetary/apod',
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
