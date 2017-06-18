''''MTG mana curve generator'''
import multiprocessing
import itertools
import random


def keep(hand):
    '''Works out whether you to keep hand'''
    return 1 < hand.count(0) < len(hand)


def mtgtest(deck, turns=5, number=10000, on_draw=False):
    '''Tests deck'''
    results = 0.0
    randint = random.randint
    for _ in range(number):
        cdeck = deck.copy()
        hsize = 7
        keeping = False
        hand = []
        while not keeping and hsize > 2:
            cdeck.extend(hand)
            hand = [cdeck.pop(randint(0, len(cdeck) - 1)) for i in range(hsize)]
            keeping = keep(hand)
            hsize -= 1
        lands = 0
        for turn in range(1, turns+1):
            if turn != 1 or on_draw:
                hand.append(cdeck.pop(randint(0, len(cdeck) - 1)))
            if 0 in hand:
                lands += 1
                hand.remove(0)
            mana = lands
            for cost in sorted(hand, reverse=True):
                if cost != 0 and cost <= mana:
                    hand.remove(cost)
                    mana -= cost
            results += (lands - mana)/turn
    return results/turns/number


def run(turns, number, size, decks, threads=4):
    '''Parse commandline arguments and run program'''
    results = []
    options = list(range(0, turns + 1))
    decks_so_far = 0
    decks = []
    try:
        for deck in itertools.combinations_with_replacement(options,
                                                            r=size):
            decks_so_far += 1
            result = mtgtest(list(deck), turns=turns, number=number)
            if len(results) < decks or result > min(results)[0]:
                results.append([float(result), deck])
                print(deck.count(0), decks_so_far, result)
            if len(results) > decks:
                results.remove(min(results))
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    for i in list(sorted(results))[-10:]:
        print('Result:', i[0])
        for cmc in sorted(set(i[1])):
            if cmc == 0:
                print('Land: %s' % (i[1].count(cmc)))
            else:
                print('CMC %s: %s' % (cmc, i[1].count(cmc)))
