
# cash_machine
This repository contains a simple cash_machine application.
A given banknote will release coins for an equivalent value.

The machine has the following coins available: 0.20£, 0.50£, 1£, 2£. The machine accepts the following banknotes: 5£, 10£, 20£.
There are 2 operations available:

  ● an operator can load more coins in the machine
  ● a customer can exchange a banknote

You are given a text file which contains two types of instructions:


## Usage
Check out the repo and navigate to `MPS-project/`.

Execute as follows to show usage:
```
python -m cash_machine -h
usage: cash_machine [-h] [-v] [--verbose]

positional arguments:
  input          input file name. ex, input.txt

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  --verbose      Verbose output
```

## Examples
```
$ python -m cash_machine input.txt
```
```
$ python -m cash_machine --verbose input.txt
```


## Tests
This application benefits from `pytest` tests. To run the tests:
```
$ pytest ./tests/test_main.py -v -s
or,
$ pytest ./tests/test_main.py
```
```
================== test session starts ================================
platform win32 -- Python 3.7.1, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: D:\MPS
collected 8 items

tests\test_main.py ........                                      [100%]

======================= 8 passed in 0.10s =============================
```

## Environment
If you need to set up a working environment the following files can be used:

- `requirements.txt` - Classic pip requirements file.
