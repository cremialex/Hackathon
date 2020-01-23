import numpy as np

from dal.service import DalService


def answer_rfq(rfq):
    mean_ret = DalService.get_prices(rfq.get_sym()).pct_change().mean().values[0]
    med_volume = DalService.get_volumes(rfq.get_sym()).iloc[-10:].values[:]
    med_volume = np.mean(med_volume)
    pivot_price = DalService.get_prices(rfq.get_sym()).iloc[-1].values[0]
    distance = 20 / (100 ** 2)
    param_1 = 15000
    param_2 = 0.5
    if rfq.get_qty() < 0:
        if abs(rfq.get_qty()) * pivot_price > param_1:
            return pivot_price
        else:
            return pivot_price * (1 - distance + param_2 * mean_ret)
    else:
        if abs(rfq.get_qty()) * pivot_price > param_1:
            return pivot_price
        else:
            return pivot_price * (1 + distance + param_2 * mean_ret)
