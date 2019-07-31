import datetime

begin_of_day = datetime.timedelta(hours=9, minutes=30)
end_of_day = datetime.timedelta(hours=6, minutes=30)
next_day = datetime.timedelta(hours=8)

one_day = datetime.timedelta(days=1)
weekend = datetime.timedelta(days=2)


class Calendar:
    def __init__(self):
        self.current_time = datetime.datetime(2018, 1, 1)

    def set_begin_of_day(self):
        self.current_time = self.current_time + begin_of_day

    def set_end_of_day(self):
        self.current_time = self.current_time + end_of_day

    def set_next_business_day(self):
        self.current_time = self.current_time + next_day
        if self.current_time.weekday() > 4:
            self.current_time = self.current_time + weekend

    def get_current_time(self):
        return self.current_time
