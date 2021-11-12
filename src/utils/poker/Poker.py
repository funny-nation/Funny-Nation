from typing import List

from src.utils.poker.Card import Card
import random


class Poker:
    def __init__(self):
        self.cards: List[Card] = []
        for suit in range(0, 4):
            for rank in range(1, 14):
                newCards = Card(suit, rank)
                self.cards.append(newCards)

    def shuffle(self):
        random.shuffle(self.cards)

    def getACard(self) -> Card or None:
        """
        Get a card from
        :return:
        """
        if len(self.cards) != 0:
            return self.cards.pop()
        return None

    def getAllCards(self) -> List[Card]:
        return self.cards


def test_Poker():
    poker = Poker()
    poker.shuffle()
    card = poker.getACard()
    assert card is not None
