import random

from dal.service import DalService
from rfq.rfq import Rfq
import numpy as np


class RfqService:
    class __RfqService:
        def __init__(self, param):
            self.param = param

        def generate_rfq(self):
            data = DalService.get_company_list()
            index_sp500 = random.randint(0, len(data) - 1)
            volumes = DalService.get_volumes(data[index_sp500]).iloc[:-1]
            volume_yesterday = volumes.iloc[-1].values[0]
            num_of_shares = int(volume_yesterday * 0.001)
            sign = np.sign(np.random.normal(volumes.pct_change().apply(np.sign).ewm(com=0.6).mean().iloc[-1].values[0], 0.5, 1)[0])
            quantity = sign * random.randint(int(num_of_shares * 0.1), num_of_shares)
            return Rfq(data[index_sp500], quantity)

    instance = None

    def __init__(self):
        if not RfqService.instance:
            RfqService.instance = RfqService.__RfqService(500000)

    @staticmethod
    def generate_rfq():
        return RfqService.instance.generate_rfq()
