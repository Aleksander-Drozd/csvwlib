from rdflib import URIRef

from csvwlib.utils.json.CommonProperties import CommonProperties
from csvwlib.utils.rdf.Namespaces import Namespaces


class ValueUrlUtils:

    @staticmethod
    def create_uri_ref(value, value_url):
        if CommonProperties.is_common_property(value_url):
            return Namespaces.get_term(value_url)
        if '{' not in value_url:
            return URIRef(value_url)
        sufix = ''
        key = value_url[value_url.find('{') + 1:value_url.find('}')]
        domain = value_url[:value_url.find('{')]
        if key.startswith('#'):
            sufix = '#'

        return URIRef(domain + sufix + value)
