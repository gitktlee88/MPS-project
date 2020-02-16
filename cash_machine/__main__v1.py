"""cash_machine.

A cash machine that, when given a banknote will release coins for an equivalent value.
The machine has the following coins available: 0.20£, 0.50£, 1£, 2£.
The machine accepts the following banknotes: 5£, 10£, 20£.
There are 2 operations available:
    ● an operator can load more coins in the machine
    ● a customer can exchange a banknote

"""
import argparse
import sys
import time

import logging

# Create and configure logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

#logging.basicConfig(filename = "LumberJack.log")      # default is Warning
logging.basicConfig(stream = sys.stdout,
                    level = logging.DEBUG,
                    format = LOG_FORMAT)

logger = logging.getLogger()

# A dictionary for available coins and bank notes
coins_notes = {
    ('0.20',): 0,   # 0.20
    ('0.50',): 0,   # 0.50
    ('1',): 0,    # 1
    ('2',): 0,    # 2
    ('5',): 0,    # 5
    ('10',): 0,   # 10
    ('20',): 0,   # 20
}

def parse_args(argv=None):
    """Parse command line arguments.
    :param list argv: Args to parse.
    """
    parser = argparse.ArgumentParser(prog='cash_machine')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'{parser.prog} 0.1',
    )
    parser.add_argument(
        '--verbose',
        help='Verbose output',
        default=False,
        action='store_true',
        dest='verbose',
    )
    parser.add_argument(
        'input_file',
        metavar='input',
        type=str,
        # nargs='+',
        help='input file name.  ex, input.txt'
    )
    return parser.parse_args(argv)

def store_cash(num, typeOfCoin):
    """ Store given number of coins into the dictionary.
    :param list num: number of coins, typeOfCoin: type of coin.
    """
    for key in coins_notes:
        if key == (typeOfCoin,):
            coins_notes[key] += num
    output_cash()

def output_cash():
    """ Display current status of coins and banknotes
    :param list None.
    """
    res = ''
    money =[(key, val) for (key,), val in coins_notes.items()]

    for key in money:
        res += str(key[1]) + ' ' + key[0] + '£, '

    print(res[:-2])

def exchange_to_coins(notes):
    """ Exchange a note to coins.
    :param list notes: banknote.
    """
    sumOfcoins = 0

    for key, val in coins_notes.items():
        if key[0].isdigit():
            k = int(key[0])
            if k < 3:             # 1£ or 2£
                sumOfcoins += val*k
        else:
            k = float(key[0])     # 0.20£ or 0.50£
            sumOfcoins += val*k

    if not notes:
        print('{} cannot be exchanged'.format(notes))
        return

    do_calc(notes, sumOfcoins)
    output_cash()

def do_calc(notes, totalCoins):
    """ Calculate the number of coins in the order of high-to-low.
    :param list notes: banknote, totalCoins: sum of available coins.
    """
    # [('0.20', 10), ('0.50', 0), ('1', 10), ('2', 21), ('5', 0), ('10', 0), ('20', 0)]
    money =[(key, val) for (key,), val in coins_notes.items()]
    # exchange = ["CANNOT EXCHANGE"]  lkt
    sumOfcoins = 0
    coins = []  # [(int, str), ...]
    if totalCoins < notes:
        print("CANNOT EXCHANGE")
        return

    # Iterate coins_notes(dictionary) in reversed order like
    # {('2',): 0, ('1',): 0, ('0.50',): 0, ('0.20',): 0}
    for i, t in enumerate(money[-4::-1]):   # t = (key, val)
        if i == 0:   # 2£
            twosum = t[1]*int(t[0])
            if notes <= twosum:
                coins.append((notes//2, t[0]))
                coins_notes[(t[0],)] -= notes//2
                sumOfcoins += int(t[0])*(notes//2)
                if sumOfcoins == notes:
                    break
            elif twosum != 0:
                coins.append((t[1], t[0]))
                sumOfcoins += twosum
                coins_notes[(t[0],)] -= t[1]
        elif i == 1:   # 1£
            onesum = t[1]*int(t[0])
            if notes <= onesum and sumOfcoins == 0:
                coins.append((notes, t[0]))
                coins_notes[(t[0],)] -= notes
                sumOfcoins += int(t[0])*(notes)
                break
            elif onesum != 0:
                remain = notes - sumOfcoins
                if remain <= onesum:
                    do_func(t[0], t[1], remain, coins, sumOfcoins)
                    break
                elif onesum != 0:
                    coins.append((t[1], t[0]))
                    sumOfcoins += onesum
                    coins_notes[(t[0],)] -= t[1]

        elif i == 2:   # 0.50£
            fiftysum = t[1]*float(t[0])
            if notes <= fiftysum and sumOfcoins == 0:
                coins.append((notes*2, t[0]))
                coins_notes[(t[0],)] -= notes*2
                sumOfcoins += float(t[0])*notes*2
                break
            elif fiftysum != 0:
                remain = notes - sumOfcoins
                if remain <= fiftysum:
                    do_func(t[0], t[1], remain, coins, sumOfcoins)
                    break
                elif fiftysum != 0:
                    coins.append((t[1], t[0]))
                    sumOfcoins += fiftysum
                    coins_notes[(t[0],)] -= t[1]
        else:   # 0.20£
            twentysum = t[1]*float(t[0])
            if notes <= twentysum and sumOfcoins == 0:
                coins.append((notes*5, t[0]))
                coins_notes[(t[0],)] -= notes*5
                sumOfcoins += float(t[0])*notes*5
                break
            elif twentysum != 0:
                remain = notes - sumOfcoins
                if remain <= twentysum:
                    do_func(t[0], t[1], remain, coins, sumOfcoins)
                    break
                elif twentysum != 0:
                    coins.append((t[1], t[0]))
                    sumOfcoins += twentysum
                    coins_notes[(t[0],)] -= t[1]

    if not len(coins):
        print("CANNOT EXCHANGE")
    else:
        coins_notes[(str(notes),)] += 1   # put notes in the dictionary
        result = ''
        for v in coins:
            result += str(v[0]) + ' ' + v[1] + '£, '
        print(result)

def do_func(typeOfcoin, numOfcoins, remain, coins, sumOfcoins):
    for i in range(1, numOfcoins+1):
        if remain == i*float(typeOfcoin):
            coins.append((i, typeOfcoin))
            coins_notes[(typeOfcoin,)] -= i
            sumOfcoins += remain
            break
    return

def main(argv=None):
    """Program entry point.
    ● reads the text file with commands
    ● will output each command received
    ● after each command will output the number of coins and banknote 
    available in the cash machine. 
    E.g.: = 5 0.20£, 10 0.50£, 5 1£, 3 2£, 0 5£, 6 10£, 2 20£

    :param list argv: Command line arguments.
    """
    # Parse arguments
    args = parse_args(argv)

    if not args.verbose:
        logger.disable()

    # Load input.txt and store comands in a list
    commands = []
    try:
        with open(args.input_file, 'r') as infile:
            for line in infile:
                commands.append(line.lstrip(">").split())
    except EnvironmentError:
        logger.error('No such file or directory')
    except Exception as e:
        logger.error(e)

    for command in commands:
        if command[0].upper() == "LOAD":
            print('\n> {} {} {}\n'.format(command[0], command[1], command[2]))
            # store_cash(int(command[1]), 'c' + command[2].lstrip('0|.'))
            store_cash(int(command[1]), command[2])

        elif command[0].upper() == "EXCHANGE":
            print('\n> {} {}\n'.format(command[0], command[1]))
            exchange_to_coins(int(command[1]))

        else:
            logger.error('No command found in input data')

if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
