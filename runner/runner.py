# Base Runner Code


import backtest.backtest as benchmark
import dal.functions as dal
import rfq.rfq_sender as generator
import runner.allocator as alloc
import runner.calendar as cal
import runner.unwinder as unwind
from answers import agata, alessandro, victor


class Runner:
    def __init__(self):
        self.current_day = cal.Calendar()
        self.clients = []
        self.unwinder = unwind.Unwinder()
        self.working_days = dal.get_working_days(2018)

    def run(self):
        import client.client as client
        print(self.current_day.get_current_time())

        # Creating fake clients manual at the moment make sure the import the answers
        clientNew = client.Client('baptiste', benchmark.benchmark_safe_move)
        self.clients.append(clientNew)

        clientNew = client.Client('agata', agata.answer_rfq)
        self.clients.append(clientNew)

        clientNew = client.Client('victor', victor.answer_rfq)
        self.clients.append(clientNew)

        clientNew = client.Client('alessandro', alessandro.answer_rfq)
        self.clients.append(clientNew)
        # ----------------------

        self.run_year()

    def run_year(self):
        while self.current_day.get_current_time().year == 2018:
            while self.current_day.get_current_day_string() not in self.working_days:
                self.current_day.to_next_day()
            self.run_day()

    def run_day(self):
        self.current_day.set_begin_of_day()
        print(self.current_day.get_current_time())
        RFQs = []

        for i in range(5):
            RFQs.append(generator.get_new_rfq())

        for rfq in RFQs:
            print(rfq)

            allocator = alloc.Allocator(self.clients)

            for client in self.clients:
                print(str(client.name) + ' answer is ' + str(client.answer_rfq(rfq)))

            rfq_winner = allocator.allocate_rfq(rfq)
            if rfq_winner is None:
                print('No Winner')
            else:
                print('Winner of the auction is ' + rfq_winner.name)
            print("\n")

        self.current_day.set_end_of_day()
        print(self.current_day.get_current_time())

        for client in self.clients:
            self.unwinder.unwind_client(client)
            client.display_portfolio()

        self.current_day.set_next_business_day()
        print("\n\n------- NEW DAY -------")
        print(self.current_day.get_current_time())
