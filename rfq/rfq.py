class Rfq:
    def __init__(self, sym, qty):
        self._sym = sym
        self._qty = qty

    def get_sym(self):
        return self._sym

    def get_qty(self):
        return self._qty

    def __str__(self):
        return ' '.join([self._sym, str(self._qty)])
