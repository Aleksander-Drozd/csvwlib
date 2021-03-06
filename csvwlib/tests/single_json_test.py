import json as jsonlib
import unittest

import requests
from csvwlib.converter.CSVWConverter import CSVWConverter
from deepdiff import DeepDiff

from csvwlib.utils.rdf.CSVW import CONST_STANDARD_MODE


class TestToJSONConverter(unittest.TestCase):

    _remote_tests_location = 'http://www.w3.org/2013/csvw/tests/'
    _local_tests_location = 'http://localhost/tests/'
    _tests_location = _local_tests_location

    def compare_dicts(self, real, expected):
        print(jsonlib.dumps(expected, sort_keys=True, indent=4))
        print('-------real---------')
        print(jsonlib.dumps(real, sort_keys=True, indent=4))
        print(DeepDiff(real, expected))
        self.maxDiff = None
        self.assertEqual(jsonlib.dumps(real, sort_keys=True), jsonlib.dumps(expected, sort_keys=True))

    def run_test(self, tested_file=None, result_file=None, metadata_url=None, mode=CONST_STANDARD_MODE):
        result_url = self._tests_location + result_file
        metadata_url = self._tests_location + metadata_url if metadata_url is not None else None
        csv_url = self._tests_location + tested_file if tested_file is not None else None
        converted = CSVWConverter.to_json(csv_url, metadata_url, mode)
        expected = jsonlib.loads(requests.get(result_url).content)
        self.change_urls_in_result(expected)
        self.compare_dicts(converted, expected)

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
        self.run_test('test005.csv', 'test005.json')


if __name__ == '__main__':
    unittest.main()
