from nasa.base import NasaApiObject

class Temperature(NasaApiObject):
    """NASA temperature anomalies"""
    class Meta(object):
        properties = ['year', 'anomaly']

    def __init__(self, api, **kwargs):
        super(Temperature, self).__init__(api, **kwargs)
