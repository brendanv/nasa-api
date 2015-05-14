API_BASE = 'https://api.data.gov/nasa/planetary/earth/temperature/'

class Temperatures(object):
    """NASA temperature anomalies"""

    def __init__(self, count=0, anomalies=[], raw=None):
        super(Temperatures, self).__init__()
        self.count = count
        self.anomalies = anomalies
        self._raw = raw

    @classmethod
    def get(cls, api_type, payload):
        url = API_BASE + api_type
        return Temperatures.from_response(cls.api._get(url, payload))

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
        return Temperatures(content['count'], content['results'], content)
