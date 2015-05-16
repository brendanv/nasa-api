class NasaApiObject(object):
    """docstring for NasaApiObject"""
    def __init__(self, api, **kwargs):
        self._api = api
        for k in kwargs:
            if k in self.Meta.properties:
                setattr(self, '{0}'.format(k), kwargs[k])

    @classmethod
    def from_response(cls, api, response):
        kwargs = {}
        for prop in cls.Meta.properties:
            try:
                kwargs[prop] = response[prop]
            except KeyError:
                pass
        return cls(api, **kwargs)
