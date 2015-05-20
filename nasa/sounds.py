from nasa.base import NasaApiObject
from nasa import api

def sounds(query, limit=10):
    payload = {'q': query, 'limit': limit}
    response = api.api_get(
        'https://api.data.gov/nasa/planetary/sounds',
        payload,
    )
    return [Sound.from_response(r) for r in response['results']]


class Sound(NasaApiObject):
    """NASA sound data (BETA)"""
    class Meta(object):
        properties = ['title', 'id', 'description', 'download_url',
                      'duration', 'last_modified', 'license', 'stream_url',
                      'tag_list']

    def __ini__(self, **kwargs):
        super(Sound, self).__init__(**kwargs)

    def __repr__(self):
        return '<NasaSound id="%s">' % self.id
