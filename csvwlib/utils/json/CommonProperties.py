from rdflib import Literal, URIRef, BNode, RDF

from csvwlib.utils.rdf.Namespaces import Namespaces
from csvwlib.utils.rdf.RDFUtils import RDFUtils


class CommonProperties:
    """https://www.w3.org/TR/2015/REC-tabular-metadata-20151217/#common-properties
    """

    @staticmethod
    def property_to_triples(entry, subject, language):
        key, value = entry
        return {
            str: lambda: CommonProperties._handle_raw_string(entry, subject, language),
            list: lambda: CommonProperties._handle_list(entry, subject, language),
            dict: lambda: CommonProperties._handle_dict(entry, subject, language)
        }[type(value)]()

    @staticmethod
    def _handle_raw_string(entry, subject, language):
        key, value = entry
        term = RDFUtils.term(key)
        return [(subject, term, Literal(value, lang=language))]

    @staticmethod
    def _handle_list(entry, subject, language):
        key, values = entry
        predicate = Namespaces.get_term(key)
        triples = []
        for value in values:
            if type(value) is dict:
                triples.extend(CommonProperties.property_to_triples((key, value), subject, language))
            else:
                triples.append((subject, predicate, Literal(value, lang=language)))
        return triples

    @staticmethod
    def _handle_dict(entry, subject, language):
        triples = []
        key, json = entry
        predicate = Namespaces.get_term(key)

        if '@value' in json or '@id' in json:
            raw_type = json.get('@type')
            rdf_datatype = Namespaces.get_term(raw_type)
            value = CommonProperties._json_ld_value(json, rdf_datatype)
            triples.append((subject, predicate, value))
        else:
            local_subject = BNode()
            triples.append((subject, predicate, local_subject))
            for _key, _value in json.items():
                if CommonProperties.is_common_property(_key):
                    triple = CommonProperties.property_to_triples((_key, _value), local_subject, language)
                    triples.extend(triple)
            if '@type' in json:
                rdf_value_type = Namespaces.get_term(json['@type'])
                triples.append((local_subject, RDF.type, rdf_value_type))

        return triples

    @staticmethod
    def _has_nested_properties(keys):
        return any(map(CommonProperties.is_common_property, keys))

    @staticmethod
    def _json_ld_value(json, datatype):
        if '@value' in json:
            return Literal(json['@value'], datatype=datatype)
        elif '@id' in json:
            return URIRef(json['@id'])

    @staticmethod
    def is_common_property(prop):
        return ':' in prop and '://' not in prop

    @staticmethod
    def expand_property_if_possible(prop):
        if not CommonProperties.is_common_property(prop):
            return prop

        prefix, prop = prop.split(':')
        return Namespaces.get(prefix).term(prop)

    @staticmethod
    def expand_property(prop):
        prefix, prop = prop.split(':')
        return Namespaces.get(prefix).term(prop)
