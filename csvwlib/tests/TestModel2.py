import json
import unittest

from csvwlib.converter.ModelConverter2 import ModelConverter2


class TestModelConverter(unittest.TestCase):
    __tests_location = 'http://localhost/tests/'

    def compareDictsAsJSONs(self, actual, expected):
        self.assertEqual(json.dumps(actual, sort_keys=True), json.dumps(expected, sort_keys=True))

    def run_test_for_file(self, tested_file):
        converted = ModelConverter2(self.__tests_location + tested_file + '.csv').convert()
        # expected = requests.get(self.__testsLocation + tested_file + '.json').content
        # expected_decoded = json.loads(expected)
        # self.compareDictsAsJSONs(converted, expected_decoded)
        print(json.dumps(converted, indent=4))

    def test001(self):
        self.run_test_for_file('test002')


if __name__ == '__main__':
    unittest.main()
