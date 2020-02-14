import time
import pytest
import cashMachine.__main__ as main

@pytest.fixture
def exchange_text():
    return [
        ['EXCHANGE', 20],
        ['EXCHANGE', 10]
    ]

def test_log(capsys):
    main.logger.enabled = True
    main.logger.warning('logger-test')
    stdout, _ = capsys.readouterr()
    assert 'hello-test' not in stdout

def test_log_quiet(capsys):
    main.logger.enabled = False
    main.logger.warning('warning test')
    stdout, _ = capsys.readouterr()
    assert not len(stdout)


class TestParseArgs:

    def test_version(self, capsys):
        with pytest.raises(SystemExit):
            main.parse_args(['--version', 'input.txt'])
        stdout, _ = capsys.readouterr()
        assert 'cashMachine' in stdout

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
