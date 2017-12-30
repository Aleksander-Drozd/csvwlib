from rdflib import URIRef, Literal

from csvwlib.utils.ATDMUtils import ATDMUtils
from csvwlib.utils.json.CommonProperties import CommonProperties


class UriTemplateUtils:

    @staticmethod
    def insert_value_rdf(url, atdm_row, col_name, domain_url):
        """ Does the same what normal 'insert_value' but
        returns rdf type: URIRef of Literal based on uri"""
        filled_url = UriTemplateUtils.insert_value(url, atdm_row, col_name, domain_url)
        return URIRef(filled_url) if filled_url.startswith('http') else Literal(filled_url)

    @staticmethod
    def insert_value(url, atdm_row, col_name, domain_url):
        """ Inserts value into uri template - between {...}
        If url is common property, it is returned unmodified
        Also uri is expanded with domain url if necessary """
        if CommonProperties.is_common_property(url):
            return url
        url = UriTemplateUtils.expand(url, domain_url)
        if '{' not in url:
            return url

        key = url[url.find('{') + 1:url.find('}')]
        key = key.replace('#', '')
        prefix = UriTemplateUtils.prefix(url, '')

        if key == '_row':
            return prefix + str(atdm_row['number'])
        elif key == '_sourceRow':
            return prefix + atdm_row['url'].rsplit('=')[1]
        elif key == '_name':
            return prefix + col_name
        else:
            return prefix + ATDMUtils.column_value(atdm_row, key)

    @staticmethod
    def expand(url, domain_url):
        if url.startswith('http'):
            return url
        else:
            return domain_url + url

    @staticmethod
    def prefix(url, csv_url):
        """ :return prefix of uri template - the part before {...}"""
        if url.startswith('http'):
            key = url[url.find('{') + 1:url.find('}')]
            if key.startswith('#'):
                url = url[:url.find('#') + 1]
                return url.replace('{', '')
            else:
                return url[:url.find('{')]
        else:
            return csv_url + url[:url.find('{')]
