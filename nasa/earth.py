import requests
from PIL import Image
from StringIO import StringIO

class EarthAsset(object):
    """docstring for EarthAsset"""
    def __init__(self, id, date, lat, lon):
        super(EarthAsset, self).__init__()
        self.id = id
        self.date = date
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return '<NasaEarthAsset id="%s">' % self.id

    @classmethod
    def query(cls, lat, lon, begin, end=None):
        payload = {'lat': lat, 'lon': lon, 'begin': begin, 'end': end}
        filtered_payload = dict((k, v) for k, v in payload.iteritems() if v)
        response = cls.api._get(
            'https://api.data.gov/nasa/planetary/earth/assets',
            payload,
        )
        return [
            EarthAsset(r['id'], r['date'], lat, lon)
            for r in response['results']
        ]

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
