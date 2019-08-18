from dal.service import DalService


# Buying: (0.3 z_score prices) % of current price added (careful, z_score prices can be negative)
# Selling: (0.5 z_score prices) % of current price removed
def answer_rfq(rfq):
    historical_prices = DalService.get_prices(rfq.get_sym())
    hist_price_z_scr = z_score(historical_prices)

    if rfq.get_qty() < 1:
        final_price = historical_prices.iloc[-1].values[0] * (1 + 0.3 * hist_price_z_scr / 100)

    else:
        final_price = historical_prices.iloc[-1].values[0] * (1 - 0.5 * hist_price_z_scr / 100)

    return final_price


def z_score(data):
    mean = data.mean()
    std = data.std()
    return (data.iloc[-1].values[0] - mean[0]) / std[0]
