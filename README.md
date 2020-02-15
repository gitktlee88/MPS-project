
# cashMachine
This repository contains a simple cashMachine application.
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
python -m cashMachine -h
usage: cashMachine [-h] [-v] [--verbose]

positional arguments:
  input          input file name. ex, input.txt

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  --verbose      Verbose output
```

## Examples
```
$ python -m cashMachine input.txt
```
```
$ python -m cashMachine --verbose input.txt
```


## Tests
This application benefits from `pytest` tests. To run the tests:
```bash
$ pytest ./tests/test_main.py -v -s
```

## Environment
If you need to set up a working environment the following files can be used:

- `requirements.txt` - Classic pip requirements file.
