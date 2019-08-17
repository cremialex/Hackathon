import random

import dal.functions as dal
import rfq.rfq as rfq


def get_new_rfq():
    data = dal.get_company_list()
    index_sp500 = random.randint(0, len(data))
    quantity = random.randint(-10000, 10000)
    return rfq.Rfq(data[index_sp500], quantity)
