import pandas as pd
import datetime

from runner.calendar import CalendarService


class DalService:
    class __DalService:
        def __init__(self):
            self.df = pd.read_csv('data/data_new_list_wikipedia.csv', header=[0, 1], index_col=0, dayfirst=True,
                                  parse_dates=True).dropna(axis=1)

            self.dates_col = ['Q1 2017 date', 'Q2 2017 date', 'Q3 2017 date', 'Q4 2017 date', 'Q1 2018 date', 'Q2 2018 date', 'Q3 2018 date', 'Q4 2018 date']
            self.df_earnings = pd.read_csv('data/earnings_yahoo.csv', parse_dates=self.dates_col).set_index('Stock')


        def get_company_list(self):
            companies = self.df.columns.get_level_values(0).to_list()
            return list(dict.fromkeys(companies))

        def get_working_days(self, year):
            return [item.strftime('%Y%m%d') for item in self.df.loc[str(year)].index.to_list()]

        def get_prices(self, tickers):
            return self.df[tickers].iloc[:, ::2].loc[:CalendarService.get_current_time().strftime("%Y%m%d")]

        def get_volumes(self, tickers):
            return self.df[tickers].iloc[:, 1::2].loc[:CalendarService.get_current_time().strftime("%Y%m%d")]

        def get_price_stock(self, sym, date):
            return self.get_prices(sym).loc[date.strftime('%Y%m%d')].values[0]

        def get_earnings_prev(self, ticker):
            all_dates = self.df_earnings.loc[ticker, self.dates_col]
            position = all_dates.searchsorted(CalendarService.get_current_time())
            if(position == 0):
                earnings = { 'estimated' :  None,
                            'actual' : None
                            }
            else:
                earnings = { 'estimated' : self.df_earnings.iloc[self.df_earnings.index.get_loc(ticker), (position * 3) - 2],
                            'actual' : self.df_earnings.iloc[self.df_earnings.index.get_loc(ticker), (position *  3) - 1]
                            }
            return earnings

        def get_earnings_next(self, ticker):
            all_dates = self.df_earnings.loc[ticker, self.dates_col]
            position = all_dates.searchsorted(CalendarService.get_current_time())
            if(position > len(all_dates) - 1):
                earnings = { 'estimated' :  None,
                            'actual' : None
                            }
            else:
                earnings = { 'estimated': self.df_earnings.iat[self.df_earnings.index.get_loc(ticker), 1 + (position * 3)],
                            'actual': self.df_earnings.iat[self.df_earnings.index.get_loc(ticker), 2 + (position * 3)]
                            }
            return earnings

        def get_earnings_all(self,ticker):
            return self.df[ticker]
        

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

    @staticmethod
    def get_macd(data):
        exp1 = data.ewm(span=12, adjust=False).mean()
        exp2 = data.ewm(span=26, adjust=False).mean()
        return exp1 - exp2

    @staticmethod
    def get_macd_signal_line(data):
        exp1 = data.ewm(span=12, adjust=False).mean()
        exp2 = data.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        return macd.ewm(span=9, adjust=False).mean()

    @staticmethod
    def get_volatilities(data, days):
        return data.rolling(days).std()

    @staticmethod
    def get_moving_average(data, days):
        return data.rolling(days).mean()

    @staticmethod
    def get_earnings_all(ticker):
        return DalService.instance.get_earnings_all(ticker)

    @staticmethod
    def get_earnings_next(ticker):
        return DalService.instance.get_earnings_next(ticker)

    @staticmethod
    def get_earnings_prev(ticker):
        return DalService.instance.get_earnings_prev(ticker)
