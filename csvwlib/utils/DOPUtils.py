class DOPUtils:
    """ Description Object Property Utils
    https://www.w3.org/TR/tabular-metadata/#h-property-syntax """

    @staticmethod
    def natural_language_first_value(property_value):
        if type(property_value) is str:
            return property_value
        elif type(property_value) is list:
            return property_value[0]
