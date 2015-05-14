API_BASE = 'https://api.data.gov/nasa/planetary/sounds'

class Sound(object):
    """NASA sound data (BETA)"""

    def __init__(self, title='', id='', description='', download_url='',
                 duration='', last_modified='', license='', stream_url='',
                 tag_list=[]):
        super(Sound, self).__init__()
        self.title = title
        self.id = id
        self.description = description
        self.download_url = download_url
        self.duration = duration
        self.last_modified = last_modified
        self.license = license
        self.stream_url = stream_url
        self.tag_list = tag_list

    def __repr__(self):
        return '<NasaSound id="%s">' % self.id

    @classmethod
    def query(cls, query, limit=10):
        payload = {'q': query, 'limit': limit}
        response = cls.api._get(
            'https://api.data.gov/nasa/planetary/sounds',
            payload,
        )
        return [Sound.from_response(result) for result in response['results']]

    @staticmethod
    def from_response(result):
        return Sound(
            result['title'], result['id'], result['description'],
            result['download_url'], result['duration'],
            result['last_modified'], result['license'], result['stream_url'],
            result['tag_list'],
        )
