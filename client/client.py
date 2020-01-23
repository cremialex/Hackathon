from client.pnl_event import PnlEvent
from client.portfolio import Portfolio
from datalogger.logger_service import LoggerService
from runner.calendar import CalendarService


class Client:
    def __init__(self, name, function_rfq=lambda x: 0):
        self._name = name
        self._function_rfq = function_rfq
        self._portfolio = Portfolio()
        self._pnl = 0
        self._is_bankrupt = False

    def answer_rfq(self, incoming_rfq):
        if self._is_bankrupt:
            return None
        return self._function_rfq(incoming_rfq)

    def add_to_portfolio(self, position):
        self._portfolio.add_position(position)

    def display_portfolio(self):
        print(self._name + ' Portfolio is composed of: ')
        self._portfolio.compute_inventory()
        self._portfolio.show_inventory()
        print(self._name + ' PnL is: ' + str(self._pnl))

    def get_name(self):
        return self._name

    def get_portfolio(self):
        return self._portfolio

    def adjust_pnl(self, trade_pnl):
        pnl_event = PnlEvent(CalendarService.get_current_time(), trade_pnl, self._name, 'No reason')
        LoggerService.log(pnl_event)
        self._pnl = self._pnl + trade_pnl
        if not self._is_bankrupt and self._pnl < -200_000:
            self._is_bankrupt = True
            print(self._name + ' is now BANKRUPT')
