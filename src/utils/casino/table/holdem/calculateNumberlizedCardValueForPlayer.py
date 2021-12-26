from typing import List
from itertools import combinations
from src.utils.casino.table.holdem.numberlizeCards import numberlizeCards
from src.utils.poker.Card import Card


def calculateNumberlizedCardValueForPlayer(hand: List[Card], board: List[Card]):
    totalCards = hand + board
    highestNumberlizedCardValue = 0
    for possibleHand in combinations(totalCards, 5):
        currentNumberlizedCardValue = numberlizeCards(list(possibleHand))
        if currentNumberlizedCardValue > highestNumberlizedCardValue:
            highestNumberlizedCardValue = currentNumberlizedCardValue
    return highestNumberlizedCardValue