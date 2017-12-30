import io
import requests
import csv as csvlib


class CSVUtils:

    @staticmethod
    def parse_csv_from_url_to_list(csv_url, delimiter=','):
        raw_csv = requests.get(csv_url).content
        decoded = raw_csv.decode('utf-8')
        data = io.StringIO(decoded)
        return list(csvlib.reader(data, delimiter=delimiter))
