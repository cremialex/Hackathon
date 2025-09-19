import numpy as np
import math

from dal.service import DalService


# function that return a float
# rfq is an object with 2 attributes qty and stock name (universe S&P 500)
def answer_rfq(rfq):
    days_long = 26
    days_histo = 26
    
    # loading the historical price
    price_stock_hist = DalService.get_prices(rfq.get_sym()).tail(days_histo)
   
    hist_volume = DalService.get_volumes(rfq.get_sym()).tail(days_histo)
    med_volume = np.median(hist_volume)

    

    previous_close = price_stock_hist.iloc[-1].values[0]
    #discretionnary factor applied to the price depending on various factors
    price_factor = 3

    # qty is neg we return the opposite price
    if rfq.get_qty() >0:
        return previous_close + price_factor
    else:
        return previous_close - price_factor