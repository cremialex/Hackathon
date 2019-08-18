import numpy as np

from dal.service import DalService


def benchmark_safe_move(rfq):
    price_stock_hist = DalService.get_prices(rfq.get_sym())
    price_stock_hist_ret = price_stock_hist.pct_change()
    sign = np.sign(price_stock_hist_ret.iloc[-1])
    if sign.iloc[-1] > 0:
        return price_stock_hist.iloc[-1].values[0] * 1.005
    else:
        return price_stock_hist.iloc[-1].values[0] * 0.995
