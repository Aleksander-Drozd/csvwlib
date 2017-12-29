import json
import time
import unittest

from pipenv.utils import requests

from pycsvw.converter.ModelConverter import convert_from_url


class TestModelConverter(unittest.TestCase):
    __testsLocation = 'http://www.w3.org/2013/csvw/tests/'

    def compareDictsAsJSONs(self, actual, expected):
        self.assertEqual(json.dumps(actual, sort_keys=True), json.dumps(expected, sort_keys=True))

    def run_test_for_file(self, tested_file):
        converted = convert_from_url(self.__testsLocation + tested_file + '.csv')
        expected = requests.get(self.__testsLocation + tested_file + '.json').content
        expected_decoded = json.loads(expected)
        self.compareDictsAsJSONs(converted, expected_decoded)

    def test_test002(self):
        self.run_test_for_file('test002')

    def test_test003(self):
        time.sleep(0.2)
        self.run_test_for_file('test003')
        

if __name__ == '__main__':
    unittest.main()
