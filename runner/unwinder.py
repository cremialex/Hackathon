import dal.functions as dal
import runner.calendar as cal


class Unwinder:
    def __init__(self):
        self.calendar = cal.Calendar()

    def unwind_client(self, client):
        print('unwinding client ' + client.get_name())
        client_ptf = client.get_portfolio()
        positions = client_ptf.get_raw_positions()
        position_to_remove = []
        for item in positions:
            date = item.get_fill_date()
            if date.date() < self.calendar.get_current_time().date():
                print("Needs to unwind position " + item.get_symbol())
                position_to_remove.append(item)
        for item in position_to_remove:
            client_ptf.remove_position(item)
            client.adjust_pnl(-item.get_qty() *
                              (dal.get_price_stock(item.get_symbol(), item.get_fill_date()) -
                               dal.get_price_stock(item.get_symbol(), self.calendar.get_current_time())))
