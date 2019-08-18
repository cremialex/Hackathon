from dal.service import DalService


# this function will always return current price * 0.99999999
# because Rfq qty will "never" be above average daily volume (especially
# if qty is negative...)
def answer_rfq(rfq):
    price_stock_hist = DalService.get_prices(rfq.get_sym())
    volume = DalService.get_volumes(rfq.get_sym())
    average_history_vol = volume.sum() / volume.count()

    if rfq.get_qty() > int(average_history_vol):
        return price_stock_hist.iloc[-1].values[0] * 1.30
    else:
        return price_stock_hist.iloc[-1].values[0] * 0.99999999
