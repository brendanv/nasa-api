import requests
from nasa.base import NasaApiObject
from PIL import Image
from io import BytesIO

class EarthAsset(NasaApiObject):
    """Date and time assets from Nasa's Earth API"""
    class Meta(object):
        properties = ['id', 'date', 'lat', 'lon']
    def __init__(self, api, **kwargs):
        super(EarthAsset, self).__init__(api, **kwargs)
        self._image = None

    def __repr__(self):
        return '<NasaEarthAsset id="%s">' % self.id

    def get_asset_image(self, dim=None):
        # API expects only YYYY-MM-DD
        date = self.date[:10]
        return self._api.get_earth_image(self.lat, self.lon, dim, date)


class EarthImagery(NasaApiObject):
    """NASA Earth Imagery API"""
    class Meta(object):
        properties = ['id', 'url', 'date', 'cloud_score', 'resource']

    def __init__(self, api, **kwargs):
        super(EarthImagery, self).__init__(api, **kwargs)
        self._image = None

    def __repr__(self):
        return '<NasaEarthImagery id="%s">' % self.id

    @property
    def image(self):
        if self._image is None:
            self._image = Image.open(BytesIO(requests.get(self.url).content))
        return self._image
