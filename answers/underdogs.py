import dal.functions as dal


def answer_rfq(incoming_rfq):
    historical_prices = dal.get_prices([incoming_rfq[0]])
    order_qty = incoming_rfq[1]
    hst_price_z_scr = vol_z_score(historical_prices)

    if order_qty < 1:
        final_price = historical_prices.iloc[-1].values[0] * (1 + 0.3 * hst_price_z_scr / 100)

    else:
        final_price = historical_prices.iloc[-1].values[0] * (1 - 0.5 * hst_price_z_scr / 100)

    return final_price


def vol_z_score(historical_volumes):
    vol_mean = historical_volumes.mean()
    vol_sd = historical_volumes.std()
    return (historical_volumes.iloc[-1].values[0] - vol_mean[0]) / vol_sd[0]
