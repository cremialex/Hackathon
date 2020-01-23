import numpy as np

from dal.service import DalService


def answer_rfq(rfq):
    hist_prices = DalService.get_prices(rfq.get_sym()).iloc[-3:]
    mean_price = np.mean(hist_prices)

    median_price = np.median(hist_prices)

    hist_volume = DalService.get_volumes(rfq.get_sym()).iloc[-3]
    med_volume = np.median(hist_volume)

    hist_vol = DalService.get_volatilities(hist_prices, 3)
    mean_vol = np.mean(hist_vol)

    spot_price = hist_prices.values[-1]

    std = 1.4
    ecart = (std * float(hist_vol.values[-1]))
    if abs(float(spot_price) - float(mean_price)) < ecart:
        m = mean_price
        if float(spot_price) > float(mean_price):
            price = spot_price - (spot_price - m) / 150
        else:
            price = spot_price + (spot_price - m) / 150

    else:
        price = float(spot_price + mean_price) / 2

    return (float(price))
