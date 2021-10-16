from src.data.casino.table.Table import Table
from data.poker.BlackJackPoker import BlackJackPoker


class BlackJackTable(Table):

    def __init__(self, money):
        Table.__init__(self, 'blackJack')
        self.poker = BlackJackPoker()
        self.money = money

    def gameStart(self):
        if len(self.players) != 2:
            return False
        self.poker.shuffle()
        for playerID in self.players:
            cardA = self.poker.getACard()
            cardB = self.poker.getACard()
            self.players[playerID]['cards'] = [cardA, cardB]
            self.players[playerID]['stay'] = False
        return True

    def viewCards(self, playerID):
        return self.players[playerID]['cards']

    def hit(self, playerID):
        card = self.poker.getACard()
        self.players[playerID]['cards'].append(card)
        return card

    def stay(self, playerID):
        self.players[playerID]['stay'] = True

    def isOver(self):
        for playerID in self.players:
            if not self.players[playerID]['stay']:
                return False
        return True

    def shouldStopHitting(self, playerID):
        """
        Return true if player's rank is not less than 21 with ace as 1 rank
        :param playerID:
        :return:
        """
        cards = self.players[playerID]['cards']
        rank = self.poker.calculateRankBlackJack(cards)
        return rank >= 21

    def endAndGetWinner(self):
        playersArr = []
        for playerID in self.players:
            playersArr.append({
                'id': playerID,
                'cards': self.players[playerID]['cards']
            })
        result = self.poker.compareForBlackJack(playersArr[0]['cards'], playersArr[1]['cards'])
        if result == 1:
            return playersArr[0]['id']
        if result == 2:
            return playersArr[1]['id']
        return None


def test_BlackJackTable():
    table = BlackJackTable(10)
    table.addPlayer(123)
    table.addPlayer(456)
    table.gameStart()
    assert table.isOver() is False
    while not table.shouldStopHitting(123):
        table.hit(123)
    while not table.shouldStopHitting(456):
        table.hit(456)
    table.stay(123)
    assert table.isOver() is False
    table.stay(456)
    assert table.isOver() is True
    print(table.viewCards(123))
    print('----')
    print(table.viewCards(456))
    print('Winner: ')
    print(table.endAndGetWinner())