import base64
import re

from csvwlib.utils.NumericUtils import NumericUtils
from csvwlib.utils.TypeConverter import TypeConverter
from csvwlib.utils.metadata import non_regex_types
from csvwlib.utils.rdf.CSVW import number_datatypes, date_datatypes

type_constraints = {
    'boolean': {'type': 'boolean'},
    'byte': {'type': 'number', 'max': 128},
    'dayTimeDuration': {'type': 'dayTimeDuration', 'regex': '[^YM]*[DT].*'},
    'duration': {'type': 'duration', 'regex': '-?P[0-9]+Y?([0-9]+M)?([0-9]+D)?(T([0-9]+H)?([0-9]+M)?([0-9]+(\.[0-9]+)?S)?)?'},
    'unsignedLong': {'type': 'number', 'min': 0},
    'unsignedShort': {'type': 'number', 'min': 0},
    'unsignedByte': {'type': 'number', 'min': 0},
    'positiveInteger': {'type': 'number', 'min': 1},
    'negativeInteger': {'type': 'number', 'max': -1},
    'nonPositiveInteger': {'type': 'number', 'max': 0},
    'nonNegativeInteger': {'type': 'number', 'min': 0},
    'double': {'type': 'number'},
    'number': {'type': 'number'},
    'float': {'type': 'number'},
    'yearMonthDuration': {'type': 'yearMonthDuration', 'regex': '-?P((([0-9]+Y)([0-9]+M)?)|([0-9]+M))'},
}


def is_compatible_with_datatype(value, datatype):
    if datatype is None:
        return True
    if not satisfies_datatype_constraints(value, datatype):
        return False
    if not satisfies_user_bounds(value, datatype):
        return False
    if not satisfies_regex(value, datatype):
        return False
    if not satisfies_length(value, datatype):
        return False
    return True


def satisfies_datatype_constraints(value, datatype):
    datatype_name = get_type_name(datatype)
    if datatype_name not in type_constraints:
        return True

    constraint = type_constraints[datatype_name]

    if constraint['type'] == 'number':
        if not NumericUtils.is_numeric(value):
            return False
    if constraint['type'] == 'boolean':
        if type(datatype) is dict and 'format' in datatype:
            boolean_templates = datatype['format'].split('|')
            if len(boolean_templates) != 2 or value not in boolean_templates:
                return False
    if 'regex' in constraint and 'format' not in datatype:
        return re.match(constraint['regex'], value)
    if 'min' in constraint:
        if float(value) < constraint['min']:
            return False
    if 'max' in constraint:
        if float(value) > constraint['max']:
            return False
    return True


operated_types = number_datatypes + date_datatypes


def satisfies_user_bounds(value, datatype):
    if type(datatype) is not dict:
        return True
    if get_type_name(datatype) not in operated_types:
        return True
    value = TypeConverter.convert(value, datatype)
    if 'minimum' in datatype:
        constraint_value = TypeConverter.convert(datatype['minimum'], datatype)
        if value < constraint_value:
            return False
    if 'maximum' in datatype:
        constraint_value = TypeConverter.convert(datatype['maximum'], datatype)
        if value > constraint_value:
            return False
    if 'minInclusive' in datatype:
        constraint_value = TypeConverter.convert(datatype['minInclusive'], datatype)
        if value < constraint_value:
            return False
    if 'maxInclusive' in datatype:
        constraint_value = TypeConverter.convert(datatype['maxInclusive'], datatype)
        if value > constraint_value:
            return False
    if 'minExclusive' in datatype:
        constraint_value = TypeConverter.convert(datatype['minExclusive'], datatype)
        if value <= constraint_value:
            return False
    if 'maxExclusive' in datatype:
        constraint_value = TypeConverter.convert(datatype['maxExclusive'], datatype)
        if value >= constraint_value:
            return False
    return True


def satisfies_regex(value, datatype):
    if type(datatype) is dict:
        base = datatype.get('base', 'string')
        datatype_format = datatype.get('format')
        if base not in non_regex_types and datatype_format is not None:
            try:
                re.compile(datatype_format)
                return re.match(datatype_format, value)
            except re.error:
                return True
    return True


def satisfies_length(value, datatype):
    if type(datatype) is not dict:
        return True
    comparing_function = len
    if get_type_name(datatype) == 'hexBinary':
        value = int(value, 16)
        comparing_function = bytes_count_in_number
    if get_type_name(datatype) == 'base64Binary':
        value = base64.decodebytes(str.encode(value))
    if 'length' in datatype:
        if comparing_function(value) != datatype['length']:
            return False
    if 'maxLength' in datatype:
        if comparing_function(value) > datatype['maxLength']:
            return False
    if 'minLength' in datatype:
        if comparing_function(value) < datatype['minLength']:
            return False
    return True


def bytes_count_in_number(number):
    n = 0
    while number != 0:
        number >>= 8
        n += 1
    return n


def get_type_name(datatype_entry):
    if type(datatype_entry) is dict:
        return datatype_entry.get('base', 'string')
    else:
        return datatype_entry
