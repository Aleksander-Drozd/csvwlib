class ATDMUtils:

    @staticmethod
    def column_value(atdm_row, column_name):
        for column, values in atdm_row['cells'].items():
            if column_name == column:
                return values[0]
