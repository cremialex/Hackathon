import numpy as np

# from scipy.stats import pearsonr
from dal.service import DalService


# Mean reverting strategy

def answer_rfq(rfq):
    days = 30

    price_stock_hist = DalService.get_prices(rfq.get_sym())
    price_stock_day = DalService.get_prices(rfq.get_sym()).iloc[-30:].values[0]
    price_stock_mean = np.mean(price_stock_day)

    cumulative_volume_hist = DalService.get_volumes(rfq.get_sym())
    volatility_hist = DalService.get_volatilities(price_stock_hist, days)
    # moving_average_hist = DalService.get_moving_average(price_stock_hist, days)

    # Pearson's correlation
    # corr, _ = pearsonr(cumulative_volume_hist, volatility_hist)

    if rfq.get_qty() > 0:
        param_buy = abs(price_stock_hist.iloc[-1].values[0] - price_stock_mean) / 2

        if price_stock_hist.iloc[-1].values[0] > price_stock_mean:
            return price_stock_mean
        else:
            return price_stock_hist.iloc[-1].values[0] * (1 + 0.0001 * param_buy)
    else:
        param_sell = abs(price_stock_hist.iloc[-1].values[0] - price_stock_mean) / 2

        if price_stock_hist.iloc[-1].values[0] > price_stock_mean:
            return price_stock_hist.iloc[-1].values[0] * (1 - 0.0001 * param_sell)
        else:
            return price_stock_mean
