import client.portfolio as ptf
import runner.calendar as cal


class Client:
    def __init__(self, name, function_rfq=lambda x: 0):
        self.name = name
        self.function_rfq = function_rfq
        self.portfolio = ptf.Portfolio()
        self.pnl = 0
        self.calendar = cal.Calendar()
        self.is_bankrupt = False

    def answer_rfq(self, incoming_rfq):
        if self.is_bankrupt:
            return None
        return self.function_rfq(incoming_rfq)

    def add_to_portfolio(self, position):
        self.portfolio.add_position(position)

    def display_portfolio(self):
        print(self.name + ' Portfolio is composed of: ')
        self.portfolio.compute_inventory()
        self.portfolio.show_inventory()
        print(self.name + ' PnL is: ' + str(self.pnl))

    def get_name(self):
        return self.name

    def get_portfolio(self):
        return self.portfolio

    def adjust_pnl(self, trade_pnl):
        self.pnl = self.pnl + trade_pnl
        if not self.is_bankrupt and self.pnl < 1_000_000:
            self.is_bankrupt = True
            print(self.name + ' is now BANKRUPT')
