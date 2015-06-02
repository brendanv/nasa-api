from nasa import api
from nasa.base import NasaApiObject

''' Retrieves the most recent MAAS Report '''
def latest():
    response = api.external_api_get(
        'http://marsweather.ingenology.com/v1/latest/',
        {},
    )
    return MAASReport.from_response(response['report'])

''' Retrieves the set of MAAS Reports that match the filters
provided via keyword args. Most report fields can be used as
filters.
'''
def archived(**kwargs):
    return _maas_paginate(
        'http://marsweather.ingenology.com/v1/archive/',
        **kwargs
    )

def _maas_paginate(url, **kwargs):
    response = api.external_api_get(url, kwargs)
    response['results'] = [
        MAASReport.from_response(r) for r in response['results']
    ]
    next_url = response['next']
    if next_url is not None:
        response['next'] = lambda: _maas_paginate(next_url)
    prev_url = response['previous']
    if prev_url is not None:
        response['previous'] = lambda: _maas_paginate(prev_url)
    return response


class MAASReport(NasaApiObject):
    """Mars Atmospheric Aggregation System Report"""
    class Meta(object):
        properties = ['terrestrial_date', 'sol', 'ls', 'min_temp',
                      'min_temp_fahrenheit', 'max_temp', 'max_temp_fahrenheit',
                      'pressure', 'pressure_string', 'abs_humidity',
                      'wind_speed', 'wind_direction', 'atmo_opacity', 'season',
                      'sunrise', 'sunset']

    def __init__(self, **kwargs):
        super(MAASReport, self).__init__(**kwargs)
