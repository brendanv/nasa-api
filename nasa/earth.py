import requests
from nasa.base import NasaApiObject
from PIL import Image
from StringIO import StringIO

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
        return self._api.earth_imagery.query(self.lat, self.lon, dim, date)


class EarthImagery(object):
    """NASA Earth Imagery API"""

    def __init__(self, id='', url=None, date=None, cloud_score=None,
                 resource=None):
        super(EarthImagery, self).__init__()
        self.id = id
        self.url = url
        self.date = date
        self.cloud_score = cloud_score
        self.resource = resource
        self._image = None

    def __repr__(self):
        return '<NasaEarthImagery id="%s">' % self.id

    @classmethod
    def query(cls, lat, lon, dim=None, date=None, cloud_score=None):
        payload = {
            'lat': lat, 'lon': lon, 'dim': dim, 'date': date,
            'cloud_score': cloud_score,
        }
        filtered_payload = dict((k, v) for k, v in payload.iteritems() if v)
        response = cls.api._get(
            'https://api.data.gov/nasa/planetary/earth/imagery',
            payload,
        )
        return EarthImagery.from_response(response)

    @staticmethod
    def from_response(result):
        try:
            score = result['cloud_score']
        except KeyError:
            score=None
        return EarthImagery(
            result['id'], result['url'], result['date'],
            score, result['resource'],
        )

    @property
    def image(self):
        if self._image is None:
            self._image = Image.open(StringIO(requests.get(self.url).content))
        return self._image
