class AboutUrlUtils:

    @staticmethod
    def prefix(about_url, csv_url):
        if about_url.startswith('http'):
            column = about_url[about_url.find('{') + 1:about_url.find('}')]
            if column.startswith('#'):
                about_url = about_url[:about_url.find('#') + 1]
                return about_url.replace('{', '')
            else:
                if '#' in about_url:
                    return about_url[:about_url.find('#')]
                else:
                    return about_url[:about_url.rfind('/') + 1]
        else:
            return csv_url + about_url[:about_url.find('{')]

    @staticmethod
    def column_name(about_url):
        column = about_url[about_url.find('{') + 1:about_url.find('}')]
        if column.startswith('#'):
            return column[1:]
        else:
            return column
