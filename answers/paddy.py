import dal.functions as dal


def answer_rfq(incoming_rfq):
    symbol = incoming_rfq[0]
    price_stock_hist = dal.get_prices([symbol])
    volume = dal.get_volumes(symbol)
    average_history_vol = volume.sum() / volume.count()

    volume_rfq = incoming_rfq[1]
    if volume_rfq > int(average_history_vol):
        return price_stock_hist.iloc[-1].values[0] * 1.30
    else:
        return price_stock_hist.iloc[-1].values[0] * 0.99999999
