import numpy as np
import pandas as pd

import dal.functions as dal


# Strategy based on momentum (of only latest return)
# More agressive if volume above 95% quantile
def answer_rfq(rfq):
    price_stock_hist = dal.get_prices(rfq.get_sym())
    price_stock_hist_ret = price_stock_hist.pct_change()

    volume_stock_hist = dal.get_volumes(rfq.get_sym())
    volume_stock_hist = pd.DataFrame(volume_stock_hist.values[0:125])

    quantile_volume = volume_stock_hist.quantile(0.95)
    sign = np.sign(price_stock_hist_ret.iloc[-1])

    if volume_stock_hist.iloc[-1].values[0] > quantile_volume.values:
        if sign.iloc[-1] > 0:
            return price_stock_hist.iloc[-1].values[0] * 1.01
        else:
            return price_stock_hist.iloc[-1].values[0] * 0.99
    else:
        if sign.iloc[-1] > 0:
            return price_stock_hist.iloc[-1].values[0] * 1.003
        else:
            return price_stock_hist.iloc[-1].values[0] * 0.997
