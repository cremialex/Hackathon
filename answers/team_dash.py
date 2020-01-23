import numpy as np

from dal.service import DalService


def answer_rfq(rfq):
    price_stock_hist = DalService.get_prices(rfq.get_sym())
    price_stock_hist_ret = price_stock_hist.pct_change() * rfq.get_qty() / abs(rfq.get_qty())
    volume = DalService.get_volumes(rfq.get_sym())
    vol_long = price_stock_hist_ret.rolling(20).std()
    vol_courte = price_stock_hist_ret.rolling(5).std()
    buy_sell = np.sign(rfq.get_qty())

    if buy_sell == 1:
        if abs(rfq.get_qty() * price_stock_hist.iloc[-1].values[0]) > 275000:
            return price_stock_hist.iloc[-1].values[0] * 0.9998
        else:
            if vol_courte.iloc[-1].values[0] > vol_long.iloc[-1].values[0] * 1.15:
                if price_stock_hist.iloc[-10:].mean().values[0] > price_stock_hist.iloc[-20:].mean().values[0]:
                    return price_stock_hist.iloc[-1].values[0] * 1.000035000001
                else:
                    return price_stock_hist.iloc[-1].values[0] * 1.0000100001
            return price_stock_hist.iloc[-1].values[0] * 1.00002500001
    else:
        if abs(rfq.get_qty() * price_stock_hist.iloc[-1].values[0]) > 325000:
            return price_stock_hist.iloc[-1].values[0] * 1.0002
        else:
            if vol_courte.iloc[-1].values[0] > vol_long.iloc[-1].values[0] * 1.15:
                if price_stock_hist.iloc[-10:].mean().values[0] > price_stock_hist.iloc[-20:].mean().values[0]:
                    return price_stock_hist.iloc[-1].values[0] * 0.999999998
                else:
                    return price_stock_hist.iloc[-1].values[0] * 0.9998998
            return price_stock_hist.iloc[-1].values[0] * 0.9997998
