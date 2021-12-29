from typing import List
import copy
from src.utils.poker.Card import Card
import src.utils.casino.table.holdem.checkHandValue as checkHandValue
from src.utils.casino.table.holdem.sortCards import sortCards

"""
For numberlization of cards
There are 11 digit


10101010101
^  
First digit represent hand value
    0 for high card
    1 for pair
    2 for two pair
    3 for three of a kind
    4 for straight
    5 for flush
    6 for full house
    7 for four of a kind
    8 for straight flush
    9 for Royal flush
    
10101010101
 ^^
Second and third digit represent first card rank value

10101010101
   ^^
4th and 5th digit represent second card rank value

10101010101
     ^^
6th and 7th digit represent third card rank value

10101010101
       ^^
8th and 9th digit represent 4th card rank value

10101010101
         ^^
9th and 10th digit represent 5th card rank value
"""

def numberlizeCards(cards: List[Card]):
    sortCards(cards)
    handValue = getHandValue(cards)
    numberlizedCards = 0
    times = 1
    for i in range(0, 5):
        numberlizedCards += (getCardValue(cards[i]) * times)
        times *= 100
    numberlizedCards += (handValue * times)
    return numberlizedCards

def getCardValue(card: Card):
    if card.rank == 1:
        return 14
    return card.rank

def getHandValue(cards: List[Card]) -> int:

    if checkHandValue.isRoyalFlush(cards):
        return 9
    if checkHandValue.isStraightFlush(cards):
        return 8
    if checkHandValue.isFourOfAKind(cards):
        return 7
    if checkHandValue.isFullHouse(cards):
        return 6
    if checkHandValue.isFlush(cards):
        return 5
    if checkHandValue.isStraight(cards):
        return 4
    if checkHandValue.isThreeOfAKind(cards):
        return 3
    if checkHandValue.isTwoPair(cards):
        return 2
    if checkHandValue.isPair(cards):
        return 1
    return 0





