from src.utils.casino.table.holdem.numberlizeCards import numberlizeCards
from typing import List
from src.utils.poker.Card import Card

royalFlushCards: List[Card] = [
    Card(3, 11),
    Card(3, 10),
    Card(3, 1),
    Card(3, 13),
    Card(3, 12)
]

highCards: List[Card] = [
    Card(2, 3),
    Card(3, 5),
    Card(2, 6),
    Card(1, 4),
    Card(3, 11)
]

fullHouseCards: List[Card] = [
    Card(2, 3),
    Card(3, 3),
    Card(1, 5),
    Card(2, 5),
    Card(1, 3)
]

fourOfAKindCards: List[Card] = [
    Card(0, 3),
    Card(3, 1),
    Card(1, 3),
    Card(2, 3),
    Card(3, 3)
]

threeOfAKindCard: List[Card] = [
    Card(3, 4),
    Card(2, 4),
    Card(1, 4),
    Card(1, 5),
    Card(2, 6)
]
twoPairCards: List[Card] = [
    Card(3, 4),
    Card(2, 5),
    Card(2, 4),
    Card(1, 5),
    Card(2, 6)
]

twoPairCards2: List[Card] = [
    Card(3, 4),
    Card(2, 2),
    Card(2, 4),
    Card(1, 2),
    Card(2, 3)
]
pairCards: List[Card] = [
    Card(3, 4),
    Card(2, 5),
    Card(2, 6),
    Card(1, 6),
    Card(2, 7)
]

straightFlushCards: List[Card] = [
    Card(2, 3),
    Card(2, 4),
    Card(2, 5),
    Card(2, 6),
    Card(2, 7)
]

flushCards: List[Card] = [
    Card(2, 3),
    Card(2, 5),
    Card(2, 7),
    Card(2, 11),
    Card(2, 1)
]
straightCards: List[Card] = [
    Card(1, 4),
    Card(3, 5),
    Card(1, 6),
    Card(2, 7),
    Card(1, 8)
]

def test_():
    assert numberlizeCards(royalFlushCards) == 91413121110
    assert numberlizeCards(straightFlushCards) == 80706050403
    assert numberlizeCards(fourOfAKindCards) == 70303030314
    assert numberlizeCards(fullHouseCards) == 60303030505
    assert numberlizeCards(flushCards) == 51411070503
    assert numberlizeCards(straightCards) == 40807060504
    assert numberlizeCards(threeOfAKindCard) == 30404040605
    assert numberlizeCards(twoPairCards) == 20505040406
    assert numberlizeCards(twoPairCards2) == 20404020203
    assert numberlizeCards(pairCards) == 10606070504
    assert numberlizeCards(highCards) == 1106050403