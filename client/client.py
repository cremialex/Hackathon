import runner.calendar as cal


class Client:
    def __init__(self, name, function_rfq=lambda x: 0):
        self.name = name
        self.function_rfq = function_rfq
        self.portfolio = []
        self.pnl = 0
        self.calendar = cal.Calendar()

    def answer_rfq(self, incoming_rfq):
        return self.function_rfq(incoming_rfq)

    def add_to_portfolio(self, position):
        self.portfolio.append(position)

    def display_portfolio(self):
        print(self.name + ' Portfolio is composed of: ')
        for pos in self.portfolio:
            print('Symbol: ' + pos.symbol + ', quantity: ' + str(pos.qty) + ', fill date: ' + pos.get_fill_date()
                  .isoformat())
        print(self.name + ' PnL is: ' + str(self.pnl))

    def get_name(self):
        return self.name

    def get_portfolio(self):
        return self.portfolio

    def adjust_pnl(self, trade_pnl):
        self.pnl = self.pnl + trade_pnl

    def portfolio_manager(self):
        for pos in self.portfolio:
            print('to do')
