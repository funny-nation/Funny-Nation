from src.data.poker.Poker import Poker
from src.data.poker.Card import Card


class BlackJackPoker(Poker):

    def __init__(self):
        Poker.__init__(self)

    def compareForBlackJack(self, playerAlphaCards, playerBetaCards) -> int:
        """

        :param playerAlphaCards:
        :param playerBetaCards:
        :return:
        1 for player alpha win
        2 for player beta win
        0 for draw
        """
        rankForPlayerAlpha: int = self.calculateRankBlackJackWithAceAs11(playerAlphaCards)
        rankForPlayerBeta: int = self.calculateRankBlackJackWithAceAs11(playerBetaCards)

        if (rankForPlayerAlpha > 21) and (rankForPlayerBeta <= 21):
            rankForPlayerAlpha = self.calculateRankBlackJack(playerAlphaCards)
            if rankForPlayerAlpha > 21:
                return 2
        if (rankForPlayerAlpha <= 21) and (rankForPlayerBeta > 21):
            rankForPlayerBeta = self.calculateRankBlackJack(playerBetaCards)
            if rankForPlayerBeta > 21:
                return 1
        if (rankForPlayerAlpha > 21) and (rankForPlayerBeta > 21):
            rankForPlayerBeta = self.calculateRankBlackJack(playerBetaCards)
            rankForPlayerAlpha = self.calculateRankBlackJack(playerAlphaCards)
            if (rankForPlayerAlpha > 21) and (rankForPlayerBeta > 21):
                return 0

        if rankForPlayerAlpha > rankForPlayerBeta:
            return 1
        if rankForPlayerAlpha < rankForPlayerBeta:
            return 2

        if len(playerAlphaCards) < len(playerBetaCards):
            return 1
        if len(playerBetaCards) < len(playerAlphaCards):
            return 2

        return 0

    @staticmethod
    def calculateRankBlackJack(cards: [Card]):
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


def test_BlackJack():
    poker = BlackJackPoker()
    poker.shuffle()
    playerAlphaCards = []
    playerBetaCards = []
    while poker.calculateRankBlackJack(playerAlphaCards) < 15:
        playerAlphaCards.append(poker.getACard())

    while poker.calculateRankBlackJack(playerBetaCards) < 15:
        playerBetaCards.append(poker.getACard())

    print("Alpha: ")
    for i in playerAlphaCards:
        print(i.rank)

    print("Beta: ")
    for i in playerBetaCards:
        print(i.rank)

    print("Result: ")
    print(poker.compareForBlackJack(playerAlphaCards, playerBetaCards))
