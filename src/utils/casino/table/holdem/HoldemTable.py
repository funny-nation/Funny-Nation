from src.utils.casino.table.Table import Table
from discord import Message, Member
from src.utils.poker.Poker import Poker
from src.utils.poker.HoldemScoreDetector import HoldemScoreDetector

class HoldemTable(Table):
    def __init__(self, inviteMessage: Message or None, owner: Member or None, scoreDetector: HoldemScoreDetector):
        Table.__init__(self, 'holdem', inviteMessage, 10, owner)
        self.mainPot = 0
        self.poker = Poker()
        self.sidePots = {}
        self.board = []
        self.whoBet: int or None = None
        self.whosTurn: int or None = None
        self.ante = 500
        self.numberOfPlayersNotFold = 0
        self._scoreDetector: HoldemScoreDetector = scoreDetector
        self.playersCards = {}
        self.communityCards = []


    def gameStart(self):
        self.poker.shuffle()
        self.gameStarted = True
        playersIDs = list(self.players.keys())
        previousPlayerID = playersIDs[-1]
        for playerID in self.players:
            self.numberOfPlayersNotFold += 1
            self.players[previousPlayerID]['next'] = playerID
            previousPlayerID = playerID
            self.players[playerID]['fold'] = False
            self.players[playerID]['cards'] = []
            self.players[playerID]['cards'].append(self.poker.getACard())
            self.players[playerID]['cards'].append(self.poker.getACard())



    def toNext(self) -> bool:
        """

        :return:
        Return True if round is over, available for a new public card
        Return False if the rund is not overed yet.
        """
        nextPlayerID: int = self.players[self.whosTurn]['next']
        while self.players[nextPlayerID]['fold']:
            nextPlayerID = self.players[nextPlayerID]['next']
        if self.whoBet is None:
            self.whosTurn = nextPlayerID
            return nextPlayerID == self.owner.id


    def viewCards(self, playerID):
        return self.players[playerID]['cards']

    def flop(self):
        self.board.append(self.poker.getACard())
        self.board.append(self.poker.getACard())
        self.board.append(self.poker.getACard())

    def turnOrRiver(self):
        self.board.append(self.poker.getACard())

    def rise(self, playerID, money):
        return

    def callOrCheck(self, playerID):
        return

    def allIn(self, playerID):
        return

    def fold(self, playerID):
        self.numberOfPlayersNotFold -= 1
        self.players[playerID]['fold'] = True

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
