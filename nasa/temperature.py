from nasa import api
from nasa.base import NasaApiObject

def address(address, begin=None, end=None):
    payload = {'text': address, 'begin': begin, 'end': end}
    response = api.api_get(
        'https://api.data.gov/nasa/planetary/earth/temperature/address',
        payload,
    )
    return [Temperature.from_response(r) for r in response['results']]

def coordinates(lat, lon, begin=None, end=None):
    payload = {'lat': lat, 'lon': lon, 'begin': begin, 'end': end}
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
