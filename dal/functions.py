import pandas as pd
import runner.calendar as cal

def get_company_list():
    df = pd.read_csv('data/data_new_list_wikipedia.csv', header=[0, 1], index_col=0, dayfirst=True, parse_dates=True)
    companies = df.columns.get_level_values(0).to_list()

    return list(dict.fromkeys(companies))


def get_prices(list_of_tickers):
    df = pd.read_csv('data/data_new_list_wikipedia.csv', header=[0, 1], index_col=0, dayfirst=True, parse_dates=True)
    df = df[list_of_tickers]
    datetime = cal.Calendar()

    return df.iloc[:, ::2].loc[:datetime.get_current_time().strftime("%Y%m%d")]


def get_volumes(list_of_tickers):
    df = pd.read_csv('data/data_new_list_wikipedia.csv', header=[0, 1], index_col=0, dayfirst=True, parse_dates=True)
    df = df[list_of_tickers]
    datetime = cal.Calendar()

    return df.iloc[:, 1::2].loc[:datetime.get_current_time().strftime("%Y%m%d")]


def get_volatilities(data, days):

    return data.rolling(days).std()

def get_moving_average(data, days):

    return data.rolling(days).mean()

def get_macd(data):
    exp1 = data.ewm(span=12, adjust=False).mean()
    exp2 = data.ewm(span=26, adjust=False).mean()
    macd = exp1-exp2

    return macd

def get_macd_signal_line(data):
    exp1 = data.ewm(span=12, adjust=False).mean()
    exp2 = data.ewm(span=26, adjust=False).mean()
    macd = exp1-exp2
    exp3 = macd.ewm(span=9, adjust=False).mean()

    return exp3