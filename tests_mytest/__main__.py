"""cashMachine.

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
logging.basicConfig(stream=sys.stdout,
                    level = logging.DEBUG,
                    format = LOG_FORMAT)

logger = logging.getLogger()

# from cashMachine import db_mysql_v2 as db
# mydb = db.MySQLdb_connection()

# from logbook import Logger, StreamHandler
# StreamHandler(sys.stdout).push_application()
# logger = Logger('CashMachine')


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
    parser = argparse.ArgumentParser(prog='cashMachine')
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
    return parser.parse_args(argv)

def store_cash(num, typeOfCash):
    for key in coins_notes:
        if key == (typeOfCash,):
            coins_notes[key] += num
    output_cash()

def output_cash():
    res = ''
    money =[(key, val) for (key,), val in coins_notes.items()]

    for key in money:
        res += str(key[1]) + ' ' + key[0] + '£, '

    print(res[:-2])

def exchange_to_coins(notes):
    sumOfCoins = 0

    for key, val in coins_notes.items():
        if key[0].isdigit():
            k = int(key[0])
            if k < 3:             # 1£ or 2£
                sumOfCoins += val*k
        else:
            k = float(key[0])     # 0.20£ or 0.50£
            sumOfCoins += val*k

    if not notes:
        print('{} cannot be exchanged'.format(notes))
        return

    # print(sumOfCoins, notes)
    do_calc(notes, sumOfCoins)
    output_cash()


def do_calc(notes, totalCoins):
    # [('0.20', 10), ('0.50', 0), ('1', 10), ('2', 21), ('5', 0), ('10', 0), ('20', 0)]
    money =[(key, val) for (key,), val in coins_notes.items()]
    exchange = ["CANNOT EXCHANGE"]
    sumOfCoins = 0
    coins = []  # [(int, str), ...]
    if totalCoins < notes:
        print(exchange[0])
        return

    for i, t in enumerate(money[-4::-1]):   # t = (key, val)
        if i == 0:   # 2£
            twosum = t[1]*int(t[0])
            if notes <= twosum:
                coins.append((notes//2, t[0]))
                coins_notes[(t[0],)] -= notes//2
                sumOfCoins += int(t[0])*(notes//2)
                break
            elif twosum != 0:
                coins.append((t[1], t[0]))
                sumOfCoins += twosum
                coins_notes[(t[0],)] -= t[1]
        elif i == 1:   # 1£
            onesum = t[1]*int(t[0])
            if notes <= onesum and sumOfCoins == 0:
                coins.append((notes, t[0]))
                coins_notes[(t[0],)] -= notes
                sumOfCoins += int(t[0])*(notes)
                break
            elif onesum != 0:
                remain = notes - sumOfCoins
                if remain <= onesum:
                    for i in range(1, t[1]+1):
                        if remain == i*int(t[0]):
                            coins.append((i, t[0]))
                            coins_notes[(t[0],)] -= i
                            sumOfCoins += remain
                            break
                elif onesum != 0:
                    coins.append((t[1], t[0]))
                    sumOfCoins += onesum
                    coins_notes[(t[0],)] -= t[1]

        elif i == 2:   # 0.50£
            fiftysum = t[1]*float(t[0])
            if notes <= fiftysum and sumOfCoins == 0:
                coins.append((notes*2, t[0]))
                coins_notes[(t[0],)] -= notes*2
                sumOfCoins += float(t[0])*notes*2
                break
            elif fiftysum != 0:
                remain = notes - sumOfCoins
                if remain <= fiftysum:
                    for i in range(1, t[1]+1):
                        if remain == i*float(t[0]):
                            coins.append((i, t[0]))
                            coins_notes[(t[0],)] -= i
                            sumOfCoins += remain
                            break
                elif fiftysum != 0:
                    coins.append((t[1], t[0]))
                    sumOfCoins += fiftysum
                    coins_notes[(t[0],)] -= t[1]
        else:   # 0.20£
            twentysum = t[1]*float(t[0])
            if notes <= twentysum and sumOfCoins == 0:
                coins.append((notes*5, t[0]))
                coins_notes[(t[0],)] -= notes*5
                sumOfCoins += float(t[0])*notes*5
                break
            elif twentysum != 0:
                remain = notes - sumOfCoins
                if remain <= twentysum:
                    for i in range(1, t[1]+1):
                        if remain == i*float(t[0]):
                            coins.append((i, t[0]))
                            coins_notes[(t[0],)] -= i
                            sumOfCoins += remain
                            break
                elif twentysum != 0:
                    coins.append((t[1], t[0]))
                    sumOfCoins += twentysum
                    coins_notes[(t[0],)] -= t[1]

    if coins:
        exchange.append(coins)
        # print(coins)
        # print(coins_notes)

    if len(exchange) == 1:
        print(exchange[0])
    else:
        coins_notes[(str(notes),)] += 1   # put notes in the dictionary
        result = ''
        for t in exchange[1:]:
            for v in t:
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
        with open('input.txt', 'r') as infile:
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
