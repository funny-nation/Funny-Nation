from src.utils.casino.table.holdem.checkHandValue import isRoyalFlush, isStraightFlush, isFourOfAKind, isFullHouse, isFlush, isStraight, isThreeOfAKind, isTwoPair, isPair

from typing import List

from src.utils.poker.Card import Card

royalFlushCards: List[Card] = [
    Card(3, 10),
    Card(3, 11),
    Card(3, 12),
    Card(3, 13),
    Card(3, 1)
]

straightCards: List[Card] = [
    Card(2, 10),
    Card(3, 11),
    Card(3, 12),
    Card(3, 13),
    Card(3, 1)
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

fourOfAKindCards: List[Card] = [
    Card(2, 3),
    Card(2, 2),
    Card(3, 2),
    Card(1, 2),
    Card(0, 2)
]
fullHouseCards: List[Card] = [
    Card(2, 3),
    Card(1, 3),
    Card(3, 5),
    Card(2, 5),
    Card(1, 5)
]
flushCards2: List[Card] = [
    Card(2, 3),
    Card(2, 5),
    Card(2, 7),
    Card(2, 11),
    Card(2, 1)
]

straightCards2: List[Card] = [
    Card(1, 4),
    Card(3, 5),
    Card(1, 6),
    Card(2, 7),
    Card(1, 8)
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
    Card(2, 4),
    Card(2, 5),
    Card(1, 5),
    Card(2, 6)
]

pairCards: List[Card] = [
    Card(3, 4),
    Card(2, 4),
    Card(2, 5),
    Card(1, 6),
    Card(2, 7)
]

highcard: List[Card] = [
    Card(3, 1),
    Card(2, 3),
    Card(2, 5),
    Card(1, 7),
    Card(2, 9)
]

def test_checkIfRoyalFlush():

    assert isRoyalFlush(royalFlushCards) is True
    assert isRoyalFlush(straightCards) is False

def test_isStraightFlush():

    assert isStraightFlush(straightFlushCards) is True
    assert isStraightFlush(royalFlushCards) is True
    assert isStraightFlush(flushCards) is False


def test_isFourOfAKind():

    assert isFourOfAKind(fourOfAKindCards) is True
    assert isFourOfAKind(fullHouseCards) is False
    assert isFourOfAKind(flushCards2) is False


def test_isFullHouse():
    assert isFullHouse(fullHouseCards) is True
    assert isFullHouse(flushCards) is False
    assert isFullHouse(threeOfAKindCard) is False

def test_isFlush():
    assert isFlush(flushCards) is True
    assert isFlush(fullHouseCards) is False

def test_isStraight():
    assert isStraight(straightCards) is True
    assert isStraight(straightCards2) is True
    assert isStraight(fullHouseCards) is False

def test_isThreeOfAKind():
    assert isThreeOfAKind(threeOfAKindCard) is True
    assert isThreeOfAKind(fullHouseCards) is True
    assert isThreeOfAKind(flushCards) is False

def test_isTwoPair():
    assert isTwoPair(twoPairCards) is True
    assert isTwoPair(pairCards) is False
    assert isTwoPair(highcard) is False

def test_isPair():
    assert isPair(pairCards) is True
    assert isPair(highcard) is False
