import random

from dal.service import DalService
from rfq.rfq import Rfq


class RfqService:
    class __RfqService:
        def __init__(self, param):
            self.param = param

        def generate_rfq(self):
            data = DalService.get_company_list()
            index_sp500 = random.randint(0, len(data) - 1)
            price = DalService.get_prices(data[index_sp500]).iloc[-1].values[0]
            num_of_shares = int(self.param / price)
            quantity = random.randint(-num_of_shares, num_of_shares)
            return Rfq(data[index_sp500], quantity)

    instance = None

    def __init__(self):
        if not RfqService.instance:
            RfqService.instance = RfqService.__RfqService(500000)

    @staticmethod
    def generate_rfq():
        return RfqService.instance.generate_rfq()
