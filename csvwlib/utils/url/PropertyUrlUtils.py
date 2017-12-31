from rdflib import Namespace

from csvwlib.utils.rdf.Namespaces import Namespaces
from csvwlib.utils.url.UriTemplateUtils import UriTemplateUtils


class PropertyUrlUtils:

    @staticmethod
    def domain(property_url):
        return property_url.rsplit('/', 1)[0] + '/'

    @staticmethod
    def ontology_prefix(property_url):
        if ':' in property_url:
            prefix, term = property_url.split(':')
            return prefix
        after_http_part = property_url.split('//')[1]
        if after_http_part.startswith('www.'):
            after_http_part = after_http_part[4:]
        return after_http_part[:after_http_part.find('.')]

    @staticmethod
    def create_namespace(property_url, domain_url=''):
        property_url = UriTemplateUtils.expand(property_url, domain_url)
        if ':' in property_url and '://' not in property_url:
            prefix, term = property_url.split(':')
            return Namespaces.get(prefix)
        if '{' not in property_url:
            return Namespace(property_url)

        property_key = property_url[property_url.find('{') + 1:property_url.find('}')]
        prefix = ''
        if property_key.startswith('#'):
            property_key = property_key[1:]
            property_url = property_url.replace('#', '')
            prefix = '#'
        if property_key == '_name':
            namespace_url = property_url.replace('{_name}', prefix)
            return Namespace(namespace_url)
