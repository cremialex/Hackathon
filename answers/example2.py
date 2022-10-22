import numpy as np
import math

from dal.service import DalService


# z score i.e. normalize the dataset
def z_score(data):
    mean = data.mean()
    std = data.std()
    return (data.iloc[-1].values[0] - mean[0]) / std[0]


# sigmoid function
def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# tuning looking at the volatilities over multiple horizon
def tuning(data):
    vol7 = DalService().get_volatilities(data, 7).iloc[-1].values[-1]
    vol21 = DalService().get_volatilities(data, 21).iloc[-1].values[-1]

    tuner = sigmoid((vol21 - vol7) / vol21)
    return tuner


# macd signal
def get_macd(data):
    exp1 = data.ewm(span=12, adjust=False).mean()
    exp2 = data.ewm(span=26, adjust=False).mean()
    return exp1 - exp2


# function that return a float
# rfq is an object with 2 attributes qty and stock name (universe S&P 500)
def answer_rfq(rfq):
    days_long = 26
    days_histo = 26
    flagLarge = 0
    # loading the historical price
    price_stock_hist = DalService.get_prices(rfq.get_sym()).tail(days_histo)
    z_scr = z_score(price_stock_hist)
    # loading the historical volumes
    hist_volume = DalService.get_volumes(rfq.get_sym()).tail(days_histo)
    med_volume = np.median(hist_volume)

    # tune based on the volatility
    tuner = tuning(price_stock_hist)
    param_1 = 0.001
    param_2 = 0.02 * tuner

    # reduice the price if there is a lot of volume
    if abs(rfq.get_qty()) > med_volume:
        flagLarge = 1

    #storing some values in variables
    last_macd = DalService.get_macd_signal_line(price_stock_hist).iloc[-1].values[-1]
    previous_close = price_stock_hist.iloc[-1].values[0]
    #discretionnary factor applied to the price depending on various factors
    price_factor = param_2 * last_macd * (1-flagLarge * abs(z_scr)) * param_1

    # qty is neg we return the opposite price
    if rfq.get_qty() >0:
        return previous_close + price_factor
    else:
        return previous_close - price_factor