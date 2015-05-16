from nasa.base import NasaApiObject

class Sound(NasaApiObject):
    """NASA sound data (BETA)"""
    class Meta(object):
        properties = ['title', 'id', 'description', 'download_url',
                      'duration', 'last_modified', 'license', 'stream_url',
                      'tag_list']

    def __ini__(self, api, **kwargs):
        super(Sound, self).__init__(api, **kwargs)

    def __repr__(self):
        return '<NasaSound id="%s">' % self.id
