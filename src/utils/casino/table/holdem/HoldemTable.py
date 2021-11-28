from src.utils.casino.table.Table import Table
from discord import Message, Member
from src.utils.casino.table.holdem.getTheHighHand import getTheHighHand
from src.utils.poker.Poker import Poker


class HoldemTable(Table):
    def __init__(self, inviteMessage: Message or None, owner: Member or None):
        Table.__init__(self, 'holdem', inviteMessage, 10, owner)
        self.mainPot = 0
        self.poker = Poker()
        self.sidePots = {}
        self.board = []
        self.whoRise: Member or None = None

    def gameStart(self):
        self.poker.shuffle()
        self.gameStarted = True
        for playerID in self.players:
            self.players[playerID]['cards'] = []
            self.players[playerID]['cards'].append(self.poker.getACard())
            self.players[playerID]['cards'].append(self.poker.getACard())

    def flop(self):
        self.board.append(self.poker.getACard())
        self.board.append(self.poker.getACard())
        self.board.append(self.poker.getACard())

    def turnAndRiver(self):
        self.board.append(self.poker.getACard())

    def rise(self, playerID, money):


    def call(self, playerID):

    def allIn(self, playerID):

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
        winners: list = getTheHighHand(self)

def test_():
    holdemTable = HoldemTable(None, None)
    holdemTable.addPlayer(1)
    holdemTable.addPlayer(2)
    holdemTable.addPlayer(3)
    holdemTable.addPlayer(4)
    holdemTable.gameStart()
