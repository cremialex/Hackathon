#!/usr/bin/python

import random
from datetime import datetime
from datetime import timedelta
from random import randrange

import dal.functions as dal
import rfq.RFQ as RFQ


def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_senconds())))


def get_new_rfq():
    data = dal.get_company_list()
    index_sp500 = random.randint(0, len(data))
    quantity = random.randint(-10000, 10000)
    return data[index_sp500], quantity


def random_date(start, end):
    # function that returns the random datetime between 2 quantities
    random_hours = randrange(27)
    date_random = start + timedelta(hours=random_hours)
    return date_random


def rdf_generator(time):
    start_date = datetime.strptime(time, '%d/%m/%Y')
    end_date = datetime.strptime('1/1/2019', '%d/%m/%Y')
    random_hours = randrange(72)  # random within 3 days
    rfq_time = start_date + timedelta(hours=random_hours)
    print(rfq_time)
    sym, qty = get_new_rfq()
    print(sym)
    return RFQ.RFQ(rfq_time, sym, qty)

# print("example that print the RFQ attributes (random sym, date and qty)")
#
# testRFQ = rdf_generator("01/01/2018")
# testRFQ2 = rdf_generator("01/01/2018")
# testRFQ3 = rdf_generator("01/01/2018")
#
# print("RFQ 1: sym", testRFQ.sym, "qty: ", testRFQ.qty, ", date RFQ random range with in range: ", testRFQ.time, " ")
# print("RFQ 2: sym", testRFQ2.sym, "qty: ", testRFQ2.qty, ", date RFQ random range with in range: ", testRFQ2.time, " ")
# print("RFQ 3: sym", testRFQ3.sym, "qty: ", testRFQ3.qty, ", date RFQ random range with in range: ", testRFQ3.time, " ")
