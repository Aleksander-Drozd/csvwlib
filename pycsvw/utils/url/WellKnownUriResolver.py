import uritemplate


class WellKnownUriResolver:

    @staticmethod
    def resolve(template, csv_url):
        if template[0].isalpha():
            domain = csv_url.rsplit('/', 1)[0] + '/'
            uri_template = domain + template
        elif template[0] == '/':
            domain = '/'.join(csv_url.split('/')[:3])
            uri_template = domain + template
        else:
            uri_template = template

        return uritemplate.expand(uri_template, {'url': csv_url})
