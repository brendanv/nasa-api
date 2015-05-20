from nasa import api, validations
from nasa.base import NasaApiObject


''' Retrieves local temperature anomalies for an address

Query Parameters
text    string  Address string
begin   int     Beginning year for date range, inclusive
end     int     End year for date range, inclusive
'''
def address(address, begin=None, end=None):
    payload = {
        'text': address,
        'begin': validations.optional_int(begin),
        'end': validations.optional_int(end),
    }
    response = api.api_get(
        'https://api.data.gov/nasa/planetary/earth/temperature/address',
        payload,
    )
    return [Temperature.from_response(r) for r in response['results']]

''' Retrieves local temperature anomalies for coordinates

Query Parameters:
lat     float   Latitude
lon     float   Longitude
begin   int     Beginning year for date range, inclusive
end     int     End year for date range, inclusive
'''
def coordinates(lat, lon, begin=None, end=None):
    payload = {
        'lat': validations.nasa_float(lat),
        'lon': validations.nasa_float(lon),
        'begin': validations.optional_int(begin),
        'end': validations.optional_int(end),
    }
    response = api.api_get(
        'https://api.data.gov/nasa/planetary/earth/temperature/coords',
        payload,
    )
    return [Temperature.from_response(r) for r in response['results']]

class Temperature(NasaApiObject):
    """NASA temperature anomalies"""
    class Meta(object):
        properties = ['year', 'anomaly']

    def __init__(self, **kwargs):
        super(Temperature, self).__init__(**kwargs)
