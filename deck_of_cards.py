import random
from collections import namedtuple

def initialize_deck():
    cardfaces = []
    colors = ['red', 'yellow', 'green', 'blue']
    special = ['reverse', 'skip', 'draw2']
    deck = ['W+4', 'W+4', 'W+4', 'W+4', 'WC', 'WC', 'WC', 'WC']

    for i in range(0, 10):
        cardfaces.append(str(i))
    for spcl in special:
        cardfaces.append(spcl)
    for color in colors:
        for i in range(13):
            card = (color + "_" + cardfaces[i])
            deck.append(card)
            if cardfaces[i] != '0':
                deck.append(card)
    #shuffling and dealing cards to players
    p1 = []
    p2 = []
    random.shuffle(deck)
    for i in range(0, 14, 2):
        p1.append(deck.pop(i))
        p2.append(deck.pop(i + 1))
    return deck, p1, p2
