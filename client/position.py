class Position:
    def __init__(self, symbol, qty, fill_date):
        self._symbol = symbol
        self._qty = qty
        self._fill_date = fill_date

    def get_symbol(self):
        return self._symbol

    def get_qty(self):
        return self._qty

    def set_qty(self, qty):
        self._qty = qty

    def get_fill_date(self):
        return self._fill_date

    def __str__(self):
        return ' '.join([self._symbol, str(self._qty), self._fill_date.strftime('%Y-%m-%d')])
