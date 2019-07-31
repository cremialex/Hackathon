class Client:
    def __init__(self, name, function_rfq=lambda x: 0):
        self.name = name
        self.function_rfq = function_rfq
        self.portfolio = []

    def answer_rfq(self, incoming_rfq):
        return self.function_rfq(incoming_rfq)

    def add_to_portfolio(self, position):
        self.portfolio.append(position)

    def display_portfolio(self):
        print(self.name + 'Portfolio is composed of: ')
        for pos in self.portfolio:
            print('Symbol: ' + pos.symbol + ', quantity: ' + str(pos.qty))

    def get_name(self):
        return self.name

    def get_portfolio(self):
        return self.portfolio
