import dal.functions as dal


# return current price times a multiplier (4 different values)
# this multiplier is define in a dictionnary, the key selected is
# the closest to z-score returns
# Strategy is basicaly momentum based and cutting risk for too large z_score
def answer_rfq(incoming_rfq):
    price_stock_hist = dal.get_prices(incoming_rfq.get_sym())
    price_stock_hist_ret = price_stock_hist.pct_change() * incoming_rfq.get_qty() / abs(incoming_rfq.get_qty())

    z_dict = {
        0.8: 1.0050000001,  # add 50 bips
        1: 1.000000001,  # market price
        -0.8: 0.99499999999,  # remove 50 bips
        -1: 0.989999999999  # remove 1 %
    }

    rtn_z = ((price_stock_hist_ret.iloc[-1] - price_stock_hist_ret.iloc[-10:].mean()) / price_stock_hist_ret.iloc[
                                                                                        -60:].std()).values

    rtn_multiplier = z_dict[min(z_dict.keys(), key=lambda x: abs(x - rtn_z))]

    return price_stock_hist.iloc[-1].values[0] * rtn_multiplier
