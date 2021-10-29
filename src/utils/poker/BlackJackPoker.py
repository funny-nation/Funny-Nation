import copy
from typing import List

from src.utils.poker.Poker import Poker
from src.utils.poker.Card import Card


class BlackJackPoker(Poker):

    def __init__(self):
        Poker.__init__(self)

    @staticmethod
    def isBusted(self, cards: List[Card]):
        return self.calculateRankBlackJackWithAceAs1(cards) > 21

    @staticmethod
    def calculateValue(cards: List[Card]) -> int:
        """
        Calculate cards values.
        :param cards:
        :return: int
        if busted, return 0
        """
        values = []
        copyedCards = copy.deepcopy(cards)
        continueLoop = True
        while continueLoop:
            continueLoop = False
            valueTemp = 0
            for card in copyedCards:
                if card.rank >= 10:
                    valueTemp += 10
                    continue
                if card.rank == 1:
                    valueTemp += 1
                    if not continueLoop:
                        card.rank = 0
                        continueLoop = True
                    continue
                if card.rank == 0:
                    valueTemp += 11
                    continue

                valueTemp += card.rank
            values.append(valueTemp)

        bestValue = 0
        for value in values:
            if (value > bestValue) and (value <= 21):
                bestValue = value
        return bestValue


    @staticmethod
    def calculateRankBlackJackWithAceAs1(cards: [Card]):
        rank = 0
        for card in cards:
            if card.rank < 10:
                rank += card.rank
            else:
                rank += 10
        return rank

    @staticmethod
    def calculateRankBlackJackWithAceAs11(cards: [Card]):
        rank = 0
        for card in cards:
            if card.rank < 10:
                if card.rank == 1:
                    rank += 11
                else:
                    rank += card.rank
            else:
                rank += 10
        return rank


def test_CalculateValueBlackJack():
    cards = [Card(0, 11), Card(0, 1)]
    assert BlackJackPoker.calculateValue(cards) == 21


def test_CalculateValueDoubleAce():
    cards = [Card(0, 1), Card(0, 1)]
    assert BlackJackPoker.calculateValue(cards) == 12


def test_CalculateValue777():
    cards = [Card(0, 7), Card(0, 7), Card(0, 7)]
    assert BlackJackPoker.calculateValue(cards) == 21


def test_CalculateValueAce56():
    cards = [Card(0, 1), Card(0, 5), Card(0, 6)]
    assert BlackJackPoker.calculateValue(cards) == 12


def test_CalculateValueBust():
    cards = [Card(0, 11), Card(0, 5), Card(0, 12)]
    assert BlackJackPoker.calculateValue(cards) == 0


def test_CalculateValueAce():
    cards = [Card(0, 11), Card(0, 1), Card(0, 12)]
    assert BlackJackPoker.calculateValue(cards) == 21


def test_CalculateValueBustAce():
    cards = [Card(0, 11), Card(0, 1), Card(0, 5), Card(0, 12)]
    assert BlackJackPoker.calculateValue(cards) == 0
