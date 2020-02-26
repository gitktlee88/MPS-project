from math_func import StudentDB

import pytest




# db = None
# def setup_module(nodule):
#     print('------setup------')
#     global db
#     db = StudentDB()
#     db.connect('data.json')
#
# def teardown_module(nodule):
#     print('------teardown------')
#     db.close()

# def test_scott_data():
#     db = StudentDB()  # init class
#     db.connect('data.json')
#     scott_data = db.get_data('Scott')
#     assert scott_data['id'] == 1
#     assert scott_data['name'] == 'Scott'
#     assert scott_data['result'] == 'pass'
#
# def test_mark_data():
#     db = StudentDB()  # init class
#     db.connect('data.json')
#     scott_data = db.get_data('Mark')
#     assert scott_data['id'] == 2
#     assert scott_data['name'] == 'Mark'
#     assert scott_data['result'] == 'fail'


@pytest.fixture(scope='module')  # default scope=function , module, session
def db():
    print('------setup------')
    db = StudentDB()
    db.connect('data.json')
    # return db
    yield db
    print('------teardown------')
    db.close()

# def test_scott_date():
def test_scott_data(db):
    # db = StudentDB()  # init class
    # db.connect('data.json')
    scott_data = db.get_data('Scott')
    assert scott_data['id'] == 1
    assert scott_data['name'] == 'Scott'
    assert scott_data['result'] == 'pass'

# def test_mark_date():
def test_mark_data(db):
    # db = StudentDB()  # init class
    # db.connect('data.json')
    scott_data = db.get_data('Mark')
    assert scott_data['id'] == 2
    assert scott_data['name'] == 'Mark'
    assert scott_data['result'] == 'fail'
