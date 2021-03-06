import numpy as np

from dal.service import DalService


# this function will always return current price
# because Rfq qty will "never" be above MDV21
def answer_rfq(rfq):
    hist_prices = DalService.get_prices(rfq.get_sym()).iloc[-20:]
    mean_price = np.mean(hist_prices)

    hist_volume = DalService.get_volumes(rfq.get_sym()).iloc[-20:]
    med_volume = np.median(hist_volume)

    param = 0.2

    if rfq.get_qty() < 0:
        if abs(rfq.get_qty()) > med_volume:
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0] * (1 - (param + 0.6) * mean_price)
        else:
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0]

    else:
        if abs(rfq.get_qty()) > med_volume:
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0] * (1 + param * mean_price)
        else:
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0]
