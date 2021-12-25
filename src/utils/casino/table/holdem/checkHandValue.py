from typing import List

from src.utils.poker.Card import Card


def isRoyalFlush(cards: List[Card]) -> bool:
    royalFlushCards: List[Card] = [
        Card(3, 10),
        Card(3, 11),
        Card(3, 12),
        Card(3, 13),
        Card(3, 1)
    ]
    for i in range(0, 5):
        if cards[i] != royalFlushCards[i]:
            return False
    return True


def isStraightFlush(cards: List[Card]) -> bool:
    cards = cards[:]
    for card in cards:
        if card.rank == 1:
            card.rank = 14
    previousCard = cards[0]
    for i in range(1, 5):
        if (previousCard.rank + 1) != cards[i].rank:
            return False
        if previousCard.suit != cards[i].suit:
            return False
        previousCard = cards[i]

    return True

def tokenizeTheCards(cards: List[Card]) -> List[List[Card]]:
    tokenizedCards: List[List[Card]] = []
    for card in cards:
        tokenized = False
        for tokenizedCard in tokenizedCards:
            if tokenizedCard[0].rank == card.rank:
                tokenizedCard.append(card)
                tokenized = True
                continue
        if not tokenized:
            tokenizedCards.append([card])
    return tokenizedCards


def isFourOfAKing(cards: List[Card]) -> bool:
    tokenizedCards = tokenizeTheCards(cards)

    if len(tokenizedCards) > 2:
        return False
    for tokenizedCard in tokenizedCards:
        if len(tokenizedCard) == 4:
            return True
    return False

def isFullHouse(cards: List[Card]) -> bool:
    tokenizedCards = tokenizeTheCards(cards)
    if len(tokenizedCards) > 2:
        return False
    for tokenizedCard in tokenizedCards:
        if len(tokenizedCard) == 3:
            return True
    return False

def isFlush(cards: List[Card]) -> bool:
    suit = cards[0].suit
    for card in cards:
        if card.suit != suit:
            return False
    return True

def isStraight(cards: List[Card]) -> bool:
    cards = cards[:]
    for card in cards:
        if card.rank == 1:
            card.rank = 14
    for i in range(1, 5):
        if (cards[i].rank - 1) != cards[i-1].rank:
            return False
    return True

def isThreeOfTheKing(cards: List[Card]) -> bool:
    tokenizedCards = tokenizeTheCards(cards)
    if len(tokenizedCards) > 3:
        return False
    for tokenizedCard in tokenizedCards:
        if len(tokenizedCard) == 3:
            return True
    return False

def isTwoPair(cards: List[Card]) -> bool:
    tokenizedCards = tokenizeTheCards(cards)
    return len(tokenizedCards) == 3

def isPair(cards: List[Card]) -> bool:
    tokenizedCards = tokenizeTheCards(cards)
    return len(tokenizedCards) == 4
