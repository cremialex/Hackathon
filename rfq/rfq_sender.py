import random

from dal.service import DalService
from rfq.rfq import Rfq


def get_new_rfq():
    data = DalService.get_company_list()
    index_sp500 = random.randint(0, len(data) - 1)
    price = DalService.get_prices(data[index_sp500]).iloc[-1].values[0]
    num_of_shares = int(500000/price)
    quantity = random.randint(-num_of_shares, num_of_shares)
    return Rfq(data[index_sp500], quantity)
