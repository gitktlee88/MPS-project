import pytest
from inventory import Inventory, InvalidQuantityException, NoSpaceException, ItemNotFoundException

# 1 Features and test planning
#
# 2 Before writing first integration test with the requirement,
#   - let's flesh out the smaller components a bit to figure out what would be
#     our inputs and output, function signatures and other system design elements.


@pytest.fixture
def ten_stock_inventory():
    """Returns an inventory with some test stock items"""
    inventory = Inventory(20)
    inventory.add_new_stock('Puma Test', 100.00, 8)
    inventory.add_new_stock('Reebok Test', 25.50, 2)
    return inventory


@pytest.fixture
def no_stock_inventory():
    """Returns an empty inventory that can store 10 items"""
    return Inventory(10)


def test_default_inventory():
    """Test that the default limit is 100"""
    inventory = Inventory()
    assert inventory.limit == 100
    assert inventory.total_items == 0


def test_custom_inventory_limit():
    """Test that we can set a custom limit"""
    inventory = Inventory(limit=25)
    assert inventory.limit == 25
    assert inventory.total_items == 0


# def test_add_new_stock_success(no_stock_inventory):
#     no_stock_inventory.add_new_stock('Test Jacket', 10.00, 5)
#     assert no_stock_inventory.total_items == 5
#     assert no_stock_inventory.stocks['Test Jacket']['price'] == 10.00
#     assert no_stock_inventory.stocks['Test Jacket']['quantity'] == 5
#
#
# @pytest.mark.parametrize('name,price,quantity,exception', [
#     ('Test Jacket', 10.00, 0, InvalidQuantityException(
#         'Cannot add a quantity of 0. All new stocks must have at least 1 item')),
#     ('Test Jacket', 10.00, 25, NoSpaceException(
#         'Cannot add these 25 items. Only 10 more items can be stored'))
# ])
# def test_add_new_stock_bad_input(name, price, quantity, exception):
#     inventory = Inventory(10)
#     try:
#         inventory.add_new_stock(name, price, quantity)
#     except (InvalidQuantityException, NoSpaceException) as inst:
#         # First ensure the exception is of the right type
#         assert isinstance(inst, type(exception))
#         # Ensure that exceptions have the same message
#         assert inst.args == exception.args
#         # print(exception.args)
#     else:
#         pytest.fail("Expected error but found none")

@pytest.mark.parametrize('name,price,quantity,exception', [
    ('Test Jacket', 10.00, 0, InvalidQuantityException(
        'Cannot add a quantity of 0. All new stocks must have at least 1 item')),
    ('Test Jacket', 10.00, 25, NoSpaceException(
        'Cannot add these 25 items. Only 10 more items can be stored')),
    ('Test Jacket', 10.00, 5, None)
])
def test_add_new_stock(no_stock_inventory, name, price, quantity, exception):
    try:
        no_stock_inventory.add_new_stock(name, price, quantity)
    except (InvalidQuantityException, NoSpaceException) as inst:
        # First ensure the exception is of the right type
        assert isinstance(inst, type(exception))
        # Ensure that exceptions have the same message
        assert inst.args == exception.args
        # print(exception.args)
    else:
        assert no_stock_inventory.total_items == quantity
        assert no_stock_inventory.stocks[name]['price'] == price
        assert no_stock_inventory.stocks[name]['quantity'] == quantity


# ...
# Note the extra parameters, we need to set our expectation of
# what totals should be after our remove action
@pytest.mark.parametrize('name,quantity,exception,new_quantity,new_total', [
    ('Puma Test', 0,
     InvalidQuantityException(
         'Cannot remove a quantity of 0. Must remove at least 1 item'),
        0, 0),
    ('Not Here', 5,
     ItemNotFoundException(
         'Could not find Not Here in our stocks. Cannot remove non-existing stock'),
        0, 0),
    ('Puma Test', 25,
     InvalidQuantityException(
         'Cannot remove these 25 items. Only 8 items are in stock'),
     0, 0),
    ('Puma Test', 5, None, 3, 5)
])
def test_remove_stock(ten_stock_inventory, name, quantity, exception,
                      new_quantity, new_total):
    try:
        ten_stock_inventory.remove_stock(name, quantity)
    except (InvalidQuantityException, NoSpaceException, ItemNotFoundException) as inst:
        assert isinstance(inst, type(exception))
        assert inst.args == exception.args
    else:
        assert ten_stock_inventory.stocks[name]['quantity'] == new_quantity
        assert ten_stock_inventory.total_items == new_total

# if __name__ == "__main__":
#     test_buy_and_sell_nikes_adidas()
