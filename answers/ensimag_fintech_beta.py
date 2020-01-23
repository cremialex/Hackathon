import pandas as pd

from dal.service import DalService


def answer_rfq(rfq):
    price_stock_hist = DalService.get_prices(rfq.get_sym())

    volume_stock_hist = DalService.get_volumes(rfq.get_sym())
    volume_stock_hist = pd.DataFrame(volume_stock_hist.values[0:125])

    # we authorize ourself to take more risk
    quantile_volume = volume_stock_hist.quantile(0.90)

    hist_prices_100 = DalService.get_prices(rfq.get_sym()).iloc[-100:]
    mva_100 = hist_prices_100.mean()

    hist_prices_200 = DalService.get_prices(rfq.get_sym()).iloc[-200:]
    mva_200 = hist_prices_200.mean()

    gap = mva_200 - mva_100
    price_to_return = 0

    if float(gap) > float(0):
        # when the prices are getting higher
        if volume_stock_hist.iloc[-1].values[0] > quantile_volume.values:
            # when volumes are big, we trying to improve benefits
            price_to_return = price_stock_hist.iloc[-1].values[0] * 1.02
        else:
            # with less volume, we keep the current price
            price_to_return = price_stock_hist.iloc[-1].values[0]
    else:
        # when the prices are decreasing
        if volume_stock_hist.iloc[-1].values[0] > quantile_volume.values:
            # we have big volumes, we have to reduce it
            price_to_return = price_stock_hist.iloc[-1].values[0] * 0.998
        else:
            # when volumes are low, we keep the price, taking the risk of not selling
            price_to_return = price_stock_hist.iloc[-1].values[0]
    return price_to_return
