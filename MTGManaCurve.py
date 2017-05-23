''''MTG mana curve generator'''
import itertools
import argparse
import random


def keep(hand):
    '''Works out whether you to keep hand'''
    if len(hand) == 7:
        return 1 < hand.count('Land') < 7
    elif len(hand) == 6:
        return 1 < hand.count('Land') < 6
    else:
        return 'Land' in hand and hand.count('Land') != len(hand)


def mtgtest(deck, turns=5, number=10000, on_draw=False):
    '''Tests deck'''
    results = 0.0
    randint = random.randint
    for _ in range(number):
        cdeck = deck.copy()
        hsize = 7
        keeping = False
        while not keeping and hsize > 2:
            hand = [cdeck.pop(randint(0, len(cdeck) - 1)) for i in range(hsize)]
            keeping = keep(hand)
            hsize -= 1
        lands = 0
        for turn in range(1, turns+1):
            if turns != 0 or on_draw:
                hand.append(cdeck.pop(randint(0, len(cdeck) - 1)))
            if 'Land' in hand:
                lands += 1
                hand.remove('Land')
            mana = lands
            for cost in sorted(filter(lambda x: x != 'Land',
                                      hand.copy()), reverse=True):
                if cost <= mana:
                    hand.remove(cost)
                    mana -= cost
            results += (lands - mana)/turn
    return results/turns/number


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
    results = []
    options = ['Land'] + list(range(1, args.turns + 1))
    decks_so_far = 0
    try:
        for deck in itertools.combinations_with_replacement(options,
                                                            r=args.size):
            decks_so_far += 1
            print(deck.count('Land'), decks_so_far)
            result = mtgtest(list(deck), turns=args.turns, number=args.number)
            if len(results) < args.decks or result > min(results,
                                                         key=lambda x: x[0])[0]:
                results.append([float(result), deck])
            if len(results) > args.decks:
                results.remove(min(results, key=lambda x: x[0]))
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    for i in list(sorted(results, key=lambda x: x[0]))[-10:]:
        print('Result:', i[0])
        for cmc in sorted(set(i[1]), key=str):
            print('CMC %s: %s' % (cmc, i[1].count(cmc)))


if __name__ == '__main__':
    main()
    # import cProfile as profile
    # profile.run('main()', sort='tottime')
