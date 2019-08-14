class Portfolio:
    def __init__(self):
        self.inventory = dict()  # keyed by symbol
        self.historical_positions = set()
        self.raw_positions = set()

    # position is a tuple ()
    def add_position(self, position):
        self.historical_positions.add(position)
        self.raw_positions.add(position)

    def remove_position(self, position):
        self.raw_positions.remove(position)

    def compute_inventory(self):
        for item in self.raw_positions:
            current_position = self.inventory.get(item.get_symbol())
            if current_position is None:
                self.inventory[item.get_symbol()] = item.get_qty()
            else:
                self.inventory[item.get_symbol()] = current_position + item.get_qty()

    def get_inventory(self):
        return self.inventory

    def get_raw_positions(self):
        return self.raw_positions

    def get_historical_positions(self):
        return self.historical_positions

    def show_inventory(self):
        print(self.inventory)

    def show_raw_positions(self):
        print(self.raw_positions)

    def show_historical_positions(self):
        print(self.historical_positions)
