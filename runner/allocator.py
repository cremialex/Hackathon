import client.position as position
import runner.calendar as cal
from dal.service import DalService


class Allocator:
    def __init__(self, clients):
        self.clients = clients
        self.calendar = cal.Calendar()

    def allocate_rfq(self, incoming_rfq):
        winning_client = None
        best_bet = None
        rfq_as_pos = position.Position(incoming_rfq.get_sym(), incoming_rfq.get_qty(), self.calendar.get_current_time())
        if incoming_rfq.get_qty() > 0:
            best_bet = 0
            for client in self.clients:
                client_ans = client.answer_rfq(incoming_rfq)
                print(str(client.name) + ' answer is ' + str(client_ans))
                if client_ans is not None and client_ans > best_bet:
                    winning_client = client
                    best_bet = client_ans
        if incoming_rfq.get_qty() <= 0:
            best_bet = 1000000
            for client in self.clients:
                client_ans = client.answer_rfq(incoming_rfq)
                print(str(client.name) + ' answer is ' + str(client_ans))
                if client_ans is not None and client_ans < best_bet:
                    winning_client = client
                    best_bet = client_ans

        if winning_client is not None:
            winning_client.add_to_portfolio(rfq_as_pos)
            winning_client.adjust_pnl(incoming_rfq.get_qty() * (
                    DalService.get_price_stock(incoming_rfq.get_sym(), self.calendar.get_current_time()) - best_bet))
            return winning_client
        return None
