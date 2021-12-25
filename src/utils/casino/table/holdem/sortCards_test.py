from src.utils.casino.table.holdem.sortCards import sortCards
from src.utils.poker.Card import Card
import random

def test_():
    cards = [
        Card(1, 3),
        Card(2, 5),
        Card(1, 1),
        Card(1, 11),
        Card(1, 12)
    ]
    random.shuffle(cards)
    sortCards(cards)
    assert cards[0].rank == 3
    assert cards[1].rank == 5
    assert cards[2].rank == 11
    assert cards[3].rank == 12
    assert cards[4].rank == 1