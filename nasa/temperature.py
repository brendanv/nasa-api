API_BASE = 'https://api.data.gov/nasa/planetary/earth/temperature/'

class Temperature(object):
    """NASA temperature anomalies"""

    def __init__(self, year='', anomaly=None):
        super(Temperature, self).__init__()
        self.year = year
        self.anomaly = anomaly

    @classmethod
    def get(cls, api_type, payload):
        url = API_BASE + api_type
        response = cls.api._get(url, payload)
        return [Temperature.from_response(r) for r in response['results']]

    @classmethod
    def for_address(cls, address, begin=None, end=None):
        payload = {'text': address}
        if begin is not None:
            payload['begin'] = begin
        if end is not None:
            payload['end'] = end
        return cls.get('address', payload)

    @classmethod
    def for_coords(cls, lat, lon, begin=None, end=None):
        payload = {'lat': lat, 'lon': lon}
        if begin is not None:
            payload['begin'] = begin
        if end is not None:
            payload['end'] = end
        return cls.get('coords', payload)

    @classmethod
    def from_response(cls, content):
        return Temperature(content['year'], content['anomaly'])
