import datetime

begin_of_day = datetime.timedelta(hours=9, minutes=30)
end_of_day = datetime.timedelta(hours=6, minutes=30)
next_day = datetime.timedelta(hours=8)

one_day = datetime.timedelta(days=1)
weekend = datetime.timedelta(days=2)


class Calendar:
    class __Calendar:
        def __init__(self):
            self.current_time = datetime.datetime(2018, 1, 2)

        def add_time(self, time):
            self.current_time = self.current_time + time

        def get_current_time(self):
            return self.current_time

    instance = None
    
    def __init__(self):
        if not Calendar.instance:
            Calendar.instance = Calendar.__Calendar()

    @staticmethod
    def set_begin_of_day():
        Calendar.instance.add_time(begin_of_day)

    @staticmethod
    def set_end_of_day():
        Calendar.instance.add_time(end_of_day)

    @staticmethod
    def set_next_business_day():
        Calendar.instance.add_time(next_day)
        if Calendar.instance.get_current_time().weekday() > 4:
            Calendar.instance.add_time(next_day)

    @staticmethod
    def get_current_time():
        return Calendar.instance.get_current_time()
