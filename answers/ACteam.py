import numpy as np

from dal.service import DalService


# this function will always return current price * 0.99999999
# because Rfq qty will "never" be above average daily volume (especially
# if qty is negative...)

def z_score(data):
    mean = data.mean()
    std = data.std()
    return (data.iloc[-1].values[0] - mean[0]) / std[0]


def get_macd(data, days_short, days_long):
    exp1 = data.ewm(span=days_short, adjust=False).mean()
    exp2 = data.ewm(span=days_long, adjust=False).mean()
    macd = exp1 - exp2
    return macd


def answer_rfq(rfq):
    days_short = 2
    days_long = 10
    days_histo = 10
    param = 0.001

    price_stock_hist = DalService.get_prices(rfq.get_sym()).tail(days_histo)
    z_scr = z_score(price_stock_hist)

    hist_volume = DalService.get_volumes(rfq.get_sym()).tail(days_histo)
    med_volume = np.median(hist_volume)

    if rfq.get_qty() > 0:
        if abs(rfq.get_qty()) > med_volume:
            return price_stock_hist.iloc[-1].values[0] * (1 + abs(z_scr) * param)
        else:
            if get_macd(price_stock_hist, days_short, days_long).iloc[-1].values[0] < 0:
                return price_stock_hist.iloc[-1].values[0] * (1 + abs(z_scr) * param)
            else:
                return price_stock_hist.iloc[-1].values[0]

    else:
        if abs(rfq.get_qty()) > med_volume:
            return price_stock_hist.iloc[-1].values[0] * (1 - abs(z_scr) * param)
        else:
            if get_macd(price_stock_hist, days_short, days_long).iloc[-1].values[0] > 0:
                return price_stock_hist.iloc[-1].values[0] * (1 - abs(z_scr) * param)
            else:
                return price_stock_hist.iloc[-1].values[0]
