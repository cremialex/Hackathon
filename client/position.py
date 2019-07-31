class Position:
    def __init__(self, symbol, qty, fill_date=0):
        self.symbol = symbol
        self.qty = qty
        self.fill_date = fill_date

    def get_symbol(self):
        return self.symbol

    def get_qty(self):
        return self.qty

    def set_qty(self, new_qty):
        self.qty = new_qty

    def get_fill_date(self):
        return self.fill_date
