import client.position as position
import dal.functions as dal
import runner.calendar as cal


class Allocator:
    def __init__(self, clients):
        self.clients = clients
        self.calendar = cal.Calendar()

    def allocate_rfq(self, incoming_rfq):
        winning_client = None
        best_bet = 0
        for client in self.clients:
            client_ans = client.answer_rfq(incoming_rfq)
            if client_ans > best_bet:
                winning_client = client
                best_bet = client_ans
        rfq_as_pos = position.Position(incoming_rfq[0], incoming_rfq[1], self.calendar.get_current_time())
        winning_client.add_to_portfolio(rfq_as_pos)
        winning_client.adjust_pnl(best_bet - dal.get_price_stock(incoming_rfq[0], self.calendar.get_current_time()))
        return winning_client
