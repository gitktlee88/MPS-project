import pytest
from invent import Invent, InvalidQuantity, NoSpaces, ItemNotFound


@pytest.fixture
def no_stock_invent():
    """Returns empty invent that can store 10 items"""
    return Invent(10)


@pytest.fixture
def ten_stock_invent():
    """Returns an inventory with some test stock items"""
    invent = Invent(20)
    invent.add_new_stock('Puma Test', 80.00, 7)
    invent.add_new_stock('Puma Test', 100.00, 9)
    invent.add_new_stock('Reebok Test', 25.50, 2)
    # print(invent.stocks['Puma Test'])
    # print(invent.total_items)
    return invent


def test_default_invent():
    """Test that default limit is 100"""
    invent = Invent()
    assert invent.limit == 100
    assert invent.total_items == 0


def test_add_new_stock_success(no_stock_invent):
    no_stock_invent.add_new_stock('Test Jacket', 10.00, 5)
    assert no_stock_invent.total_items == 5
    assert no_stock_invent.stocks['Test Jacket']['price'] == 10.00
    assert no_stock_invent.stocks['Test Jacket']['quantity'] == 5


@pytest.mark.parametrize('name,price,quantity,exception', [
    ('Test Jacket', 10.00, 0, InvalidQuantity('Cannot add 0 quantity')),
    ('Test Jacket', 10.00, 20, NoSpaces('No Spaces are available')),
    ('Test Jacket', 10.00, 5, None)
])
def test_add_new_stock_bad(no_stock_invent, name, price, quantity, exception):
    # invent = Invent(10)
    try:
        # invent.add_new_stock(name, price, quantity)
        no_stock_invent.add_new_stock(name, price, quantity)
    except (InvalidQuantity, NoSpaces) as e:
        assert isinstance(e, type(exception))
        assert e.args == exception.args
    else:
        # pytest.fail("Expected error but not found")
        assert no_stock_invent.total_items == quantity
        assert no_stock_invent.stocks[name]['price'] == price
        assert no_stock_invent.stocks[name]['quantity'] == quantity


@pytest.mark.parametrize('name,quantity,exception,new_quantity,new_total', [
    ('Puma Test', 0, InvalidQuantity('Cannot remove 0 quantity'), 0, 0),
    ('Not Here', 5, ItemNotFound("Could not find 'Not Here' in our stocks."), 0, 0),
    ('Puma Test', 25, InvalidQuantity('Cannot remove these 25 items. Only 9 items are in stock'), 0, 0),
    ('Puma Test', 5, None, 4, 6)
])
def test_remove_stock(ten_stock_invent, name, quantity, exception, new_quantity,
                      new_total):
    try:
        ten_stock_invent.remove_stock(name, quantity)
    except (InvalidQuantity, ItemNotFound) as e:
        assert isinstance(e, type(exception))
        assert e.args == exception.args
    else:
        assert ten_stock_invent.stocks[name]['quantity'] == new_quantity
        assert ten_stock_invent.total_items == new_total
