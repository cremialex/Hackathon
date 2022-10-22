import numpy as np
import math

from dal.service import DalService

# z score i.e. normalize the dataset
def z_score(data):
    mean = data.mean()
    std = data.std()
    return (data.iloc[-1].values[0] - mean[0]) / std[0]

#sigmoid function
def sigmoid(x):
    import math
    return 1/(1+math.exp(-x))

#tuning looking at the volatilities over multiple horizon
def tuning(data):
    vol7 = DalService().get_volatilities(data, 7).iloc[-1].values[-1]
    vol21 = DalService().get_volatilities(data, 21).iloc[-1].values[-1]

    tuner = sigmoid((vol21 - vol7)/vol21)
    return tuner

#macd signal
def get_macd(data):
    exp1 = data.ewm(span=12, adjust=False).mean()
    exp2 = data.ewm(span=26, adjust=False).mean()
    return exp1 - exp2


# function that return a float
# rfq is an object with 2 attributes qty and stock name (universe S&P 500)
def answer_rfq(rfq):
    #get historical data and run some analysis
    price_stock_hist = DalService.get_prices(rfq.get_sym())
    prices_last_week = price_stock_hist.iloc[-20:].values[0]
    volume_last_week = 1.0 / DalService.get_volumes(rfq.get_sym()).iloc[-20:].values[0]
    mean = prices_last_week.dot(volume_last_week) / np.sum(volume_last_week)
    # z score
    z_score = (price_stock_hist.iloc[-1].values[0] - mean) / price_stock_hist.iloc[-20:].std().values[0]
    spread = 1e-4
    #adding some scaling based on how the zscore is performing compared to historically
    if np.abs(z_score) > 2:
        m = 1.1
    elif np.abs(z_score) > 1 and np.abs(z_score) < 2:
        m = 1.2
    else:
        m = 1
    # discretionnary factor applied to the price depending on various factors
    price_factor = (1 + spread * m * z_score)
    #previous close price loaded from the data
    previous_close = price_stock_hist.iloc[-1].values[0]

    return previous_close * price_factor
