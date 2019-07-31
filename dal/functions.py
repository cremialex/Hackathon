import pandas as pd


def get_prices(list_of_tickers):
    df = pd.read_csv('data/data_new_list_wikipedia.csv', header=[0, 1], index_col=0, dayfirst=True, parse_dates=True)
    df = df[list_of_tickers]

    return df.iloc[:, ::2]


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
