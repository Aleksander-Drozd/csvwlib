from csvwlib.utils.rdf.Namespaces import Namespaces


class RDFUtils:

    @staticmethod
    def term(common_property):
        """https://www.w3.org/TR/2015/REC-tabular-metadata-20151217/#common-properties
        """
        namespace_abbreviation, term = common_property.split(':')
        return Namespaces.get(namespace_abbreviation).term(term)
