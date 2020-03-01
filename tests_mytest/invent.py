
class ItemNotFound(Exception):
    pass


class NoSpaces(Exception):
    pass


class InvalidQuantity(Exception):
    pass


class Invent:
    def __init__(self, limit=100):
        self.limit = limit
        self.total_items = 0
        self.stocks = {}

    def add_new_stock(self, name, price, quantity):
        if quantity <= 0:
            raise InvalidQuantity('Cannot add {} quantity'.format(quantity))

        if self.limit < self.total_items + quantity:
            raise NoSpaces('No Spaces are available')

        diff_quantity = 0

        for n in self.stocks:
            if name == n:  # already existing ?
                diff_quantity = quantity - self.stocks[name]['quantity']

        self.stocks[name] = {
            'price': price,
            'quantity': quantity
        }

        self.total_items += quantity if diff_quantity == 0 else diff_quantity

    def remove_stock(self, name, quantity):
        if quantity <= 0:
            raise InvalidQuantity('Cannot remove 0 quantity')

        if name not in self.stocks:
            raise ItemNotFound(
                "Could not find '{}' in our stocks.".format(name))

        if self.stocks[name]['quantity'] - quantity <= 0:
            raise InvalidQuantity(
                'Cannot remove these {} items. Only {} items are in stock'.format(
                    quantity, self.stocks[name]['quantity']))

        self.stocks[name]['quantity'] -= quantity
        self.total_items -= quantity
