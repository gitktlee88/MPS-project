from mydic_func import MySQLDBcon

import pytest

@pytest.fixture(scope='module')  # default scope=function , module, session
def db():
    print('------setup------')
    db = MySQLDBcon()
    db.connect('mydic')
    # return db
    yield db
    print('------teardown------')
    # db.close()

def test_11test_data(db):
    sql = "SELECT * FROM mydic.words WHERE word = '11test';"
    r = db.query_db(sql)
    print(r)
    # assert scott_data['result'] == 'pass'
def test_APWD_data(db):
    sql = "SELECT * FROM mydic.words WHERE word = 'A\.PWD';"
    r = db.query_db(sql)
    print(r)
    # assert scott_data['result'] == 'pass'
