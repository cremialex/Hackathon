from dal.service import DalService


# this function will always return current price * 0.99999999

# because Rfq qty will "never" be above average daily volume (especially

# if qty is negative...)
def answer_rfq(rfq):
    price_stock_hist = DalService.get_prices(rfq.get_sym())
    ll = -10
    volume = DalService.get_volumes(rfq.get_sym())

    if ((moyenne_mobile(price_stock_hist, 99) - moyenne_mobile(price_stock_hist, 199)) * (
            moyenne_mobile(price_stock_hist, 100) - moyenne_mobile(price_stock_hist, 200))) < 0:
        if (moyenne_mobile(price_stock_hist, 100) < moyenne_mobile(price_stock_hist, 200)):
            return price_stock_hist.iloc[-1].values[0] * (1 - 10 ** ll)

        if (moyenne_mobile(price_stock_hist, 100) > moyenne_mobile(price_stock_hist, 200)):
            return price_stock_hist.iloc[-1].values[0] * (1 + 10 ** ll)
    else:
        if rfq.get_qty() < 0:
            return price_stock_hist.iloc[-1].values[0] * (1 - 10 ** ll)
        else:
            return price_stock_hist.iloc[-1].values[0] * (1 + 10 ** ll)


def moyenne_mobile(historique, profondeur):
    return historique.iloc[-profondeur:].mean().values[0]
