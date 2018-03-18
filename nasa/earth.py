import requests
from nasa import api, validations
from nasa.base import NasaApiObject
from PIL import Image
from io import BytesIO


'''Retrieves the date-times and asset names for available imagery for a
supplied location

Query Parameters:
lat   float       Latitude
lon   float       Longitude
begin YYYY-MM-DD  Beginning of date range
end   YYYY-MM-DD  End of date range
'''
def assets(lat, lon, begin, end=None):
    payload = {
        'lat': validations.nasa_float(lat),
        'lon': validations.nasa_float(lon),
        'begin': validations.nasa_date(begin),
        'end': validations.optional_date(end),
    }
    response = api.api_get(
        'https://api.nasa.gov/planetary/earth/assets',
        payload,
    )
    results = response['results']
    for result in results:
        result.update({'lat': lat, 'lon': lon})
    return [EarthAsset.from_response(r) for r in results]

''' Retrieves the Landsat 8 image for the supplied location and date

Query Parameters:
lat         float        Latitude
lon         float        Longitude
dim         float        Width and height of image in degrees
date        YYYY-MM-DD   Date of image; if not supplied,
                         then the most recent image (i.e., closest to today)
                         is returned
cloud_score bool         False calculate the percentage of the image covered
                         by clouds
'''
def image(lat, lon, dim=None, date=None, cloud_score=None):
    payload = {
        'lat': validations.nasa_float(lat),
        'lon': validations.nasa_float(lon),
        'dim': validations.optional_float(dim),
        'date': validations.optional_date(date),
        'cloud_score': cloud_score,
    }
    response = api.api_get(
        'https://api.nasa.gov/planetary/earth/imagery/',
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

    def get_asset_image(self, dim=None, cloud_score=None):
        # API expects only YYYY-MM-DD
        date = self.date[:10]
        return image(self.lat, self.lon, dim, date, cloud_score)


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
