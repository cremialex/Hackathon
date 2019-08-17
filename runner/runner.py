# Base Runner Code


import backtest.backtest as benchmark
import dal.functions as dal
import os
import rfq.rfq_sender as generator
import runner.allocator as alloc
import runner.calendar as cal
import runner.unwinder as unwind
import importlib


class Runner:
    def __init__(self, year):
        self.year = year
        self.current_day = cal.Calendar()
        self.current_day.set_start_year(year)
        self.clients = []
        self.unwinder = unwind.Unwinder()
        self.working_days = dal.get_working_days(year)

    def run(self):
        import client.client as client
        print(self.current_day.get_current_time())

        # import all the users from answers and add them all
        directoryAnswers= os.getcwd()+"/answers"
        for file in os.listdir(directoryAnswers):
            if file.endswith(".py"):
                filename = os.fsdecode(file)
                name= filename.split(".")[0]
                mod =importlib.import_module("answers."+name, __name__)
                clientNew = client.Client(name, mod.answer_rfq)
                self.clients.append(clientNew)

        #keeping the benchmark
        clientNew = client.Client('benchmark', benchmark.benchmark_safe_move)
        self.clients.append(clientNew)
        # ----------------------

        self.run_year()

    def run_year(self):
        while self.current_day.get_current_time().year == self.year:
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
