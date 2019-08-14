# Base Runner Code


import dal.functions as dal
import rfq.rfq_sender as generator
import runner.allocator as alloc
import runner.calendar as cal
import runner.unwinder as unwind


class Runner:
    def __init__(self):
        self.current_day = cal.Calendar()
        self.clients = []
        self.unwinder = unwind.Unwinder()
        self.working_days = dal.get_working_days(2018)

    def run(self):
        import client.client as client
        print(self.current_day.get_current_time())

        def answer_rfq_victor(incoming_rfq):
            if incoming_rfq[1] > 0:
                return 3
            else:
                return 2

        def answer_rfq_baptiste(incoming_rfq):
            return 5

        # Creating fake clients
        client_baptiste = client.Client('Baptiste', answer_rfq_baptiste)
        self.clients.append(client_baptiste)
        client_victor = client.Client('Victor', answer_rfq_victor)
        self.clients.append(client_victor)
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

            print('Winner of the auction is ' + allocator.allocate_rfq(rfq).name)
            print("\n")

        self.current_day.set_end_of_day()
        print(self.current_day.get_current_time())

        for client in self.clients:
            self.unwinder.unwind_client(client)
            client.display_portfolio()

        self.current_day.set_next_business_day()
        print("\n\n------- NEW DAY -------")
        print(self.current_day.get_current_time())
