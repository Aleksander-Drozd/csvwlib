import unittest
from unittest import TestCase, mock
from unittest.mock import patch

from rdflib import Graph, URIRef
from rdflib.compare import to_isomorphic

from csvwlib.converter.ModelConverter import MetadataValidator, ValuesValidator
from csvwlib.utils.rdf.CSVW import CONST_STANDARD_MODE, CONST_MINIMAL_MODE
from csvwlib.converter.CSVWConverter import CSVWConverter


class TestToRDFConverter(TestCase):

    _remote_tests_location = 'http://www.w3.org/2013/csvw/tests/'
    _local_tests_location = 'http://localhost/tests/'
    _tests_location = _local_tests_location

    def run_test(self, tested_file=None, result_file=None, metadata_url=None, mode=CONST_STANDARD_MODE):
        result_graph_url = self._tests_location + result_file
        metadata_url = self._tests_location + metadata_url if metadata_url is not None else None
        csv_url = self._tests_location + tested_file if tested_file is not None else None
        converted = CSVWConverter.to_rdf(csv_url, metadata_url, mode)
        expected = Graph()
        expected.parse(result_graph_url)
        self.change_urls_in_result(expected)
        self.assertEqual(to_isomorphic(converted), to_isomorphic(expected))

    def change_urls_in_result(self, graph):
        for s, p, o in graph.triples((None, None, None)):
            if self._remote_tests_location in s:
                graph.remove((s, p, o))
                s = URIRef(s.replace(self._remote_tests_location, self._tests_location))
                graph.add((s, p, o))
            if self._remote_tests_location in p:
                graph.remove((s, p, o))
                p = URIRef(p.replace(self._remote_tests_location, self._tests_location))
                graph.add((s, p, o))
            if self._remote_tests_location in o:
                graph.remove((s, p, o))
                o = URIRef(o.replace(self._remote_tests_location, self._tests_location))
                graph.add((s, p, o))

    def test001(self):
        self.run_test('test001.csv', 'test001.ttl')

    def test005(self):
        self.run_test('test005.csv', 'test005.ttl')

    def test006(self):
        self.run_test('test006.csv', 'test006.ttl')

    def test007(self):
        self.run_test('test007.csv', 'test007.ttl')

    def test008(self):
        self.run_test('test008.csv', 'test008.ttl')

    def test009(self):
        self.run_test('test009.csv', 'test009.ttl')

    def test010(self):
        self.run_test('test010.csv', 'test010.ttl')

    def test011(self):
        self.run_test('test011/tree-ops.csv', 'test011/result.ttl')

    def test012(self):
        self.run_test('test012/tree-ops.csv', 'test012/result.ttl')

    def test013(self):
        self.run_test('tree-ops.csv', 'test013.ttl', 'test013-user-metadata.json')

    @mock.patch('csvwlib.utils.MetadataLocator.requests.head')
    def test014(self, head_mock):
        head_mock.return_value.headers = {'Link': ''}
        head_mock.return_value.links = {'describedby': {'url': 'linked-metadata.json'}}
        self.run_test('test014/tree-ops.csv', 'test014/result.ttl')

    def test015(self):
        self.run_test('test015/tree-ops.csv', 'test015/result.ttl', 'test015/user-metadata.json')

    @mock.patch('csvwlib.utils.MetadataLocator.requests.head')
    def test016(self, head_mock):
        head_mock.return_value.headers = {'Link': ''}
        head_mock.return_value.links = {'describedby': {'url': 'linked-metadata.json'}}
        self.run_test('test016/tree-ops.csv', 'test016/result.ttl')

    def test017(self):
        self.run_test('test017/tree-ops.csv', 'test017/result.ttl')

    def test018(self):
        self.run_test('test018/tree-ops.csv', 'test018/result.ttl', 'test018/user-metadata.json')

    def test023(self):
        self.run_test('tree-ops.csv', 'test023.ttl', 'test023-user-metadata.json')

    def test027(self):
        self.run_test('tree-ops.csv', 'test027.ttl', 'test027-user-metadata.json', CONST_MINIMAL_MODE)

    def test028(self):
        self.run_test('countries.csv', 'test028.ttl')

    def test029(self):
        self.run_test('countries.csv', 'test029.ttl', mode=CONST_MINIMAL_MODE)

    def test030(self):
        self.run_test(result_file='test030.ttl', metadata_url='countries.json')

    def test031(self):
        self.run_test(result_file='test031.ttl', metadata_url='countries.json', mode=CONST_MINIMAL_MODE)

    def test032(self):
        self.run_test(result_file='test032/result.ttl', metadata_url='test032/csv-metadata.json')

    def test033(self):
        self.run_test(result_file='test033/result.ttl', metadata_url='test033/csv-metadata.json',
                      mode=CONST_MINIMAL_MODE)

    def test036(self):
        self.run_test('test036/tree-ops-ext.csv', 'test036/result.ttl')

    def test037(self):
        self.run_test('test037/tree-ops-ext.csv', 'test037/result.ttl', mode=CONST_MINIMAL_MODE)

    def test038(self):
        self.run_test(metadata_url='test038-metadata.json', result_file='test038.ttl')

    def test039(self):
        self.run_test(metadata_url='test039-metadata.json', result_file='test039.ttl')

    def test040(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test040-metadata.json', result_file='test040.ttl')
            self.assertEqual(mock.call_count, 1)

    def test041(self):
        with patch.object(MetadataValidator, 'print_language_tag_warning') as mock:
            self.run_test(metadata_url='test041-metadata.json', result_file='test041.ttl')
            self.assertEqual(mock.call_count, 1)

    def test042(self):
        with patch.object(MetadataValidator, 'print_value_warning') as mock:
            self.run_test(metadata_url='test042-metadata.json', result_file='test042.ttl')
            self.assertEqual(mock.call_count, 1)

    def test043(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test043-metadata.json', result_file='test043.ttl')
            self.assertEqual(mock.call_count, 1)

    def test044(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test044-metadata.json', result_file='test044.ttl')
            self.assertEqual(mock.call_count, 1)

    def test045(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test045-metadata.json', result_file='test045.ttl')
            self.assertEqual(mock.call_count, 1)

    def test046(self):
        with patch.object(MetadataValidator, 'print_value_warning') as mock:
            self.run_test(metadata_url='test046-metadata.json', result_file='test046.ttl')
            self.assertEqual(mock.call_count, 1)

    def test047(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test047-metadata.json', result_file='test047.ttl')
            self.assertEqual(mock.call_count, 1)

    def test048(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test048-metadata.json', result_file='test048.ttl')
            self.assertEqual(mock.call_count, 1)

    def test049(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test049-metadata.json', result_file='test049.ttl')
            self.assertEqual(mock.call_count, 1)

    def test059(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test059-metadata.json', result_file='test059.ttl')
            self.assertEqual(mock.call_count, 1)

    def test060(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test060-metadata.json', result_file='test060.ttl')
            self.assertEqual(mock.call_count, 1)

    def test061(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test061-metadata.json', result_file='test061.ttl')
            self.assertEqual(mock.call_count, 1)

    def test062(self):
        with patch.object(MetadataValidator, 'print_value_warning') as mock:
            self.run_test(metadata_url='test062-metadata.json', result_file='test062.ttl')
            self.assertEqual(mock.call_count, 1)

    def test063(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test063-metadata.json', result_file='test063.ttl')
            self.assertEqual(mock.call_count, 1)

    def test065(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test065-metadata.json', result_file='test065.ttl')
            self.assertEqual(mock.call_count, 1)

    def test066(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test066-metadata.json', result_file='test066.ttl')
            self.assertEqual(mock.call_count, 1)

    def test067(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test067-metadata.json', result_file='test067.ttl')
            self.assertEqual(mock.call_count, 1)

    def test068(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test068-metadata.json', result_file='test068.ttl')
            self.assertEqual(mock.call_count, 1)

    def test069(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test069-metadata.json', result_file='test069.ttl')
            self.assertEqual(mock.call_count, 1)

    def test070(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test070-metadata.json', result_file='test070.ttl')
            self.assertEqual(mock.call_count, 1)

    def test071(self):
        with patch.object(MetadataValidator, 'print_value_constraint_warning') as mock:
            self.run_test(metadata_url='test071-metadata.json', result_file='test071.ttl')
            self.assertEqual(mock.call_count, 1)

    def test072(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test072-metadata.json', result_file='test072.ttl')
            self.assertEqual(mock.call_count, 1)

    def test073(self):
        with patch.object(MetadataValidator, 'print_language_tag_warning') as mock:
            self.run_test(metadata_url='test073-metadata.json', result_file='test073.ttl')
            self.assertEqual(mock.call_count, 1)

    def test075(self):
        with patch.object(MetadataValidator, 'print_value_warning') as mock:
            self.run_test(metadata_url='test075-metadata.json', result_file='test075.ttl')
            self.assertEqual(mock.call_count, 1)

    def test076(self):
        with patch.object(MetadataValidator, 'print_value_warning') as mock:
            self.run_test(metadata_url='test076-metadata.json', result_file='test076.ttl')
            self.assertEqual(mock.call_count, 1)

    def test093(self):
        with patch.object(MetadataValidator, 'print_undefined_property_warning') as mock:
            self.run_test(metadata_url='test093-metadata.json', result_file='test093.ttl')
            self.assertEqual(mock.call_count, 1)

    def test095(self):
        with patch.object(MetadataValidator, 'print_bad_array_item_type_warning') as mock:
            self.run_test(metadata_url='test095-metadata.json', result_file='test095.ttl')
            self.assertEqual(mock.call_count, 1)

    def test097(self):
        with patch.object(MetadataValidator, 'print_bad_array_item_type_warning') as mock:
            self.run_test(metadata_url='test097-metadata.json', result_file='test097.ttl')
            self.assertEqual(mock.call_count, 1)

    def test099(self):
        with patch.object(MetadataValidator, 'print_bad_array_type_warning') as mock:
            self.run_test(metadata_url='test099-metadata.json', result_file='test099.ttl')
            self.assertEqual(mock.call_count, 1)

    def test100(self):
        with patch.object(MetadataValidator, 'print_bad_array_type_warning') as mock:
            self.run_test(metadata_url='test100-metadata.json', result_file='test100.ttl')
            self.assertEqual(mock.call_count, 1)

    def test101(self):
        with patch.object(MetadataValidator, 'print_bad_array_type_warning') as mock:
            self.run_test(metadata_url='test101-metadata.json', result_file='test101.ttl')
            self.assertEqual(mock.call_count, 1)

    def test102(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test102-metadata.json', result_file='test102.ttl')
            self.assertEqual(mock.call_count, 1)

    def test105(self):
        with patch.object(MetadataValidator, 'print_missing_column_name_warning') as mock:
            self.run_test(metadata_url='test105-metadata.json', result_file='test105.ttl')
            self.assertEqual(mock.call_count, 1)

    def test106(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test106-metadata.json', result_file='test106.ttl')
            self.assertEqual(mock.call_count, 1)

    def test107(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test107-metadata.json', result_file='test107.ttl')
            self.assertEqual(mock.call_count, 1)

    def test109(self):
        with patch.object(MetadataValidator, 'print_language_tag_warning') as mock:
            self.run_test(metadata_url='test109-metadata.json', result_file='test109.ttl')
            self.assertEqual(mock.call_count, 1)

    def test110(self):
        with patch.object(MetadataValidator, 'print_warning') as mock:
            self.run_test(metadata_url='test110-metadata.json', result_file='test110.ttl')
            self.assertEqual(mock.call_count, 2)

    def test111(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test111-metadata.json', result_file='test111.ttl')
            self.assertEqual(mock.call_count, 1)

    def test112(self):
        with patch.object(MetadataValidator, 'print_bad_array_item_type_warning') as mock:
            self.run_test(metadata_url='test112-metadata.json', result_file='test112.ttl')
            self.assertEqual(mock.call_count, 1)

    def test113(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test113-metadata.json', result_file='test113.ttl')
            self.assertEqual(mock.call_count, 1)

    def test114(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test114-metadata.json', result_file='test114.ttl')
            self.assertEqual(mock.call_count, 1)

    def test115(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test115-metadata.json', result_file='test115.ttl')
            self.assertEqual(mock.call_count, 1)

    def test116(self):
        self.run_test('test116.csv?query', 'test116.ttl')

    def test117(self):
        with patch.object(MetadataValidator, 'print_bad_reference_warning') as mock:
            self.run_test('test117.csv', 'test117.ttl')
            self.assertEqual(mock.call_count, 1)

    def test118(self):
        self.run_test('test118/action.csv?query', 'test118/result.ttl')

    def test119(self):
        with patch.object(MetadataValidator, 'print_bad_reference_warning') as mock:
            self.run_test('test119/action.csv', 'test119/result.ttl')
            self.assertEqual(mock.call_count, 1)

    @mock.patch('csvwlib.utils.MetadataLocator.requests.head')
    def test120(self, head_mock):
        head_mock.return_value.headers = {'Link': ''}
        head_mock.return_value.links = {'describedby': {'url': 'test120-linked-metadata.json'}}
        with patch.object(MetadataValidator, 'print_bad_reference_warning') as mock:
            self.run_test('test120.csv', 'test120.ttl')
            self.assertEqual(mock.call_count, 1)

    def test121(self):
        self.run_test('test121', 'test121.ttl', 'test121-user-metadata.json')

    @mock.patch('csvwlib.utils.MetadataLocator.requests.head')
    def test122(self, head_mock):
        head_mock.return_value.headers = {'Link': ''}
        head_mock.return_value.links = {'describedby': {'url': 'test122-linked-metadata.json'}}
        with patch.object(MetadataValidator, 'print_bad_reference_warning') as mock:
            self.run_test('test122.csv', 'test122.ttl')
            self.assertEqual(mock.call_count, 1)

    def test123(self):
        with patch.object(MetadataValidator, 'print_bad_reference_warning') as mock:
            self.run_test('test123/action.csv', 'test123/result.ttl')
            self.assertEqual(mock.call_count, 1)

    def test124(self):
        self.run_test('tree-ops.csv', 'test124.ttl',  'test124-user-metadata.json')

    def test125(self):
        with patch.object(ValuesValidator, 'print_missing_required_value_warning') as mock:
            self.run_test(metadata_url='test125-metadata.json', result_file='test125.ttl')
            self.assertEqual(mock.call_count, 1)

    def test126(self):
        with patch.object(ValuesValidator, 'print_missing_required_value_warning') as mock:
            self.run_test(metadata_url='test126-metadata.json', result_file='test126.ttl')
            self.assertEqual(mock.call_count, 1)

    def test127(self):
        with patch.object(MetadataValidator, 'print_incompatibility_warning') as mock:
            self.run_test(metadata_url='test127-metadata.json', result_file='test127.ttl')
            self.assertEqual(mock.call_count, 1)

    def test129(self):
        with patch.object(MetadataValidator, 'print_field_type_warning') as mock:
            self.run_test(metadata_url='test129-metadata.json', result_file='test129.ttl')
            self.assertEqual(mock.call_count, 5)

    def test130(self):
        with patch.object(MetadataValidator, 'print_value_constraint_warning') as mock:
            self.run_test(metadata_url='test130-metadata.json', result_file='test130.ttl')
            self.assertEqual(mock.call_count, 5)

    def test131(self):
        with patch.object(MetadataValidator, 'print_value_constraint_warning') as mock:
            self.run_test(metadata_url='test131-metadata.json', result_file='test131.ttl')
            self.assertEqual(mock.call_count, 5)

    def test132(self):
        self.run_test(metadata_url='test132-metadata.json', result_file='test132.ttl')

    def test147(self):
        with patch.object(MetadataValidator, 'print_incompatibility_warning') as mock:
            self.run_test(metadata_url='test147-metadata.json', result_file='test147.ttl')
            self.assertEqual(mock.call_count, 5)

    def test148(self):
        with patch.object(MetadataValidator, 'print_no_matching_title_lang_found_warning') as mock:
            self.run_test(metadata_url='test148-metadata.json', result_file='test148.ttl')
            self.assertEqual(mock.call_count, 1)

    def test0149(self):
        self.run_test(metadata_url='test149-metadata.json', result_file='test149.ttl')

    def test150(self):
        with patch.object(MetadataValidator, 'print_value_warning') as mock:
            self.run_test(metadata_url='test150-metadata.json', result_file='test150.ttl')
            self.assertEqual(mock.call_count, 1)

    def test151(self):
        with patch.object(MetadataValidator, 'print_value_warning') as mock:
            self.run_test(metadata_url='test151-metadata.json', result_file='test151.ttl')
            self.assertEqual(mock.call_count, 1)

    def test152(self):
        self.run_test(metadata_url='test152-metadata.json', result_file='test152.ttl')

    def test153(self):
        with patch.object(ValuesValidator, 'print_bad_regex_warning') as mock:
            self.run_test(metadata_url='test153-metadata.json', result_file='test153.ttl')
            self.assertEqual(mock.call_count, 1)

    def test154(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test154-metadata.json', result_file='test154.ttl')
            self.assertEqual(mock.call_count, 1)

    def test158(self):
        self.run_test(metadata_url='test158-metadata.json', result_file='test158.ttl')

    def test168(self):
        self.run_test(metadata_url='test168-metadata.json', result_file='test168.ttl')

    def test170(self):
        self.run_test(metadata_url='test170-metadata.json', result_file='test170.ttl')

    def test171(self):
        self.run_test(metadata_url='test171-metadata.json', result_file='test171.ttl')

    def test172(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test172-metadata.json', result_file='test172.ttl')
            self.assertEqual(mock.call_count, 1)

    def test173(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test173-metadata.json', result_file='test173.ttl')
            self.assertEqual(mock.call_count, 1)

    def test174(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test174-metadata.json', result_file='test174.ttl')
            self.assertEqual(mock.call_count, 1)

    def test175(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test175-metadata.json', result_file='test175.ttl')
            self.assertEqual(mock.call_count, 1)

    def test176(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test176-metadata.json', result_file='test176.ttl')
            self.assertEqual(mock.call_count, 1)

    def test177(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test177-metadata.json', result_file='test177.ttl')
            self.assertEqual(mock.call_count, 1)

    def test178(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test178-metadata.json', result_file='test178.ttl')
            self.assertEqual(mock.call_count, 1)

    def test179(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test179-metadata.json', result_file='test179.ttl')
            self.assertEqual(mock.call_count, 1)

    def test180(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test180-metadata.json', result_file='test180.ttl')
            self.assertEqual(mock.call_count, 1)

    def test181(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test181-metadata.json', result_file='test181.ttl')
            self.assertEqual(mock.call_count, 1)

    def test182(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test182-metadata.json', result_file='test182.ttl')
            self.assertEqual(mock.call_count, 1)

    def test183(self):
        self.run_test(metadata_url='test183-metadata.json', result_file='test183.ttl')

    def test184(self):
        with patch.object(MetadataValidator, 'print_bad_datatype_format_warning') as mock:
            self.run_test(metadata_url='test184-metadata.json', result_file='test184.ttl')
            self.assertEqual(mock.call_count, 1)

    def test185(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test185-metadata.json', result_file='test185.ttl')
            self.assertEqual(mock.call_count, 1)

    def test187(self):
        self.run_test(metadata_url='test187-metadata.json', result_file='test187.ttl')

    def test188(self):
        self.run_test(metadata_url='test188-metadata.json', result_file='test188.ttl')

    def test189(self):
        self.run_test(metadata_url='test189-metadata.json', result_file='test189.ttl')

    def test190(self):
        self.run_test(metadata_url='test190-metadata.json', result_file='test190.ttl')

    def test193(self):
        self.run_test(metadata_url='test193-metadata.json', result_file='test193.ttl')

    def test194(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test194-metadata.json', result_file='test194.ttl')
            self.assertEqual(mock.call_count, 27)

    def test195(self):
        self.run_test(metadata_url='test195-metadata.json', result_file='test195.ttl')

    def test196(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test196-metadata.json', result_file='test196.ttl')
            self.assertEqual(mock.call_count, 1)

    def test197(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test197-metadata.json', result_file='test197.ttl')
            self.assertEqual(mock.call_count, 1)

    def test198(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test198-metadata.json', result_file='test198.ttl')
            self.assertEqual(mock.call_count, 1)

    def test202(self):
        self.run_test(metadata_url='test202-metadata.json', result_file='test202.ttl')

    def test203(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test203-metadata.json', result_file='test203.ttl')
            self.assertEqual(mock.call_count, 1)

    def test204(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test204-metadata.json', result_file='test204.ttl')
            self.assertEqual(mock.call_count, 1)

    def test205(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test205-metadata.json', result_file='test205.ttl')
            self.assertEqual(mock.call_count, 1)

    def test206(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test206-metadata.json', result_file='test206.ttl')
            self.assertEqual(mock.call_count, 1)

    def test207(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test207-metadata.json', result_file='test207.ttl')
            self.assertEqual(mock.call_count, 1)

    def test208(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test208-metadata.json', result_file='test208.ttl')
            self.assertEqual(mock.call_count, 1)

    def test209(self):
        self.run_test(metadata_url='test209-metadata.json', result_file='test209.ttl')

    def test210(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test210-metadata.json', result_file='test210.ttl')
            self.assertEqual(mock.call_count, 1)

    def test211(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test211-metadata.json', result_file='test211.ttl')
            self.assertEqual(mock.call_count, 1)

    def test212(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test212-metadata.json', result_file='test212.ttl')
            self.assertEqual(mock.call_count, 1)

    def test213(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test213-metadata.json', result_file='test213.ttl')
            self.assertEqual(mock.call_count, 1)

    def test214(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test214-metadata.json', result_file='test214.ttl')
            self.assertEqual(mock.call_count, 1)

    def test215(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test215-metadata.json', result_file='test215.ttl')
            self.assertEqual(mock.call_count, 1)

    def test228(self):
        self.run_test(metadata_url='test228-metadata.json', result_file='test228.ttl')

    def test229(self):
        self.run_test(metadata_url='test229-metadata.json', result_file='test229.ttl')

    def test230(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test230-metadata.json', result_file='test230.ttl')
            self.assertEqual(mock.call_count, 1)

    def test231(self):
        self.run_test(metadata_url='test231-metadata.json', result_file='test231.ttl')

    def test232(self):
        self.run_test(metadata_url='test232-metadata.json', result_file='test232.ttl')

    def test233(self):
        self.run_test(metadata_url='test233-metadata.json', result_file='test233.ttl')

    def test234(self):
        self.run_test(metadata_url='test234-metadata.json', result_file='test234.ttl')

    def test235(self):
        self.run_test(metadata_url='test235-metadata.json', result_file='test235.ttl')

    def test236(self):
        self.run_test(metadata_url='test236-metadata.json', result_file='test236.ttl')

    def test237(self):
        self.run_test(metadata_url='test237-metadata.json', result_file='test237.ttl', mode=CONST_MINIMAL_MODE)

    def test238(self):
        with patch.object(MetadataValidator, 'print_value_warning') as mock:
            self.run_test(metadata_url='test238-metadata.json', result_file='test238.ttl')
            self.assertEqual(mock.call_count, 1)

    def test242(self):
        self.run_test(metadata_url='test242-metadata.json', result_file='test242.ttl')

    def test245(self):
        self.run_test(metadata_url='test245-metadata.json', result_file='test245.ttl')

    def test246(self):
        self.run_test(metadata_url='test246-metadata.json', result_file='test246.ttl')

    def test248(self):
        self.run_test(metadata_url='test248-metadata.json', result_file='test248.ttl')

    def test259(self):
        self.run_test('test259/tree-ops.csv', 'test259/result.ttl')

    def test260(self):
        self.run_test('test260/tree-ops.csv', 'test260/result.ttl')

    def test263(self):
        self.run_test(metadata_url='test263-metadata.json', result_file='test263.ttl')

    def test264(self):
        self.run_test(metadata_url='test264-metadata.json', result_file='test264.ttl')

    def test266(self):
        with patch.object(MetadataValidator, 'print_bad_array_item_type_warning') as mock:
            self.run_test(metadata_url='test266-metadata.json', result_file='test266.ttl')
            self.assertEqual(mock.call_count, 1)

    def test268(self):
        self.run_test(metadata_url='test268-metadata.json', result_file='test268.ttl')

    def test269(self):
        with patch.object(MetadataValidator, 'print_bad_datatype_format_warning') as mock:
            self.run_test(metadata_url='test269-metadata.json', result_file='test269.ttl')
            self.assertEqual(mock.call_count, 1)

    def test270(self):
        with patch.object(MetadataValidator, 'print_invalid_member_property') as mock:
            self.run_test(metadata_url='test270-metadata.json', result_file='test270.ttl')
            self.assertEqual(mock.call_count, 1)

    def test273(self):
        self.run_test(metadata_url='test273-metadata.json', result_file='test273.ttl')

    def test275(self):
        with patch.object(MetadataValidator, 'print_invalid_member_property') as mock:
            self.run_test(metadata_url='test275-metadata.json', result_file='test275.ttl')
            self.assertEqual(mock.call_count, 1)

    def test276(self):
        with patch.object(MetadataValidator, 'print_invalid_member_property') as mock:
            self.run_test(metadata_url='test276-metadata.json', result_file='test276.ttl')
            self.assertEqual(mock.call_count, 1)

    def test277(self):
        with patch.object(MetadataValidator, 'print_invalid_member_property') as mock:
            self.run_test(metadata_url='test277-metadata.json', result_file='test277.ttl')
            self.assertEqual(mock.call_count, 1)

    def test278(self):
        with patch.object(MetadataValidator, 'print_column_count_mismatch_warning') as mock:
            self.run_test(metadata_url='test278-metadata.json', result_file='test278.ttl')
            self.assertEqual(mock.call_count, 1)

    def test279(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test279-metadata.json', result_file='test279.ttl')
            self.assertEqual(mock.call_count, 1)

    def test280(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test280-metadata.json', result_file='test280.ttl')
            self.assertEqual(mock.call_count, 1)

    def test281(self):
        with patch.object(ValuesValidator, 'print_type_value_incompatibility_warning') as mock:
            self.run_test(metadata_url='test281-metadata.json', result_file='test281.ttl')
            self.assertEqual(mock.call_count, 1)

    def test285(self):
        self.run_test(metadata_url='test285-metadata.json', result_file='test285.ttl')

    def test305(self):
        self.run_test(metadata_url='test305-metadata.json', result_file='test305.ttl')

    def test306(self):
        self.run_test(metadata_url='test306-metadata.json', result_file='test306.ttl')

    def test307(self):
        self.run_test(metadata_url='test307-metadata.json', result_file='test307.ttl')


if __name__ == '__main__':
    unittest.main()
