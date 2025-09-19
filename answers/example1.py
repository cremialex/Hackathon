import numpy as np
import math

from dal.service import DalService


#sigmoid function
def sigmoid(x):
    import math
    return 1/(1+math.exp(-x))



# function that return a float
# rfq is an object with 2 attributes qty and stock name (universe S&P 500)
def answer_rfq(rfq):
    #get historical data and run some analysis
    price_stock_hist = DalService.get_prices(rfq.get_sym())
    prices_last_week = price_stock_hist.iloc[-20:].values[0]
    volume_last_week = 1.0 / DalService.get_volumes(rfq.get_sym()).iloc[-20:].values[0]
 
    # discretionnary factor applied to the price depending on various factors
    price_factor = (1 + 40.0)
    #previous close price loaded from the data
    previous_close = price_stock_hist.iloc[-1].values[0]

    return previous_close * price_factor
