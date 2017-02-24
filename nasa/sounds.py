from nasa import api, validations
from nasa.base import NasaApiObject


''' Retrieves sound files uploaded by NASA

Query Parameters:
query   string  Search text to filter results
limit   int     Number of tracks to return
'''
def sounds(query, limit=10):
    payload = {'q': query, 'limit': validations.optional_int(limit)}
    response = api.api_get(
        'https://api.nasa.gov/planetary/sounds',
        payload,
    )
    return [Sound.from_response(r) for r in response['results']]


class Sound(NasaApiObject):
    """NASA sound data (BETA)"""
    class Meta(object):
        properties = ['title', 'id', 'description', 'download_url',
                      'duration', 'last_modified', 'license', 'stream_url',
                      'tag_list']

    def __init__(self, **kwargs):
        super(Sound, self).__init__(**kwargs)

    def __repr__(self):
        return '<NasaSound id="%s">' % self.id
