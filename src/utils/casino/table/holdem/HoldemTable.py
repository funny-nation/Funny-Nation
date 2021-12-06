from src.utils.casino.table.Table import Table
from discord import Message, Member
from src.utils.poker.Poker import Poker


class HoldemTable(Table):
    def __init__(self, inviteMessage: Message or None, owner: Member or None):
        Table.__init__(self, 'holdem', inviteMessage, 10, owner)
        self.mainPot = 0
        self.poker = Poker()
        self.sidePots = {}
        self.board = []
        self.whoBet: Member or None = None
        self.whosTurn: Member or None = None
        self.ante = 500

    def gameStart(self):
        self.poker.shuffle()
        self.gameStarted = True
        playersIDs = list(self.players.keys())
        previousPlayerID = playersIDs[-1]
        for playerID in self.players:
            self.players[previousPlayerID]['next'] = playerID
            previousPlayerID = playerID
            self.players[playerID]['cards'] = []
            self.players[playerID]['cards'].append(self.poker.getACard())
            self.players[playerID]['cards'].append(self.poker.getACard())


    def flop(self):
        self.board.append(self.poker.getACard())
        self.board.append(self.poker.getACard())
        self.board.append(self.poker.getACard())

    def viewCards(self, playerID):
        return self.players[playerID]['cards']

    def turnAndRiver(self):
        self.board.append(self.poker.getACard())

    def rise(self, playerID, money):
        return

    def call(self, playerID):
        return

    def allIn(self, playerID):
        return

    def fold(self, playerID):
        self.dropPlayer(playerID)

    def end(self):
        """
        get winners,
        calculate money to players
        :return:
        [
            [playerID, money],
            [playerID, money]
        ]
        """


def test_():
    holdemTable = HoldemTable(None, None)
    holdemTable.addPlayer(1)
    holdemTable.addPlayer(2)
    holdemTable.addPlayer(3)
    holdemTable.addPlayer(4)
    holdemTable.gameStart()
    print(holdemTable.players)
