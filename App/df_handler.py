from .utils import read_xls


class DFHandler:

    ALLOWED_OPERATIONS = ["C", "V"]

    def __init__(self, file_path="CEINNReader/data/InfoCEI_2019.xls"):
        self._file_path = file_path
        self._df = read_xls(file_path)

        self._date_col = self._df.columns[0]
        self._type_col = self._df.columns[1]
        self._stock_col = self._df.columns[2]
        self._quantity_col = self._df.columns[3]
        self._price_col = self._df.columns[4]
        self._total_price_col = self._df.columns[5]

    @property
    def date_columns(self):
        return self._date_col

    @property
    def type_col(self):
        return self._type_col

    @property
    def stock_col(self):
        return self._stock_col

    @property
    def quantity_col(self):
        return self._quantity_col

    @property
    def price_col(self):
        return self._price_col

    @property
    def total_price_col(self):
        return self._total_price_col

    def get_years(self):
        """
        Get all years listed in CeiReport
        :return a set of all unique years traded during the period
        """
        return list(set(self._df['Year']))

    def get_months(self, year=""):
        """
        Get all months listed in CeiReport
        :return a set of all unique months traded during the period
        """
        df = self._df.copy()
        if year:
            df = df[df['Year'].eq(year)]
        return list(set(self._df['Month']))

    def get_stocks(self, month="", year=""):
        """
        Get all stocks listed in CeiReport by month or year
        :return a set of all unique stocks traded during the period
        """
        df = self._df.copy()
        if year:
            df = df[df['Year'].eq(year)]
        if month:
            df = df[df['Month'].eq(month)]

        return list(set(df['Código']))

    def filter_operations(self, stock="", month="", year="", typecv=""):
        """
        Returns a dataframe containing all operations resultant from the filtered dataframe
        """
        df = self._df.copy()

        if year:
            df = df[df['Year'].eq(year)]
        if month:
            df = df[df['Month'].eq(month)]
        if stock:
            df = df[df[self._stock_col].eq(stock)]
        if typecv:
            if typecv in self.ALLOWED_OPERATIONS:
                df = df[df[self._type_col].eq(typecv)]
        return df
