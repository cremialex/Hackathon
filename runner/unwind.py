from dal.service import DalService
from runner.calendar import CalendarService


class UnwindService:
    @staticmethod
    def unwind_client(client):
        print('unwinding client ' + client.get_name())
        client_ptf = client.get_portfolio()
        positions = client_ptf.get_raw_positions()
        for item in positions.copy():
            date = item.get_fill_date()
            if date.date() < CalendarService.get_current_time().date():
                print("Needs to unwind position " + item.get_symbol())
                client_ptf.remove_position(item)
                client.adjust_pnl(item.get_qty() *
                                  (DalService.get_price_stock(item.get_symbol(), CalendarService.get_current_time()) -
                                   DalService.get_price_stock(item.get_symbol(), item.get_fill_date())))
