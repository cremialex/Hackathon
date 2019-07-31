# Base Runner Code

import client.client as client
import rfq.rfq_sender as generator
import runner.allocator as alloc
import runner.calendar as cal


class Runner:
    def __init__(self):
        self.current_day = cal.Calendar()

    def run(self):
        print(self.current_day.get_current_time())

        client_baptiste = client.Client('Baptiste')

        def answer_rfq_victor(incoming_rfq):
            if incoming_rfq[1] > 0:
                return 3
            else:
                return 2

        client_victor = client.Client('Victor', answer_rfq_victor)

        allocator = alloc.Allocator([client_baptiste, client_victor])

        rfq = generator.get_new_rfq()
        print(rfq)

        self.current_day.set_begin_of_day()
        print(self.current_day.get_current_time())

        print(client_baptiste.name + ' answer is ' + str(client_baptiste.answer_rfq(rfq)))
        print(client_victor.name + ' answer is ' + str(client_victor.answer_rfq(rfq)))

        print('Winner of the auction is ' + allocator.allocate_rfq(rfq).name)

        print(client_baptiste.name + ' portfolio is composed of: ')
        client_baptiste.display_portfolio()
        print(client_baptiste.name + ' portfolio is composed of: ')
        client_victor.display_portfolio()

        self.current_day.set_end_of_day()
        print(self.current_day.get_current_time())
        self.current_day.set_next_business_day()
        print(self.current_day.get_current_time())
