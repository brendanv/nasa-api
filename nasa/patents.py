from nasa.base import NasaApiObject

class Patent(NasaApiObject):
    """NASA's Patent Portfolio"""
    class Meta(object):
        properties = ['category', 'client_record_id', 'center', 'eRelations',
                      'reference_number', 'expiration_date', 'abstract',
                      'innovator', 'contact', 'publication', 'concepts',
                      'serial_number', 'patent_number', 'id', 'trl']

    def __init__(self, api, **kwargs):
        super(Patent, self).__init__(api, **kwargs)
        if self.concepts is not None:
            self.concepts = self.concepts.values()

    def __repr__(self):
        return '<NasaPatent id="%s">' % self.id
