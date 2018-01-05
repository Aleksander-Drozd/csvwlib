import json as jsonlib

import requests

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
            return jsonlib.loads(requests.get(metadata_url).content.decode())

        metadata = MetadataLocator._retrieve_from_site_wide_conf(csv_url)
        if metadata is not None:
            return metadata

        metadata_url = csv_url + '-metadata.json'
        response = requests.get(metadata_url)

        if response.status_code == 404:
            metadata_url = csv_url.rsplit('/', 1)[0] + '/csv-metadata.json'
            response = requests.get(metadata_url)

        return None if response.status_code == 404 else jsonlib.loads(response.content.decode())

    @staticmethod
    def _retrieve_from_site_wide_conf(csv_url):
        site_wide_conf_file = '/'.join(csv_url.split('/')[:3]) + '/.well-known/csvm'
        response = requests.get(site_wide_conf_file)

        if response.status_code == 404:
            return None

        lines = response.content.decode().splitlines()
        for relative_uri_template in lines:
            if relative_uri_template == '':
                continue
            metadata_url = WellKnownUriResolver.resolve(relative_uri_template, csv_url)
            response = requests.get(metadata_url)
            if response.status_code != 404:
                return jsonlib.loads(response.content.decode())
