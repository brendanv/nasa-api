import requests
from nasa.base import NasaApiObject
from nasa import api
from PIL import Image
from io import BytesIO

def assets(lat, lon, begin, end=None):
    payload = {'lat': lat, 'lon': lon, 'begin': begin, 'end': end}
    response = api.api_get(
        'https://api.data.gov/nasa/planetary/earth/assets',
        payload,
    )
    results = response['results']
    for result in results:
        result.update({'lat': lat, 'lon': lon})
    return [EarthAsset.from_response(r) for r in results]

def image(lat, lon, dim=None, date=None, cloud_score=None):
    payload = {
        'lat': lat, 'lon': lon, 'dim': dim, 'date': date,
        'cloud_score': cloud_score,
    }
    response = api.api_get(
        'https://api.data.gov/nasa/planetary/earth/imagery',
        payload,
    )
    return EarthImagery.from_response(response)

class EarthAsset(NasaApiObject):
    """Date and time assets from Nasa's Earth API"""
    class Meta(object):
        properties = ['id', 'date', 'lat', 'lon']
    def __init__(self, **kwargs):
        super(EarthAsset, self).__init__(**kwargs)
        self._image = None

    def __repr__(self):
        return '<NasaEarthAsset id="%s">' % self.id

    def get_asset_image(self, dim=None):
        # API expects only YYYY-MM-DD
        date = self.date[:10]
        return image(self.lat, self.lon, dim, date)


class EarthImagery(NasaApiObject):
    """NASA Earth Imagery API"""
    class Meta(object):
        properties = ['id', 'url', 'date', 'cloud_score', 'resource']

    def __init__(self, **kwargs):
        super(EarthImagery, self).__init__(**kwargs)
        self._image = None

    def __repr__(self):
        return '<NasaEarthImagery id="%s">' % self.id

    @property
    def image(self):
        if self._image is None:
            self._image = Image.open(BytesIO(requests.get(self.url).content))
        return self._image
