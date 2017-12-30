import unittest
from unittest import TestCase, mock
from unittest.mock import patch

from rdflib import Graph
from rdflib.compare import to_isomorphic

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
        self.assertEqual(to_isomorphic(converted), to_isomorphic(expected))

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

    def test118(self):
        self.run_test('test011/tree-ops.csv', 'test011/result.ttl')

    def test121(self):
        self.run_test('test121', 'test121.ttl', 'test121-user-metadata.json')

    def test124(self):
        self.run_test('tree-ops.csv', 'test124.ttl',  'test124-user-metadata.json')

    def test132(self):
        self.run_test(metadata_url='test132-metadata.json', result_file='test132.ttl')

    def test0149(self):
        self.run_test(metadata_url='test149-metadata.json', result_file='test149.ttl')

    def test152(self):
        self.run_test(metadata_url='test152-metadata.json', result_file='test152.ttl')

    def test158(self):
        self.run_test(metadata_url='test158-metadata.json', result_file='test158.ttl')

    def test168(self):
        self.run_test(metadata_url='test168-metadata.json', result_file='test168.ttl')

    def test170(self):
        self.run_test(metadata_url='test170-metadata.json', result_file='test170.ttl')

    def test171(self):
        self.run_test(metadata_url='test171-metadata.json', result_file='test171.ttl')

    def test183(self):
        self.run_test(metadata_url='test183-metadata.json', result_file='test183.ttl')

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

    def test195(self):
        self.run_test(metadata_url='test195-metadata.json', result_file='test195.ttl')

    def test202(self):
        self.run_test(metadata_url='test202-metadata.json', result_file='test202.ttl')

    def test209(self):
        self.run_test(metadata_url='test209-metadata.json', result_file='test209.ttl')

    def test228(self):
        self.run_test(metadata_url='test228-metadata.json', result_file='test228.ttl')

    def test229(self):
        self.run_test(metadata_url='test229-metadata.json', result_file='test229.ttl')

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
        TestToRDFConverter._tests_location = TestToRDFConverter._remote_tests_location
        self.run_test(metadata_url='test263-metadata.json', result_file='test263.ttl')
        TestToRDFConverter._tests_location = TestToRDFConverter._local_tests_location

    def test264(self):
        TestToRDFConverter._tests_location = TestToRDFConverter._remote_tests_location
        self.run_test(metadata_url='test264-metadata.json', result_file='test264.ttl')
        TestToRDFConverter._tests_location = TestToRDFConverter._local_tests_location

    def test268(self):
        TestToRDFConverter._tests_location = TestToRDFConverter._remote_tests_location
        self.run_test(metadata_url='test268-metadata.json', result_file='test268.ttl')
        TestToRDFConverter._tests_location = TestToRDFConverter._local_tests_location

    def test273(self):
        TestToRDFConverter._tests_location = TestToRDFConverter._remote_tests_location
        self.run_test(metadata_url='test273-metadata.json', result_file='test273.ttl')
        TestToRDFConverter._tests_location = TestToRDFConverter._local_tests_location

    def test285(self):
        TestToRDFConverter._tests_location = TestToRDFConverter._remote_tests_location
        self.run_test(metadata_url='test285-metadata.json', result_file='test285.ttl')
        TestToRDFConverter._tests_location = TestToRDFConverter._local_tests_location

    def test305(self):
        self.run_test(metadata_url='test305-metadata.json', result_file='test305.ttl')

    def test306(self):
        self.run_test(metadata_url='test306-metadata.json', result_file='test306.ttl')

    def test307(self):
        self.run_test(metadata_url='test307-metadata.json', result_file='test307.ttl')


if __name__ == '__main__':
    unittest.main()
