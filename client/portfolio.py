class Portfolio:
    def __init__(self):
        self._inventory = dict()  # keyed by symbol
        self._historical_positions = set()
        self._raw_positions = set()

    # position is a tuple ()
    def add_position(self, position):
        self._historical_positions.add(position)
        self._raw_positions.add(position)

    def remove_position(self, position):
        self._raw_positions.remove(position)

    def compute_inventory(self):
        self._inventory.clear()
        for item in self._raw_positions:
            current_position = self._inventory.get(item.get_symbol())
            if current_position is None:
                self._inventory[item.get_symbol()] = item.get_qty()
            else:
                self._inventory[item.get_symbol()] = current_position + item.get_qty()

    def get_inventory(self):
        return self._inventory

    def get_raw_positions(self):
        return self._raw_positions

    def get_historical_positions(self):
        return self._historical_positions

    def show_inventory(self):
        print(self._inventory)
