import datetime


class CalendarService:
    class __Calendar:
        def __init__(self):
            self._current_time = datetime.datetime(2017, 1, 1)

        def add_time(self, time):
            self._current_time = self._current_time + time

        def get_current_time(self):
            return self._current_time

        def set_current_year(self, year):
            self._current_time = datetime.datetime(year, 1, 1)

    instance = None

    begin_of_day = datetime.timedelta(hours=9, minutes=30)
    end_of_day = datetime.timedelta(hours=6, minutes=30)
    next_day = datetime.timedelta(hours=8)
    one_day = datetime.timedelta(days=1)
    
    def __init__(self):
        if not CalendarService.instance:
            CalendarService.instance = CalendarService.__Calendar()

    @staticmethod
    def set_begin_of_day():
        CalendarService.instance.add_time(CalendarService.begin_of_day)

    @staticmethod
    def set_end_of_day():
        CalendarService.instance.add_time(CalendarService.end_of_day)

    @staticmethod
    def set_next_business_day():
        CalendarService.instance.add_time(CalendarService.next_day)

    @staticmethod
    def to_next_day():
        CalendarService.instance.add_time(CalendarService.one_day)

    @staticmethod
    def get_current_time():
        return CalendarService.instance.get_current_time()

    @staticmethod
    def get_current_day_string(date_format='%Y%m%d'):
        return CalendarService.instance.get_current_time().strftime(date_format)

    @staticmethod
    def set_start_year(year):
        CalendarService.instance.set_current_year(year)
