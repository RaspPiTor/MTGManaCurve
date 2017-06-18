'''Runs MTGManaCurve, allows use of cython'''
import argparse
import MTGManaCurve


def main():
    '''Parse commandline arguments and run program'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--turns',
                        help='Number of turns to optimize for, defaults to 5',
                        default=5, type=int)
    parser.add_argument('-n', '--number',
                        help='Number of times to, defaults to 10000',
                        default=10000, type=int)
    parser.add_argument('-s', '--size',
                        help='Deck size, defaults to 60',
                        default=60, type=int)
    parser.add_argument('-d', '--decks',
                        help='How many decks to store, defaults to 10',
                        default=10, type=int)
    args = parser.parse_args()
    MTGManaCurve.run(args.turns, args.number, args.size, args.decks)

if __name__ == '__main__':
    import cProfile as profile
    profile.run('main()', sort='tottime')
