# Backtest Example
import numpy as np

import dal.functions as dal


def benchmark_safe_move(incoming_rfq):
    symbol = incoming_rfq[0]
    price_stock_hist = dal.get_prices([symbol])
    price_stock_hist_ret = price_stock_hist.pct_change()
    sign = np.sign(price_stock_hist_ret.iloc[-1])
    if sign.iloc[-1] > 0:
        return price_stock_hist.iloc[-1].values[0] * 1.005
    else:
        return price_stock_hist.iloc[-1].values[0] * 0.995
