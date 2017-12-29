from rdflib import XSD, RDF, URIRef


class OntologyUtils:

    _omitted_types = ['string', 'number', 'boolean']
    _name_mappings = {'datetime': 'dateTime'}
    _type_mappings = {'xml': RDF.XMLLiteral}

    @staticmethod
    def type(column_metadata):
        if 'datatype' not in column_metadata:
            return None
        datatype = column_metadata['datatype']
        if type(datatype) is dict:
            if '@id' in datatype:
                datatype = datatype['@id']
                return URIRef(datatype)
            datatype = datatype['base']
        if datatype in OntologyUtils._omitted_types:
            return None

        datatype = OntologyUtils._name_mappings.get(datatype, datatype)
        return OntologyUtils._type_mappings.get(datatype, XSD.term(datatype))
