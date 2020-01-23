import numpy as np

from dal.service import DalService


def answer_rfq(rfq):
    price_stock_hist = DalService.get_prices(rfq.get_sym())
    prices_last_week = price_stock_hist.iloc[-5:].values[0]

    volume_last_week = 1.0 / DalService.get_volumes(rfq.get_sym()).iloc[-5:].values[0]
    mean = prices_last_week.dot(volume_last_week) / np.sum(volume_last_week)

    z_score = (price_stock_hist.iloc[-1].values[0] - mean) / price_stock_hist.iloc[-5:].std().values[0]

    spread = 1e-4

    if np.abs(z_score) > 2:
        if np.sign(z_score) == np.sign(rfq.get_qty()):
            m = 1.1
            return price_stock_hist.iloc[-1].values[0] * (1 + spread * m * z_score)

    if np.sign(z_score) != np.sign(rfq.get_qty()):
        if np.abs(z_score) > 1 and np.abs(z_score) < 2:
            m = 1.2
        else:
            m = 1

        return price_stock_hist.iloc[-1].values[0] * (1 - spread * m * z_score)

    return None
