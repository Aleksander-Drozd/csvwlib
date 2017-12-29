import json as jsonlib

from utils.CSVUtils import CSVUtils
from utils.DialectUtils import DialectUtils
from utils.MetadataLocator import MetadataLocator
from utils.PropertyUtils import is_common_property, is_array_property, is_link_property, is_object_property, \
    is_natural_language_property, is_atomic_property

from pycsvw.utils.json import CommonProperties
from pycsvw.utils.json import JSONLDUtils


class ModelConverter2:
    """
    Skipped:
    - 5. encoding
    Normalization:
    - 1.4.1 base property
    - 4.
    """

    def __init__(self, csv_url):
        self.csv_url = csv_url
        self.csv = CSVUtils.parse_csv_from_url_to_list(csv_url)
        self.metadata = MetadataLocator.find_and_get(csv_url)

    def convert(self):
        if self.metadata is None:
            t, embedded = self.parse_tabular_data_file(self.csv_url, DialectUtils.get_default())
            self.metadata = embedded
            print(jsonlib.dumps(embedded, indent=4))
        self._normalize_metadata()
        print(jsonlib.dumps(self.metadata, indent=4))

        if 'tableSchema' in self.metadata:
            self._normalize_dialect(self.metadata)
            table_json, embedded_metadata = self.parse_tabular_data_file(self.metadata['url'], self.metadata['dialect'])
        else:
            for table in self.metadata['tables']:
                self._normalize_dialect(table)
                table_json, embedded_metadata = self.parse_tabular_data_file(table['url'], table['dialect'])
                # 3.5 verify compatibility

        return table_json

    def _normalize_dialect(self, table):
        dialect = DialectUtils.get_default()
        dialect = {**dialect, **self.metadata.get('dialect', {})}
        dialect = {**dialect, **table.get('dialect', {})}
        if dialect == DialectUtils.get_default():
            # override dialect based on content-type headers
            pass
        if 1 == 1:  # content type http
            pass
        table['dialect'] = dialect

    def parse_tabular_data_file(self, csv_url, dialect):
        # table T
        table = {'columns': [], 'rows': [], 'id': None, 'url': csv_url, 'table': 'auto', 'suppressOutput': False,
                 'notes': False, 'foreignKeys': [], 'transformations': []}
        # embedded metadata document structure M
        metadata = {'@context': 'http://www.w3.org/ns/csvw', 'rdfs:comment': [], 'tableSchema': {'columns': []}}
        metadata['url'] = csv_url
        source_row_number = 1
        csv = CSVUtils.parse_csv_from_url_to_list(csv_url)
# 6
        for row_index in range(dialect['skipRows']):
            row = csv[source_row_number - 1]
            row = row.join('')
            if dialect['commentPrefix'] is not None:
                if row.startswith(dialect['commentPrefix']):
                    row = row.replace(dialect['commentPrefix'], '', 1)
                    metadata['rdfs:comment'].append(row)
            else:
                if row != '':
                    metadata['rdfs:comment'].append(row)
            source_row_number += 1
# 7
        for foo in range(dialect['headerRowCount']):
            row = csv[source_row_number - 1]
            if dialect['commentPrefix'] is not None and row[0].startswith(dialect['commentPrefix']):
                row = row.replace(dialect['commentPrefix'], '', 1)
                metadata['rdfs:comment'].append(row.join(''))
            else:
                row = row[dialect['skipColumns']:]
                for i, value in enumerate(row):
                    if value == '' or value.isspace():
                        continue
                    elif i >= len(metadata['tableSchema']['columns']):
                        metadata['tableSchema']['columns'].append({'titles': [value]})
                    else:
                        metadata['tableSchema']['columns'][i]['titles'].append(value)
            source_row_number += 1

        if dialect['headerRowCount'] == 0:
            for cell in csv[source_row_number - 1][dialect['skipColumns']:]:
                metadata['tableSchema']['columns'].append({})
        row_number = 1
# 10
        if len(csv) >= source_row_number:
            for row in csv[source_row_number - 1:]:
                source_column_number = 1
                row = csv[source_row_number - 1]
                if dialect['commentPrefix'] is not None and row[0].startswith(dialect['commentPrefix']):
                    row = row.join('')
                    row = row.replace(dialect['commentPrefix'], '', 1)
                    metadata['rdfs:comment'].append(row)
                else:
                    if all(map(lambda string: string == '', row)) and dialect['skipBlankRows']:
                        source_row_number += 1
                        continue
                # row R
                # json_row = {'table': table, 'number': row_number, 'source_number': source_row_number, 'primaryKey': [],
                json_row = {'number': row_number, 'source_number': source_row_number, 'primaryKey': [],
                            'referencedRows': [], 'cells': []}
                table['rows'].append(json_row)
                row = row[dialect['skipColumns']:]
                source_column_number += dialect['skipColumns']
# 10.4.5
                for i, cell_value in enumerate(row):
                    if not self._has_index(i, table['columns']):
                        # column C
                        column = ModelConverter2._get_default_column(table, i, source_column_number)
                        # append at index
                        table['columns'].append(column)
                    column = table['columns'][i]
                    # cell D
                    cell_json = self._create_cell(table, column, json_row, row[i])
                    column['cells'].append(cell_json)
                    json_row['cells'].append(cell_json)  # index i
                    source_column_number += 1
                source_row_number += 1

        if metadata['rdfs:comment'] == []:
            del metadata['rdfs:comment']
        return table, metadata

    @staticmethod
    def _has_index(index, collection):
        return index < len(collection)

    @staticmethod
    def _get_default_column(table, i, source_column_number):
        # return {'table': table, 'number': i, 'source_number': source_column_number, 'name': None, 'titles': [],
        return {'number': i, 'source_number': source_column_number, 'name': None, 'titles': [],
                'virtual': False, 'suppressOutput': False, 'datatype': 'string', 'default': '', 'lang': 'und',
                'null': '', 'ordered': False, 'required': False, 'separator': None, 'textDirection': 'auto',
                'aboutUrl': None, 'propertyUrl': None, 'valueUrl': None, 'cells': []}

    @staticmethod
    def _create_cell(table, column, row, cell_value):
        # return {'table': table, 'column': column, 'row': row, 'stringValue': cell_value, 'value': cell_value,
        return {'stringValue': cell_value, 'value': cell_value,
                'errors': [], 'textDirection': 'auto', 'ordered': 'auto', "aboutUrl": None, 'propertyUrl': None,
                'valueUrl': None}

    @staticmethod
    def _read_row(row, dialect, row_content=''):
        escape_character = dialect['doubleQuote']
        quote_character = dialect['quoteChar']
        if row == '':
            return row_content
        if row.startswith(escape_character) and row[1] == quote_character:
            row_content += row[:2]
            row_content += ModelConverter2._read_row(row[2:], dialect, row_content)
        elif row.startswith(escape_character) and escape_character != quote_character:
            row_content = row[:2]
            row_content += ModelConverter2._read_row(row[2:], dialect, row_content)
        elif row.startswith(quote_character):
            pass
        elif row.startswith(dialect['lineTerminators'][0]):
            # TODO
            return row_content
        else:
            row_content += row[0]
            row_content += ModelConverter2._read_row(row[1:], dialect, row_content)

    @staticmethod
    def _read_quoted_value(value):
        return value

    def _normalize_metadata(self):
        for prop in self.metadata.items():
            self._normalize_property(prop, self.metadata)
        self.metadata['@context'] = 'http://www.w3.org/ns/csvw'

    def _normalize_property(self, prop, parent):
        key, value = prop
        if key == '@context':
            return
        if is_common_property(key, value) or key == 'notes':
            if type(value) is list:
                for entry in key:
                    self._normalize_entry(key, entry)
            else:
                self._normalize_entry(key, value)
        elif is_array_property(key):
            for item in value:
                for entry in item.items():
                    self._normalize_property(entry, item)
        elif is_link_property(key):
            parent[key] = JSONLDUtils.resolve_against_base_url(value, self.metadata['@context'])  # url normalization
        elif is_object_property(key):
            # 'str' (url) value not supported
            if type(value) is dict:
                for item in value.items():
                    self._normalize_property(item, value)
        elif is_natural_language_property(key) and value is not dict:
            language = JSONLDUtils.language(self.metadata['@context'])
            language = language if language is not None else "und"
            _value = value if type(value) is list else [value]
            parent[key] = {language: _value}
        elif is_atomic_property(value):
            #not supported
            pass

    def _normalize_entry(self, top_key, top_value):
        if type(top_value) is str:
            self.metadata[top_key] = {'@value': top_value}
            language = JSONLDUtils.language(self.metadata['@context'])
            if language is not None:
                self.metadata[top_key]['@language'] = language

        if type(top_value) is dict and '@value' not in top_value:
            for key, value in top_value:
                if key is '@id' and is_common_property(key, value):
                    expanded_uri = CommonProperties.expand_property_if_possible(value)
                    resolved_uri = JSONLDUtils.resolve_against_base_url(expanded_uri, self.metadata['@context'])
                    top_value[key] = resolved_uri
                elif key is not '@type':
                    self._normalize_entry(key, value)




