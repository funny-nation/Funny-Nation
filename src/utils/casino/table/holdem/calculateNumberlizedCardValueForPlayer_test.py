from src.utils.casino.table.holdem.calculateNumberlizedCardValueForPlayer import calculateNumberlizedCardValueForPlayer
from typing import List
from src.utils.poker.Card import Card

board: List[Card] = [
    Card(1, 3),
    Card(1, 5),
    Card(1, 7),
    Card(2, 7),
    Card(1, 6)
]

hand1: List[Card] = [
    Card(1, 4),
    Card(1, 9)
]

hand2: List[Card] = [
    Card(3, 7),
    Card(2, 5)
]

hand3: List[Card] = [
    Card(1, 1),
    Card(2, 1)
]

def test_():
    assert calculateNumberlizedCardValueForPlayer(hand1, board) == 80706050403
    assert calculateNumberlizedCardValueForPlayer(hand2, board) == 60707070505
    assert calculateNumberlizedCardValueForPlayer(hand3, board) == 51407060503