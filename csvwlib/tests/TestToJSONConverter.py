import json as jsonlib
import unittest
from unittest import mock
from unittest.mock import patch

import requests

from csvwlib.utils.rdf.CSVW import CONST_STANDARD_MODE, CONST_MINIMAL_MODE
from csvwlib.converter.CSVWConverter import CSVWConverter
from csvwlib.utils.MetadataLocator import MetadataLocator


class TestToJSONConverter(unittest.TestCase):

    _remote_tests_location = 'http://www.w3.org/2013/csvw/tests/'
    _local_tests_location = 'http://localhost/tests/'
    _tests_location = _local_tests_location

    def compare_dicts(self, dict1, dict2):
        self.assertEqual(jsonlib.dumps(dict1, sort_keys=True), jsonlib.dumps(dict2, sort_keys=True))

    def run_test(self, tested_file=None, result_file=None, metadata_url=None, mode=CONST_STANDARD_MODE):
        result_url = self._tests_location + result_file
        metadata_url = self._tests_location + metadata_url if metadata_url is not None else None
        csv_url = self._tests_location + tested_file if tested_file is not None else None
        metadata = MetadataLocator.find_and_get(csv_url, metadata_url)
        csv_url_sufix = csv_url.rsplit('/', 1)[0] + '/' if csv_url is not None else self._tests_location
        self._prepare_metadata_for_test(csv_url, metadata_url, csv_url_sufix, metadata)
        with patch('csvwlib.converter.ModelConverter.MetadataLocator.find_and_get') as _mock:
            _mock.return_value = metadata
            converted = CSVWConverter.to_json(csv_url, metadata_url, mode)
        expected = jsonlib.loads(requests.get(result_url).content)
        self.change_urls_in_result(expected)
        self.compare_dicts(converted, expected)

    def _prepare_metadata_for_test(self, csv_url, metadata_url, dir_path, metadata):
        if csv_url is None:
            sufix = dir_path + metadata_url.replace(self._tests_location, '')
            dir_path = sufix.rsplit('/', 1)[0] + '/'
        if metadata is not None:
            for table in metadata.get('tables', []):
                if 'url' in table and not table['url'].startswith('http'):
                    table['url'] = dir_path + table['url']
            if 'url' in metadata and not metadata['url'].startswith('http'):
                metadata['url'] = dir_path + metadata['url']

    @staticmethod
    def change_urls_in_result(json):
        if type(json) is dict:
            for key, value in list(json.items()):
                if key.startswith(TestToJSONConverter._remote_tests_location):
                    copy = json[key]
                    del json[key]
                    key = key.replace(TestToJSONConverter._remote_tests_location,
                                      TestToJSONConverter._tests_location)
                    json[key] = copy
                if type(value) is dict:
                    TestToJSONConverter.change_urls_in_result(value)
                elif type(value) is list:
                    for item in value:
                        TestToJSONConverter.change_urls_in_result(item)
                elif type(value) is str:
                    if key == 'url' or key == '@id':
                        json[key] = value.replace(TestToJSONConverter._remote_tests_location,
                                                  TestToJSONConverter._tests_location)
                    elif value.startswith(TestToJSONConverter._remote_tests_location):
                        json[key] = value.replace(TestToJSONConverter._remote_tests_location,
                                                  TestToJSONConverter._tests_location)
        elif type(json) is list:
            for item in json:
                TestToJSONConverter.change_urls_in_result(item)

    def test001(self):
        self.run_test('test001.csv', 'test001.json')

    def test005(self):
        self.run_test('test005.csv', 'test005.json')

    def test006(self):
        self.run_test('test006.csv', 'test006.json')

    def test007(self):
        self.run_test('test007.csv', 'test007.json')

    def test008(self):
        self.run_test('test008.csv', 'test008.json')

    def test009(self):
        self.run_test('test009.csv', 'test009.json')

    def test010(self):
        self.run_test('test010.csv', 'test010.json')

    def test011(self):
        self.run_test('test011/tree-ops.csv', 'test011/result.json')

    def test012(self):
        self.run_test('test012/tree-ops.csv', 'test012/result.json')

    def test013(self):
        self.run_test('tree-ops.csv', 'test013.json', metadata_url='test013-user-metadata.json')

    @mock.patch('csvwlib.utils.MetadataLocator.requests.head')
    def test014(self, head_mock):
        head_mock.return_value.headers = {'Link': ''}
        head_mock.return_value.links = {'describedby': {'url': 'linked-metadata.json'}}
        self.run_test('test014/tree-ops.csv', 'test014/result.json')

    def test015(self):
        self.run_test('test015/tree-ops.csv', 'test015/result.json', 'test015/user-metadata.json')

    @mock.patch('csvwlib.utils.MetadataLocator.requests.head')
    def test016(self, head_mock):
        head_mock.return_value.headers = {'Link': ''}
        head_mock.return_value.links = {'describedby': {'url': 'linked-metadata.json'}}
        self.run_test('test016/tree-ops.csv', 'test016/result.json')

    def test017(self):
        self.run_test('test017/tree-ops.csv', 'test017/result.json')

    def test018(self):
        self.run_test('test018/tree-ops.csv', 'test018/result.json', 'test018/user-metadata.json')

    def test023(self):
        self.run_test('tree-ops.csv', 'test023.json', 'test023-user-metadata.json')

    def test027(self):
        self.run_test('tree-ops.csv', 'test027.json', 'test027-user-metadata.json', CONST_MINIMAL_MODE)

    def test028(self):
        self.run_test('countries.csv', 'test028.json')

    def test029(self):
        self.run_test('countries.csv', 'test029.json', mode=CONST_MINIMAL_MODE)

    def test030(self):
        self.run_test(result_file='test030.json', metadata_url='countries.json')

    def test031(self):
        self.run_test(result_file='test031.json', metadata_url='countries.json', mode=CONST_MINIMAL_MODE)

    def test032(self):
        self.run_test(result_file='test032/result.json', metadata_url='test032/csv-metadata.json')

    def test033(self):
        self.run_test(result_file='test033/result.json', metadata_url='test033/csv-metadata.json',
                      mode=CONST_MINIMAL_MODE)

    def test036(self):
        self.run_test('test036/tree-ops-ext.csv', 'test036/result.json')

    def test037(self):
        self.run_test('test037/tree-ops-ext.csv', 'test037/result.json', mode=CONST_MINIMAL_MODE)

    def test038(self):
        self.run_test(metadata_url='test038-metadata.json', result_file='test038.json')

    def test039(self):
        self.run_test(metadata_url='test039-metadata.json', result_file='test039.json')

    def test118(self):
        self.run_test('test011/tree-ops.csv', 'test011/result.json')

    def test121(self):
        self.run_test('test121', 'test121.json', 'test121-user-metadata.json')

    def test124(self):
        self.run_test('tree-ops.csv', 'test124.json',  'test124-user-metadata.json')

    def test132(self):
        self.run_test(metadata_url='test132-metadata.json', result_file='test132.json')

    def test0149(self):
        self.run_test(metadata_url='test149-metadata.json', result_file='test149.json')

    def test152(self):
        self.run_test(metadata_url='test152-metadata.json', result_file='test152.json')

    def test158(self):
        self.run_test(metadata_url='test158-metadata.json', result_file='test158.json')

    def test168(self):
        self.run_test(metadata_url='test168-metadata.json', result_file='test168.json')

    def test170(self):
        self.run_test(metadata_url='test170-metadata.json', result_file='test170.json')

    def test171(self):
        self.run_test(metadata_url='test171-metadata.json', result_file='test171.json')

    def test183(self):
        self.run_test(metadata_url='test183-metadata.json', result_file='test183.json')

    def test187(self):
        self.run_test(metadata_url='test187-metadata.json', result_file='test187.json')

    def test188(self):
        self.run_test(metadata_url='test188-metadata.json', result_file='test188.json')

    def test189(self):
        self.run_test(metadata_url='test189-metadata.json', result_file='test189.json')

    def test190(self):
        self.run_test(metadata_url='test190-metadata.json', result_file='test190.json')

    def test193(self):
        self.run_test(metadata_url='test193-metadata.json', result_file='test193.json')

    def test195(self):
        self.run_test(metadata_url='test195-metadata.json', result_file='test195.json')

    def test202(self):
        self.run_test(metadata_url='test202-metadata.json', result_file='test202.json')

    def test209(self):
        self.run_test(metadata_url='test209-metadata.json', result_file='test209.json')

    def test228(self):
        self.run_test(metadata_url='test228-metadata.json', result_file='test228.json')

    def test229(self):
        self.run_test(metadata_url='test229-metadata.json', result_file='test229.json')

    def test231(self):
        self.run_test(metadata_url='test231-metadata.json', result_file='test231.json')

    def test232(self):
        self.run_test(metadata_url='test232-metadata.json', result_file='test232.json')

    def test233(self):
        self.run_test(metadata_url='test233-metadata.json', result_file='test233.json')

    def test234(self):
        self.run_test(metadata_url='test234-metadata.json', result_file='test234.json')

    def test235(self):
        self.run_test(metadata_url='test235-metadata.json', result_file='test235.json')

    def test236(self):
        self.run_test(metadata_url='test236-metadata.json', result_file='test236.json')

    def test237(self):
        self.run_test(metadata_url='test237-metadata.json', result_file='test237.json', mode=CONST_MINIMAL_MODE)

    def test242(self):
        self.run_test(metadata_url='test242-metadata.json', result_file='test242.json')

    def test245(self):
        self.run_test(metadata_url='test245-metadata.json', result_file='test245.json')

    def test246(self):
        self.run_test(metadata_url='test246-metadata.json', result_file='test246.json')

    def test248(self):
        self.run_test(metadata_url='test248-metadata.json', result_file='test248.json')

    def test259(self):
        self.run_test('test259/tree-ops.csv', 'test259/result.json')

    def test260(self):
        self.run_test('test260/tree-ops.csv', 'test260/result.json')

    def test263(self):
        self.run_test(metadata_url='test263-metadata.json', result_file='test263.json')

    def test264(self):
        self.run_test(metadata_url='test264-metadata.json', result_file='test264.json')

    def test268(self):
        self.run_test(metadata_url='test268-metadata.json', result_file='test268.json')

    def test273(self):
        self.run_test(metadata_url='test273-metadata.json', result_file='test273.json')

    def test282(self):
        self.run_test(metadata_url='test282-metadata.json', result_file='test282.json')

    def test283(self):
        self.run_test(metadata_url='test283-metadata.json', result_file='test283.json')

    def test284(self):
        self.run_test(metadata_url='test284-metadata.json', result_file='test284.json')

    def test285(self):
        self.run_test(metadata_url='test285-metadata.json', result_file='test285.json')

    def test305(self):
        self.run_test(metadata_url='test305-metadata.json', result_file='test305.json')

    def test306(self):
        self.run_test(metadata_url='test306-metadata.json', result_file='test306.json')

    def test307(self):
        self.run_test(metadata_url='test307-metadata.json', result_file='test307.json')


if __name__ == '__main__':
    unittest.main()
