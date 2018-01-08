from rdflib import Namespace

from csvwlib.utils.rdf.CSVW import CONST_STANDARD_MODE, CONST_MINIMAL_MODE
from csvwlib.utils.json.CommonProperties import CommonProperties
from csvwlib.utils.json.JSONLDUtils import JSONLDUtils
from csvwlib.utils.rdf.CSVW import is_non_core_annotation
from csvwlib.utils.rdf.Namespaces import Namespaces
from csvwlib.utils.url.UriTemplateUtils import UriTemplateUtils

CSVW = Namespace('http://www.w3.org/ns/csvw#')


class ToJSONConverter:

    def __init__(self, atdm, metadata):
        super().__init__()
        self.json = {}
        self.metadata = metadata
        self.atdm = atdm
        self.mode = CONST_STANDARD_MODE

    def convert(self, mode=CONST_STANDARD_MODE):
        self.mode = mode
        tables = []
        self.json['tables'] = tables
        self.copy_notes_and_non_core(self.atdm, self.json)

        for atdm_table in self.atdm['tables']:
            tables.append(self._parse_table(atdm_table))

        if self.mode == CONST_MINIMAL_MODE:
            self._convert_to_minimal()
        return self.json

    def _parse_table(self, atdm_table):
        table = {'url': atdm_table['url']}
        if '@id' in atdm_table:
            table['@id'] = atdm_table['@id']
        self.copy_notes_and_non_core(atdm_table, table)
        rows = []
        table['row'] = rows
        for atdm_row in atdm_table['rows']:
            rows.append(self._parse_row(atdm_table, atdm_row))
        return table

    def _parse_row(self, atdm_table, atdm_row):
        row = {'rownum': atdm_row['number'], 'url': atdm_row['@id']}
        self.copy_notes_and_non_core(atdm_row, row)
        self._add_row_titles(row, atdm_row, atdm_table)
        described_row = {}
        subjects = {'': described_row}
        self._supply_subjects(atdm_table, atdm_row, subjects)

        for cell in atdm_row['cells'].items():
            col_name, values = cell
            for column_metadata in atdm_table['columns']:
                if column_metadata['name'] == col_name:
                    break
            about_url = ''
            if 'aboutUrl' in column_metadata:
                about_url = UriTemplateUtils.insert_value(column_metadata['aboutUrl'], atdm_row, col_name,
                                                          atdm_table['url'])
            subject = subjects[about_url]
            if column_metadata.get('suppressOutput', False):
                continue
            value = self._value(col_name, values, atdm_row, atdm_table, column_metadata)
            prop = self._property(col_name, atdm_row, atdm_table, column_metadata)
            if prop in subject:
                if type(subject[prop]) is str:
                    subject[prop] = [subject[prop]]
                if type(value) is str:
                    subject[prop].append(value)
                else:
                    subject[prop].extend(value)
            else:
                subject[prop] = value

        if len(subjects) > 1:
            described_row = {**described_row, **list(subjects.values())[1]}
            row['describes'] = [described_row]
            for subject, obj in list(subjects.items())[2:]:
                subject_included = False
                for key, value in list(described_row.items()):
                    if type(value) is dict and value.get('@id') == subject:
                        subject_included = True
                        break
                if not subject_included:
                    row['describes'].append(obj)
        else:
            row['describes'] = [described_row]
        return row

    def _supply_subjects(self, atdm_table, atdm_row, subjects):
        for cell, column_metadata in zip(atdm_row['cells'].items(), atdm_table['columns']):
            col_name, values = cell
            if 'aboutUrl' not in column_metadata:
                continue
            resolved_subject = UriTemplateUtils.insert_value(column_metadata['aboutUrl'], atdm_row, col_name,
                                                             atdm_table['url'])
            subjects[resolved_subject] = {'@id': resolved_subject}
        self._handle_virtual_columns(atdm_table, atdm_row, '', subjects)

    @staticmethod
    def _handle_virtual_columns(atdm_table, atdm_row, col_name, subjects):
        for column_metadata in reversed(atdm_table['columns']):
            if 'virtual' not in column_metadata or column_metadata['virtual'] is False:
                break
            subject_id = UriTemplateUtils.insert_value(column_metadata['aboutUrl'], atdm_row, col_name,
                                                       atdm_table['url'])
            subject = subjects[subject_id]
            if column_metadata['propertyUrl'] == 'rdf:type':
                subject['@type'] = column_metadata['valueUrl']
            else:
                prop = UriTemplateUtils.insert_value(column_metadata['propertyUrl'], atdm_row, col_name,
                                                     atdm_table['url'])
                subject_id = UriTemplateUtils.insert_value(column_metadata['valueUrl'], atdm_row, col_name,
                                                           atdm_table['url'])
                subject[prop] = {'@id': subject_id}
                subjects[subject_id] = subject[prop]

    @staticmethod
    def _value(col_name, values, atdm_row, atdm_table, column_metadata):
        if 'valueUrl'in column_metadata:
            value_url = CommonProperties.expand_property_if_possible(column_metadata['valueUrl'])
            return UriTemplateUtils.insert_value(value_url, atdm_row, col_name, atdm_table['url'])
        else:
            if len(values) == 1:
                return values[0]
            else:
                return list(map(lambda value: value, values))

    @staticmethod
    def _property(col_name, atdm_row, atdm_table, column_metadata):
        if 'propertyUrl'in column_metadata:
            resolved = UriTemplateUtils.insert_value(column_metadata['propertyUrl'], atdm_row, col_name,
                                                     atdm_table['url'])
            return Namespaces.replace_url_with_prefix(resolved)
        else:
            return column_metadata['name']

    @staticmethod
    def copy_notes_and_non_core(source, target):
        if 'notes' in source:
            target['notes'] = JSONLDUtils.to_json(source['notes'])

        for key, value in source.items():
            if is_non_core_annotation(key):
                value = JSONLDUtils.to_json(source[key])
                target[key] = value

    @staticmethod
    def _add_row_titles(row, atdm_row, atdm_table):
        if 'rowTitles' not in atdm_table:
            return
        titles = atdm_table['rowTitles']
        if len(titles) == 1:
            row['titles'] = atdm_row['cells'][titles[0]][0]
        else:
            row['titles'] = list(map(lambda title: atdm_row['cells'][title][0], titles))

    def _convert_to_minimal(self):
        rows = []
        for table in self.json['tables']:
            for row in table['row']:
                rows.extend(row['describes'])
        self.json = rows
