class JSONLDUtils:

    @staticmethod
    def language(context, metadata={}):
        language = JSONLDUtils.language_in_context(context)
        if language is not None:
            return language
        for key, value in metadata.items():
            if key == 'lang':
                return value

    @staticmethod
    def language_in_context(context):
        if type(context) is str:
            return None
        if type(context) is list:
            for value in context:
                if type(value) is dict and '@language' in value:
                    return value['@language']
        if type(context) is dict:
            return context.get('@language')

    @staticmethod
    def resolve_against_base_url(url, context):
        """
        :return url resolved against baseUrl if '@base' is present in context,
        otherwise original url
        """
        if type(context) is str:
            return url
        if type(context) is list:
            for value in context:
                if type(value) is dict and '@base' in value:
                    return value['@base'] + url
            return url
        if type(context) is dict:
            return context['@base'] + url if '@base' in context else url

    @staticmethod
    def to_json(value):
        """ https://www.w3.org/TR/2015/REC-csv2json-20151217/#json-ld-to-json """
        if type(value) is str:
            return value
        if type(value) is list:
            return list(map(JSONLDUtils.to_json, value))

        if '@value' in value:
            return value['@value']
        if '@id' in value:
            return value['@id']

        json = {}
        for key, value in value.items():
            _value = JSONLDUtils.to_json(value)
            json[key] = _value
        return json
