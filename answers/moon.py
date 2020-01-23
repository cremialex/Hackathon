import numpy as np

from dal.service import DalService

infinity = int(1e10)


# this function will always return current price * 0.99999999
# because Rfq qty will "never" be above average daily volume (especially
# if qty is negative...)
def answer_rfq(rfq):
    sym = rfq.get_sym()
    qty = rfq.get_qty()

    price_stock_hist = DalService.get_prices(rfq.get_sym())
    price_stock_hist_ret = price_stock_hist.pct_change()

    short_vol = np.mean([price_stock_hist_ret.iloc[-i].values[0] for i in range(1, 4)])

    short_mean = np.mean([price_stock_hist.iloc[-i].values[0] for i in range(1, 4)])
    long_mean = np.mean([price_stock_hist.iloc[-i].values[0] for i in range(1, 61)])

    hist_volume = DalService.get_volumes(rfq.get_sym()).iloc[-20:]
    med_volume = np.median(hist_volume)

    print("short", short_mean)
    print("long", long_mean)
    print("short vol ", short_vol)

    if rfq.get_qty() < 0:  # achat, prix le plus bas
        """
        if(short_mean<long_mean):
            #vend
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0]*(1-abs(short_vol)/2)
        else:
            #ne vend pas
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0]*(1+abs(short_vol))
        """

        return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0] * 0.999999


    else:  # vente, prix le plus élevé
        """
        if(short_mean>long_mean):
            #achète
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0]*(1+abs(short_vol)/2)
        else:
            #n'achète pas
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0]*(1-abs(short_vol))
        """

        return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0] * 1.000001
