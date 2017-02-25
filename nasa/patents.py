from nasa import api, validations
from nasa.base import NasaApiObject


''' Retrieves patents from NASA's patent portfolio

Query Parameters:
query         string  Search text to filter results
concept_tags  bool    Return an ordered dictionary of concepts from the
                      patent abstract
limit         int     Number of patents to return
'''
def patents(query, concept_tags=None, limit=None):
    payload = {
        'query': query,
        'concept_tags': concept_tags,
        'limit': validations.optional_int(limit),
    }
    response = api.api_get('https://api.nasa.gov/patents/content', payload)
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
