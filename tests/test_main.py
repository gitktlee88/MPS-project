import time
import pytest
import logging
import cash_machine.__main__ as main
from cash_machine.db_mysql_v2 import MySQLdb_connection
# import pdb; pdb.set_trace()
@pytest.fixture()
def logger():
    logger = logging.getLogger('Some.Logger')
    logger.setLevel(logging.INFO)
    return logger


@pytest.fixture
def exchange_text():
    return [
        ['EXCHANGE', 20],
        ['EXCHANGE', 10]
    ]


def test_exchange_to_coins(exchange_text, capsys):
    print(exchange_text[0][1])
    main.exchange_to_coins(exchange_text[0][1])
    stdout, _ = capsys.readouterr()
    assert '0 0.20£, 0 0.50£, 0 1£, 0 2£, 0 5£, 0 10£, 0 20£' in stdout


def test_logger_with_fixture(logger, caplog):
    logger.info('Hello guys!')
    assert 'Hello guys!' in caplog.text


def test_log_test(caplog):
    main.logger.enabled = True
    main.logger.warning('warning test')
    assert 'warning test' in caplog.text


class TestParseArgs:

    def test_version(self, capsys):
        with pytest.raises(SystemExit):
            main.parse_args(['--version', 'input.txt'])
        stdout, _ = capsys.readouterr()
        assert 'cash_machine' in stdout

    def test_verbose(self):
        args = main.parse_args(['--verbose', 'input.txt'])
        assert args.verbose is True

# content of test_expectation.py


@pytest.mark.parametrize("test_input,expected", [
    (['LOAD', 10, '0.20'], '10 0.20£, 0 0.50£, 0 1£, 0 2£, 0 5£, 0 10£, 0 20£'),
    (['LOAD', 10, '0.50'], '0 0.20£, 10 0.50£, 0 1£, 0 2£, 0 5£, 0 10£, 0 20£')
])
def test_load_input(capsys, test_input, expected):
    main.store_cash(test_input[1], test_input[2])
    stdout, _ = capsys.readouterr()
    assert expected in stdout
    print(stdout)


def test_main(capsys):
    main.main(['--verbose', 'input.txt'])
    stdout, _ = capsys.readouterr()
    expectd_op = '10 0.20£, 10 0.50£, 10 1£, 0 2£, 0 5£, 0 10£, 0 20£'
    expectd_op1 = '1 2£, 8 1£,'
    assert expectd_op in stdout
    assert expectd_op1 in stdout


#  db connection test#

# A list for available coins and bank notes
# @pytest.fixture
def coins_notes():
    return [
        ['0.20', 0],   # 0.20
        ['0.50', 0],   # 0.50
        ['1', 0],      # 1
        ['2', 0],      # 2
        ['5', 0],      # 5
        ['10', 0],     # 10
        ['20', 0]      # 20
    ]


@pytest.fixture(scope='module')  # default scope=function , module, session
def db():
    print('------setup------')
    db = MySQLdb_connection()
    sql = "CREATE DATABASE IF NOT EXISTS %s" % 'mydb'
    db.query_db(sql)
    # return db
    yield db
    print('------teardown------')
    # db.close()


def test_load_mysql(db):
    sql1 = "SELECT 1 FROM mydb.coinsnotes LIMIT 1;"
    result1 = db.query_db(sql1, db_use='mydb')

    if not result1:
        # Create coinsnotes table
        list_data = coins_notes()

        # columns for coinsnotes table
        fields = ("id INT AUTO_INCREMENT PRIMARY KEY,"
                  "coin VARCHAR(5),"
                  "number INT(6)")

        sql = "CREATE TABLE IF NOT EXISTS %s (%s)" % ('mydb.coinsnotes', fields)
        r2 = db.query_db(sql, db_use='mydb')

        for l in list_data:

            sql = "INSERT INTO mydb.coinsnotes (coin, number) VALUES ('%s', %s);" % \
                (l[0], l[1])

            r2 = db.query_db(sql, db_use='mydb')

    sql = "select * from mydb.coinsnotes where coin = 0.20;"
    r2 = db.query_db(sql, db_use='mydb')
    # print(r2)
    expectd_op = (1, '0.20', 0)
    assert expectd_op in r2
