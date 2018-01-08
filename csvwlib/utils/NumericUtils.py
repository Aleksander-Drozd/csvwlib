class NumericUtils:

    _supported_special_signs = ['%', '‰']

    @staticmethod
    def interpret_special_signs(number):
        """ supported signs: %, ‰ """
        if number[0] in NumericUtils._supported_special_signs:
            character = number[0]
            number = number[1:]
        elif number[-1] in NumericUtils._supported_special_signs:
            character = number[-1]
            number = number[:-1]
        else:
            return number

        if character == '%':
            return NumericUtils.shift_decimal_separator(number, 2)
        elif character == '‰':
            return NumericUtils.shift_decimal_separator(number, 3)
        return number

    @staticmethod
    def shift_decimal_separator(number, shift):
        if '.' in number:
            decimal_separator_index = number.index('.')
            number = number.replace('.', '')
            number = number[:decimal_separator_index - shift] + '.' + number[decimal_separator_index - shift:]
        else:
            number = number[:-shift] + '.' + number[-shift:]

        return number

    @staticmethod
    def is_numeric(number):
        if type(number) is not str:
            return True
        number = number.replace('.', '', 1)
        number = number.replace('+', '', 1)
        number = number.replace('-', '', 1)
        number = number.replace('E', '', 1)
        number = number.replace('%', '', 1)
        number = number.replace('‰', '', 1)
        return number.isnumeric()
