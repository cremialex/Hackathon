import random

from dal.service import DalService
from rfq.rfq import Rfq


def get_new_rfq():
    data = DalService.get_company_list()
    index_sp500 = random.randint(0, len(data))
    quantity = random.randint(-10000, 10000)
    return Rfq(data[index_sp500], quantity)
