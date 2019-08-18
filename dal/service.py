import pandas as pd

import runner.calendar as cal


class DalService:
    class __DalService:
        def __init__(self):
            self.calendar = cal.Calendar()
            self.df = pd.read_csv('data/data_new_list_wikipedia.csv', header=[0, 1], index_col=0, dayfirst=True,
                                  parse_dates=True)

        def get_company_list(self):
            df = self.df.dropna(axis=1)
            companies = df.columns.get_level_values(0).to_list()
            return list(dict.fromkeys(companies))

        def get_working_days(self, year):
            return [item.strftime('%Y%m%d') for item in self.df.loc[str(year)].index.to_list()]

        def get_prices(self, tickers):
            return self.df[tickers].iloc[:, ::2].loc[:self.calendar.get_current_time().strftime("%Y%m%d")]

        def get_volumes(self, tickers):
            return self.df[tickers].iloc[:, 1::2].loc[:self.calendar.get_current_time().strftime("%Y%m%d")]

        def get_price_stock(self, sym, date):
            return self.get_prices(sym).loc[date.strftime('%Y%m%d')].values[0]

    instance = None

    def __init__(self):
        if not DalService.instance:
            DalService.instance = DalService.__DalService()

    @staticmethod
    def get_company_list():
        return DalService.instance.get_company_list()

    @staticmethod
    def get_working_days(year):
        return DalService.instance.get_working_days(year)

    @staticmethod
    def get_prices(tickers):
        return DalService.instance.get_prices(tickers)

    @staticmethod
    def get_volumes(tickers):
        return DalService.instance.get_volumes(tickers)

    @staticmethod
    def get_price_stock(sym, date):
        return DalService.instance.get_price_stock(sym, date)
