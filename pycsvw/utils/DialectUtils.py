class DialectUtils:

    @staticmethod
    def get_default():
        return {
            "commentPrefix": None,
            "delimiter": ",",
            "doubleQuote": True,
            "encoding": "utf-8",
            "header": True,
            "headerRowCount": 1,
            "lineTerminators": ["\r\n", "\n"],
            "quoteChar": "\"",
            "skipBlankRows": False,
            "skipColumns": 0,
            "skipInitialSpace": False,
            "skipRows": 0,
            "trim": True,
            "@type": "Dialect"
        }
