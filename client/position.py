class Position:
    def __init__(self, symbol, qty, fill_date):
        self._symbol = symbol
        self._qty = qty
        self._fill_date = fill_date

    def get_symbol(self):
        return self._symbol

    def get_qty(self):
        return self._qty

    def set_qty(self, new_qty):
        self._qty = new_qty

    def get_fill_date(self):
        return self._fill_date
