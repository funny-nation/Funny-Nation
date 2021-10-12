from Card import Card
import random


class Poker:
    def __init__(self):
        self.cards = []
        for suit in range(0, 4):
            for rank in range(1, 14):
                newCards = Card(suit, rank)
                self.cards.append(newCards)

    def shuffle(self):
        random.shuffle(self.cards)

    def getACard(self):
        """
        Get a card from
        :return:
        """
        if len(self.cards) != 0:
            return self.cards.pop()
        return None

def test_Poker():
    poker = Poker()
    poker.shuffle()
    card = poker.getACard()
    assert card is not None
