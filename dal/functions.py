import pandas as pd

def get_company_list():
    df = pd.read_csv('data/data_new_list_wikipedia.csv', header=[0, 1], index_col=0, dayfirst=True, parse_dates=True)
    companies = df.columns.get_level_values(0).to_list()

    return list(dict.fromkeys(companies))


def get_working_days(year):
    df = pd.read_csv('data/data_new_list_wikipedia.csv', header=[0, 1], index_col=0, dayfirst=True, parse_dates=True)
    days = [item.strftime('%Y%m%d') for item in df.loc[str(year)].index.to_list()]

    return days

def get_prices(list_of_tickers):
    df = pd.read_csv('data/data_new_list_wikipedia.csv', header=[0, 1], index_col=0, dayfirst=True, parse_dates=True)
    df = df[list_of_tickers]

    return df.iloc[:, ::2]


def get_price_stock(symbol, date):
    return get_prices([symbol]).loc[date.strftime('%Y%m%d')].values[0]


def get_volumes(list_of_tickers):
    df = pd.read_csv('data/data_new_list_wikipedia.csv', header=[0, 1], index_col=0, dayfirst=True, parse_dates=True)
    df = df[list_of_tickers]

    return df.iloc[:, 1::2]


def get_volatilities(list_of_tickers, feature):
    df = pd.read_csv('data/data_new_list_wikipedia.csv', header=[0, 1], index_col=0, dayfirst=True, parse_dates=True)
    df = df[list_of_tickers]
    if feature.lower() == 'price':
        df = df.iloc[:, ::2]
    elif feature.lower() == 'volume':
        df = df.iloc[:, 1::2]
    else:
        print("Please insert either 'price' or 'volume' as feature")
        return

    return
