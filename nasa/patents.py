API_URL = 'https://api.data.gov/nasa/patents/content'
DEFAULT_LIMIT = 10

class Patents(object):
    """NASA's Patent Portfolio"""

    def __init__(self, count=0, patents=[], raw=None):
        super(Patents, self).__init__()
        self.count = count
        self.patents = patents
        self._raw = raw

    @classmethod
    def get(cls, url, payload):
        return Patents.from_response(cls.api._get(url, payload))

    @classmethod
    def query(cls, query, include_concepts=False, limit=DEFAULT_LIMIT):
        payload = {
            'query': query,
            'concept_tags': include_concepts,
            'limit': limit,
            }
        return cls.get(API_URL, payload)

    @classmethod
    def from_response(cls, content):
        return Patents(content['count'], content['results'])
