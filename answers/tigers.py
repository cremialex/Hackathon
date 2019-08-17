import numpy as np

import dal.functions as dal


def answer_rfq(rfq):
    hist_prices = dal.get_prices(rfq.get_sym()).iloc[-20:]
    std_price = np.mean(hist_prices)

    hist_volume = dal.get_volumes(rfq.get_sym()).iloc[-20:]
    med_volume = np.median(hist_volume)

    param = 0.2

    if rfq.get_qty() < 0:
        if abs(rfq.get_qty()) > med_volume:
            return dal.get_prices(rfq.get_sym()).iloc[-1].values[0] * (1 - (param + 0.6) * std_price)
        else:
            return dal.get_prices(rfq.get_sym()).iloc[-1].values[0]

    else:
        if abs(rfq.get_qty()) > med_volume:
            return dal.get_prices(rfq.get_sym()).iloc[-1].values[0] * (1 + param * std_price)
        else:
            return dal.get_prices(rfq.get_sym()).iloc[-1].values[0]
