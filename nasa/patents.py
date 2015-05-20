from nasa.base import NasaApiObject
from nasa import api

def patents(query, concept_tags=None, limit=None):
    payload = {
        'query': query,
        'concept_tags': concept_tags,
        'limit': limit,
    }
    response = api.api_get('https://api.data.gov/nasa/patents/content', payload)
    return [Patent.from_response(r) for r in response['results']]

class Patent(NasaApiObject):
    """NASA's Patent Portfolio"""
    class Meta(object):
        properties = ['category', 'client_record_id', 'center', 'eRelations',
                      'reference_number', 'expiration_date', 'abstract',
                      'innovator', 'contact', 'publication', 'concepts',
                      'serial_number', 'patent_number', 'id', 'trl']

    def __init__(self, **kwargs):
        super(Patent, self).__init__(**kwargs)
        if self.concepts is not None:
            self.concepts = self.concepts.values()

    def __repr__(self):
        return '<NasaPatent id="%s">' % self.id
