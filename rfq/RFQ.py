#!/usr/bin/python
default_price = 0


class RFQ:
    def __init__(self, time, sym, qty, client=None, price=None):
        self.time = time
        self.sym = sym
        self.qty = qty
        if price is None:
            self.price = None
        else:
            self.price = client

        if price is None:
            self.price = default_price
        else:
            self.price = price
