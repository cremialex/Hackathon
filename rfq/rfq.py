class Rfq:
    def __init__(self, sym, qty):
        self.sym = sym
        self.qty = qty

    def get_sym(self):
        return self.sym

    def get_qty(self):
        return self.qty
