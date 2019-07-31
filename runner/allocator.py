import client.position as position


class Allocator:
    def __init__(self, clients):
        self.clients = clients

    def allocate_rfq(self, incoming_rfq):
        winning_client = None
        best_bet = 0
        for client in self.clients:
            client_ans = client.answer_rfq(incoming_rfq)
            if client_ans > best_bet:
                winning_client = client
                best_bet = client_ans
        rfq_as_pos = position.Position(incoming_rfq[0], incoming_rfq[1])
        winning_client.add_to_portfolio(rfq_as_pos)
        return winning_client
