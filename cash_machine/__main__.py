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

# logging.basicConfig(filename = "LumberJack.log")      # default is Warning
logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format=LOG_FORMAT)

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


def store_cash(num, type_of_coin):
    """ Store given number of coins into the dictionary.
    :param list num: number of coins, type_of_coin: type of coin.
    """
    for key in coins_notes:
        if key == (type_of_coin,):
            coins_notes[key] += num
    output_cash()


def output_cash():
    """ Display current status of coins and banknotes
    :param list None.
    """
    res = ''
    money = [(key, val) for (key,), val in coins_notes.items()]

    for key in money:
        res += str(key[1]) + ' ' + key[0] + '£, '

    print(res[:-2])


def exchange_to_coins(notes):
    """ Exchange a note to coins.
    :param list notes: banknote.
    """
    total_coins = 0

    for key, val in coins_notes.items():
        if key[0].isdigit():
            k = int(key[0])
            if k < 3:             # 1£ or 2£
                total_coins += val * k
        else:
            k = float(key[0])     # 0.20£ or 0.50£
            total_coins += val * k

    if not notes:
        print('{} cannot be exchanged'.format(notes))
        return

    do_calc(notes, total_coins)
    output_cash()


def do_calc(notes, total_coins):
    """ Calculate the number of coins in the order of high-to-low.
    :param list notes: banknote, total_coins: sum of available coins.
    """
    # [('0.20', 10), ('0.50', 0), ('1', 10), ('2', 21), ('5', 0), ('10', 0), ('20', 0)]
    money = [(key, val) for (key,), val in coins_notes.items()]
    sum_of_coins = 0
    coins = []  # [(int, str), ...]
    if total_coins < notes:
        print("CANNOT EXCHANGE")
        return

    # Iterate coins_notes(dictionary) in reversed order like
    # {('2',): 0, ('1',): 0, ('0.50',): 0, ('0.20',): 0}
    for i, t in enumerate(money[-4::-1]):   # t = (key, val)
        if t[0].isdigit():   # 2£  or 1£ ??
            coinsum = t[1] * int(t[0])
            coinval = int(t[0])
            if int(t[0]) == 2:
                coins_required = notes // 2
            else:
                coins_required = notes
        else:   # 0.50£  or 0.20£
            coinsum = t[1] * float(t[0])
            coinval = float(t[0])
            if float(t[0]) == 0.50:
                coins_required = notes * 2
            else:
                coins_required = notes * 5

        if notes <= coinsum and sum_of_coins == 0:
            coins.append((coins_required, t[0]))
            coins_notes[(t[0],)] -= coins_required
            sum_of_coins += coinval * (coins_required)
            if sum_of_coins == notes:
                break
        elif coinsum != 0:
            # print(notes, sum_of_coins)
            remains = notes - sum_of_coins
            if remains <= coinsum:
                for i in range(1, t[1] + 1):
                    if remains == i * coinval:
                        coins.append((i, t[0]))
                        coins_notes[(t[0],)] -= i
                        sum_of_coins += remains
                        break
            else:
                coins.append((t[1], t[0]))
                sum_of_coins += coinsum
                coins_notes[(t[0],)] -= t[1]

    if not len(coins):
        print("CANNOT EXCHANGE")
    else:
        coins_notes[(str(notes),)] += 1   # put notes in the dictionary
        result = ''
        for v in coins:
            result += str(v[0]) + ' ' + v[1] + '£, '
        print(result)


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
            store_cash(int(command[1]), command[2])

        elif command[0].upper() == "EXCHANGE":
            print('\n> {} {}\n'.format(command[0], command[1]))
            exchange_to_coins(int(command[1]))

        else:
            logger.error('No command found in input data')


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
