import numpy as np

from dal.service import DalService


# this function will always return current price
# because Rfq qty will "never" be above MDV21


def answer_rfq(rfq):
    hist_prices = DalService.get_prices(rfq.get_sym()).iloc[-20:]
    mean_price = np.mean(hist_prices)

    historical_prices = DalService.get_prices(rfq.get_sym())
    hist_price_z_scr = z_score(historical_prices)

    hist_volume = DalService.get_volumes(rfq.get_sym()).iloc[-20:]
    med_volume = np.median(hist_volume)

    param = hist_price_z_scr

    if rfq.get_qty() < 0:
        return historical_prices.iloc[-1].values[0] * 0.99999


    else:
        return historical_prices.iloc[-1].values[0] * 1.0000000001


def z_score(data):
    mean = data.mean()
    std = data.std()
    return (data.iloc[-1].values[0] - mean[0]) / std[0]
