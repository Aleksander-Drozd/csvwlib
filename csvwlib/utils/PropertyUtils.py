_array_properties = ['tables', 'transformations', 'notes', '@context', 'notes', 'foreignKeys',
                     'columns', 'lineTerminators']
_link_properties = ['url', 'targetFormat', 'scriptFormat', '@id', 'resource', 'schemaReference']
_object_properties = ['tableSchema', 'dialect', 'reference']
_natural_language_properties = ['titles']
_atomic_properties = ['source', '@type', 'null', 'lang', 'textDirection', 'separator', 'ordered', 'default', 'datatype',
                      'required', 'base', 'format', 'length', 'minLength', 'maxLength', 'minimum', 'maximum',
                      'minInclusive', 'maxInclusive', 'minExclusive', 'maxExclusive', 'decimalChar', 'groupChar',
                      'pattern', 'tableDirection', '@language', '@base', 'name', 'required', 'suppressOutput',
                      'virtual', 'commentPrefix', 'doubleQuote', 'delimiter', 'encoding', 'header', 'headerRowCount',
                      'quoteChar', 'skipBlankRows', 'skipColumns', 'skipInitialSpace', 'skipRows', 'trim']
_uri_template_properties = ['aboutUrl', 'propertyUrl', 'valueUrl']
_column_reference_properties = ['primaryKey', 'rowTitles', 'columnReference']


def is_common_property(key, value):
    return type(key) is str and (':' in key or key.startswith('http')) and type(value) is dict


def is_array_property(key):
    # return type(value) is list and all(type(item) is dict for item in value)
    return key in _array_properties


def is_link_property(key):
    # return type(value) is str and value.startsWith('http')
    return key in _link_properties


def is_object_property(key):
    # return value is dict or (type(value) is str and value.startsWith('http') and value.endsWith('.json'))
    return key in _object_properties


def is_natural_language_property(key):
    return key in _natural_language_properties


def is_atomic_property(key):
    return key in _atomic_properties
