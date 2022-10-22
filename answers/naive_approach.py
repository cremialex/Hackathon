import numpy as np
import pandas as pd
from dal.service import DalService

#naive strategy which returns the last available close price
#the intuition is that our best prediction is the current price
def answer_rfq(rfq):
    price_stock_hist = DalService.get_prices(rfq.get_sym())
    return price_stock_hist.iloc[-1].values[0]
