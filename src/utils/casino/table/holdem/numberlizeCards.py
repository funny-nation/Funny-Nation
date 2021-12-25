from typing import List

from src.utils.poker.Card import Card
import src.utils.casino.table.holdem.checkHandValue as checkHandValue

"""
For numberlization of cards
There are 11 digit


10101010101
^  
First digit represent hand value
    0 for highcard
    1 for pair
    2 for two pair
    3 for three of the king
    4 for straight
    5 for flush
    6 for full house
    7 for four of a king
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
    return

def getHandValue(cards: List[Card]) -> int:
    if checkHandValue.isRoyalFlush(cards):
        return 9
    if checkHandValue.isStraightFlush(cards):
        return 8
    if checkHandValue.isFourOfAKing(cards):
        return 7
    if checkHandValue.isFullHouse(cards):
        return 6
    if checkHandValue.isFlush(cards):
        return 5
    if checkHandValue.isStraight(cards):
        return 4
    if checkHandValue.isThreeOfTheKing(cards):
        return 3
    if checkHandValue.isTwoPair(cards):
        return 2
    if checkHandValue.isPair(cards):
        return 1
    return 0





