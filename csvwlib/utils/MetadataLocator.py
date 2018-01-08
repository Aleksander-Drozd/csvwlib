import json as jsonlib

import requests

from csvwlib.utils.metadata import MetadataValidator
from csvwlib.utils.url.WellKnownUriResolver import WellKnownUriResolver


class MetadataLocator:

    @staticmethod
    def find_and_get(csv_url, metadata_url=None):
        if metadata_url is not None:
            return jsonlib.loads(requests.get(metadata_url).content.decode())

        response = requests.head(csv_url)
        if 'Link' in response.headers and 'describedby' in response.links:
            metadata_name = response.links['describedby']['url']
            metadata_url = csv_url.rsplit('/', 1)[0] + '/' + metadata_name
            metadata = jsonlib.loads(requests.get(metadata_url).content.decode())
            if MetadataLocator._metadata_references_valid_csv(metadata, csv_url, response):
                return metadata

        metadata = MetadataLocator._retrieve_from_site_wide_conf(csv_url)
        if metadata is not None:
            return metadata

        if '?' in csv_url:
            csv_url, query = csv_url.split('?')
            metadata_url = csv_url + '-metadata.json'
            response = requests.get(metadata_url)
            if response.status_code >= 400:
                response = requests.get(metadata_url + '?' + query)
            else:
                response.status_code = 404
        else:
            metadata_url = csv_url + '-metadata.json'
            response = requests.get(metadata_url)

        if response.status_code < 400:
            metadata = jsonlib.loads(response.content.decode())
            if MetadataLocator._metadata_references_valid_csv(metadata, csv_url, response):
                return metadata

        if response.status_code >= 400:
            metadata_url = csv_url.rsplit('/', 1)[0] + '/csv-metadata.json'
            response = requests.get(metadata_url)

        return None if response.status_code >= 400 else jsonlib.loads(response.content.decode())

    @staticmethod
    def _retrieve_from_site_wide_conf(csv_url):
        csv_url = csv_url.split('?')[0]
        site_wide_conf_file = '/'.join(csv_url.split('/')[:3]) + '/.well-known/csvm'
        response = requests.get(site_wide_conf_file)

        if response.status_code >= 400:
            return None

        lines = response.content.decode().splitlines()
        for relative_uri_template in lines:
            if relative_uri_template == '':
                continue
            metadata_url = WellKnownUriResolver.resolve(relative_uri_template, csv_url)
            response = requests.get(metadata_url)
            if response.status_code != 404:
                return jsonlib.loads(response.content.decode())

    @staticmethod
    def _first_url(metadata):
        if 'url' in metadata:
            return metadata['url']
        else:
            return metadata['tables'][0]['url']

    @staticmethod
    def _metadata_references_valid_csv(metadata, csv_url, response):
        referencing_url = MetadataLocator._first_url(metadata)
        if not csv_url.endswith(referencing_url):
            MetadataValidator.instance.print_bad_reference_warning()
            response.status_code = 404
            return False
        else:
            return True
