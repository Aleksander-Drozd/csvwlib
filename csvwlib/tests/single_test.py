import unittest
from unittest.mock import patch

from csvwlib.converter.CSVWConverter import CSVWConverter
from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff
from csvwlib.utils.MetadataLocator import MetadataLocator

from csvwlib.utils.rdf.CSVW import CONST_STANDARD_MODE


class TestModelConverter(unittest.TestCase):

    _remote_tests_location = 'http://www.w3.org/2013/csvw/tests/'
    _local_tests_location = 'http://localhost/tests/'
    _tests_location = _local_tests_location

    def dump_nt_sorted(self, g):
        for l in sorted(g.serialize(format='ttl').splitlines()):
            if l:
                print(l.decode())

    def diff(self, actual, expected):
        both, first, second = graph_diff(actual, expected)
        print('----------actual----------')
        self.dump_nt_sorted(first)
        print('----------expected----------')
        self.dump_nt_sorted(second)

    def run_test(self, tested_file=None, result_file=None, metadata_url=None, mode=CONST_STANDARD_MODE):
        result_graph_url = self._tests_location + result_file
        metadata_url = self._tests_location + metadata_url if metadata_url is not None else None
        csv_url = self._tests_location + tested_file if tested_file is not None else None
        metadata = MetadataLocator.find_and_get(csv_url, metadata_url)
        csv_url_sufix = csv_url.rsplit('/', 1)[0] + '/' if csv_url is not None else self._tests_location
        self._prepare_metadata_for_test(csv_url, metadata_url, csv_url_sufix, metadata)
        with patch('converter.ModelConverter.MetadataLocator.find_and_get') as _mock:
            _mock.return_value = metadata
            converted = CSVWConverter.to_rdf(csv_url, metadata_url, mode)
        expected = Graph()
        expected.parse(result_graph_url)
        print(expected.serialize(format='ttl').decode())
        print(converted.serialize(format='ttl').decode())
        try:
            self.assertEqual(to_isomorphic(converted), to_isomorphic(expected))
        except AssertionError:
            self.diff(to_isomorphic(converted), to_isomorphic(expected))
            raise AssertionError

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

    def test001(self):
        self.run_test('test009.csv', 'test009.ttl')


if __name__ == '__main__':
    unittest.main()
