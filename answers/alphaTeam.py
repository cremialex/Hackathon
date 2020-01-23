import numpy as np
import pandas as pd

from dal.service import DalService


# this function will always return current price * 0.99999999
# because Rfq qty will "never" be above average daily volume (especially
# if qty is negative...)


def answer_rfq(rfq):
    def on_balance_volume(close, volume, fillna=False):

        df = pd.DataFrame([close, volume]).transpose()
        df['OBV'] = np.nan
        c1 = close < close.shift(1)
        c2 = close > close.shift(1)
        if c1.any():
            df.loc[c1, 'OBV'] = - volume
        if c2.any():
            df.loc[c2, 'OBV'] = volume
        obv = df['OBV'].cumsum()
        if fillna:
            obv = obv.replace([np.inf, -np.inf], np.nan).fillna(0)
        return pd.Series(obv, name='obv')

    dataframe = DalService.get_prices(rfq.get_sym()).join(DalService.get_volumes(rfq.get_sym()), on="Date")
    dataframe = dataframe.merge(on_balance_volume(dataframe["Adj Close"], dataframe["Volume"]).to_frame(),
                                left_index=True, right_index=True)
    dataframe["priceTrends"] = dataframe[["Adj Close"]] - dataframe[["Adj Close"]].shift(1)
    dataframe["obvTrends"] = dataframe[["obv"]] - dataframe[["obv"]].shift(1)

    dataframe.loc[(dataframe["priceTrends"] > 0) & (dataframe["obvTrends"] < 0), 'price'] = dataframe['Adj Close'] * (
            1 - (rfq.get_qty() / abs(rfq.get_qty())) * 0.06)
    dataframe.loc[(dataframe["priceTrends"] < 0) & (dataframe["obvTrends"] > 0), 'price'] = dataframe['Adj Close'] * (
            1 + (rfq.get_qty() / abs(rfq.get_qty())) * 0.01)
    dataframe['diff'] = dataframe['Adj Close'].pct_change().shift(1).fillna(0)
    dataframe.loc[(dataframe["priceTrends"] > 0) & (dataframe["obvTrends"] > 0), 'price'] = dataframe['Adj Close'] * (
            1 + dataframe['diff'] * (rfq.get_qty() / abs(rfq.get_qty())) / 100)
    dataframe.loc[(dataframe["priceTrends"] < 0) & (dataframe["obvTrends"] < 0), 'price'] = dataframe['Adj Close'] * (
            1 + dataframe['diff'] * (rfq.get_qty() / abs(rfq.get_qty())) / 100)

    dataframe["price"] = dataframe["price"].fillna(dataframe['Adj Close'])

    return dataframe["price"].iloc[-1]
