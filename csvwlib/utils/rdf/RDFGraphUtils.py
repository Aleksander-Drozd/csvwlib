from rdflib import Namespace

from csvwlib.utils.json.CommonProperties import CommonProperties
from csvwlib.utils.rdf.Namespaces import Namespaces
from csvwlib.utils.url.PropertyUrlUtils import PropertyUrlUtils


class RDFGraphUtils:

    @staticmethod
    def add_default_bindings(graph):
        for abbreviation, namespace in Namespaces.all().items():
            graph.bind(abbreviation, namespace)

    @staticmethod
    def add_bindings_from_metadata(graph, metadata):
        if len(metadata['tables']) == 1:
            graph.bind('', Namespace(metadata['tables'][0]['url']) + '#')
        for table in metadata['tables']:
            RDFGraphUtils._add_binding_if_necessary(graph, table['tableSchema'])
            for column in table['tableSchema']['columns']:
                RDFGraphUtils._add_binding_if_necessary(graph, column)

    @staticmethod
    def _add_binding_if_necessary(graph, metadata):
        if 'propertyUrl' in metadata and CommonProperties.is_common_property(metadata['propertyUrl']):
            property_url = metadata['propertyUrl']
            prefix = PropertyUrlUtils.ontology_prefix(property_url)
            namespace = PropertyUrlUtils.create_namespace(property_url)
            graph.bind(prefix, namespace)
