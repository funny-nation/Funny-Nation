from typing import List

from src.utils.poker.Card import Card


def swap(cards: List[Card], positionA, positionB):
    temp = cards[positionA]
    cards[positionA] = cards[positionB]
    cards[positionB] = temp

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


def isFourOfAKind(cards: List[Card]) -> bool:
    tokenizedCards = tokenizeTheCards(cards)

    if len(tokenizedCards) > 2:
        return False
    for tokenizedCard in tokenizedCards:
        if len(tokenizedCard) == 4:
            extraSortIfFourOfAKind(cards, tokenizedCards)
            return True
    return False

def extraSortIfFourOfAKind(cards: List[Card], tokenizedCards: List[List[Card]]):
    kindRank = None
    for tokenizedCard in tokenizedCards:
        if len(tokenizedCard) == 4:
            kindRank = tokenizedCard[0].rank
            break

    for i in range(1, 5):
        if cards[i].rank != kindRank:
            swap(cards, i, 0)
            return


def isFullHouse(cards: List[Card]) -> bool:
    tokenizedCards = tokenizeTheCards(cards)
    if len(tokenizedCards) > 2:
        return False
    for tokenizedCard in tokenizedCards:
        if len(tokenizedCard) == 3:
            extraSortIfFullHouse(cards, tokenizedCards)
            return True
    return False

def extraSortIfFullHouse(cards: List[Card], tokenizedCards: List[List[Card]]):
    kindRank = None
    for tokenizedCard in tokenizedCards:
        if len(tokenizedCard) == 3:
            kindRank = tokenizedCard[0].rank
            break
    placeItAt = 0
    for i in range(2, 5):
        if cards[i].rank != kindRank:
            swap(cards, i, placeItAt)
            placeItAt += 1

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

def isThreeOfAKind(cards: List[Card]) -> bool:
    tokenizedCards = tokenizeTheCards(cards)
    if len(tokenizedCards) > 3:
        return False
    for tokenizedCard in tokenizedCards:
        if len(tokenizedCard) == 3:
            extraSortIfThreeOfAKind(cards, tokenizedCards)
            return True
    return False

def extraSortIfThreeOfAKind(cards: List[Card], tokenizedCards: List[List[Card]]):
    kindRank = None
    for tokenizedCard in tokenizedCards:
        if len(tokenizedCard) == 3:
            kindRank = tokenizedCard[0].rank
            break
    placeItAt = 0
    for i in range(2, 5):
        if cards[i].rank != kindRank:
            swap(cards, i, placeItAt)
            placeItAt += 1

def isTwoPair(cards: List[Card]) -> bool:
    tokenizedCards = tokenizeTheCards(cards)
    if len(tokenizedCards) == 3:
        extraSortIfTwoPair(cards, tokenizedCards)
        return True
    return False

def extraSortIfTwoPair(cards: List[Card], tokenizedCards: List[List[Card]]):
    pairRank = []
    singleRank = None
    for tokenizedCard in tokenizedCards:
        if len(tokenizedCard) == 2:
            pairRank.append(tokenizedCard[0].rank)
        else:
            singleRank = tokenizedCard[0].rank

    for i in range(1, 5):
        if cards[i].rank == singleRank:
            cardTemp = cards[i]
            del cards[i]
            cards.insert(0, cardTemp)
            break

    placeItAt = 1
    for i in range(3, 5):
        if cards[i].rank != pairRank[1]:
            swap(cards, placeItAt, i)
            placeItAt += 1


def isPair(cards: List[Card]) -> bool:
    tokenizedCards = tokenizeTheCards(cards)
    if len(tokenizedCards) == 4:
        extraSortIfPair(cards, tokenizedCards)
        return True
    return False

def extraSortIfPair(cards: List[Card], tokenizedCards: List[List[Card]]):
    pairRank = None
    for tokenizedCard in tokenizedCards:
        if len(tokenizedCard) == 2:
            pairRank = tokenizedCard[0].rank
            break

    for i in range(4, -1, -1):
        if cards[i].rank == pairRank:
            cardTemp = cards[i]
            del cards[i]
            cards.append(cardTemp)
