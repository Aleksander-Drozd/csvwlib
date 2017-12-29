from pycsvw.converter.ModelConverter import ModelConverter
from pycsvw.converter.ToJSONConverter import ToJSONConverter
from pycsvw.converter.ToRDFConverter import ToRDFConverter


class CSVWConverter:

    @staticmethod
    def to_rdf(csv_url=None, metadata_url=None, mode='standard', format=None):
        assert csv_url is not None or metadata_url is not None
        atdm, metadata = ModelConverter(csv_url, metadata_url).convert_to_atdm(mode)
        return ToRDFConverter(atdm, metadata).convert(mode, format)

    @staticmethod
    def to_json(csv_url=None, metadata_url=None, mode='standard'):
        assert csv_url is not None or metadata_url is not None
        atdm, metadata = ModelConverter(csv_url, metadata_url).convert_to_atdm(mode)
        return ToJSONConverter(atdm, metadata).convert(mode)
