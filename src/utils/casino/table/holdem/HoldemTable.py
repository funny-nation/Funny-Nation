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
        self.whoBet: int or None = None
        self.whosTurn: int = owner.id
        self.ante = 500
        self.currentBet = 0
        self.numberOfPlayersNotFold = 0

    def gameStart(self):
        self.poker.shuffle()
        self.gameStarted = True
        playersIDs = list(self.players.keys())
        previousPlayerID = playersIDs[-1]
        for playerID in self.players:
            self.numberOfPlayersNotFold += 1
            self.mainPot += self.ante
            self.players[previousPlayerID]['next'] = playerID
            previousPlayerID = playerID
            self.players[playerID]['fold'] = False
            self.players[playerID]['tempPot'] = 0
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

        def cleanCurrentPot():
            self.currentBet = 0
            self.whoBet = None
            for playerID in self.players:
                self.players[playerID]['tempPot'] = 0
            whosTurn = self.owner.id
            while self.players[whosTurn]['fold']:
                whosTurn = self.players[whosTurn]['next']
            self.whosTurn = whosTurn

        while self.players[nextPlayerID]['fold']:
            nextPlayerID = self.players[nextPlayerID]['next'] # Find the next player
        self.whosTurn = nextPlayerID
        if self.whoBet is None: # No one bet, means this round would end til nextPlayerID is back to owner.
            if nextPlayerID == self.owner.id:
                cleanCurrentPot()
                return True
            else:
                return False
        else:
            if nextPlayerID == self.whoBet:
                cleanCurrentPot()
                return True
            else:
                return False




    def viewCards(self, playerID):
        return self.players[playerID]['cards']

    def flop(self):
        self.board.append(self.poker.getACard())
        self.board.append(self.poker.getACard())
        self.board.append(self.poker.getACard())

    def turnOrRiver(self):
        self.board.append(self.poker.getACard())

    def rise(self, playerID, money):
        moneyToPot = money + (self.currentBet - self.players[playerID]['tempPot'])
        self.mainPot += moneyToPot
        self.currentBet += money
        self.players[playerID]['tempPot'] = self.currentBet
        self.whoBet = playerID

        return

    def callOrCheck(self, playerID):
        self.mainPot += self.currentBet - self.players[playerID]['tempPot']
        self.players[playerID]['tempPot'] = self.currentBet
        return

    def getAmountOfMoneyToCall(self, playerID):
        return self.currentBet - self.players[playerID]['tempPot']


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


def test_Story1():
    class MemberTest:
        id = 1
    owner = MemberTest()
    holdemTable = HoldemTable(None, owner)
    holdemTable.addPlayer(1)
    holdemTable.addPlayer(2)
    holdemTable.addPlayer(3)
    holdemTable.addPlayer(4)
    holdemTable.addPlayer(5)
    holdemTable.gameStart()
    # Game start
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    # pre-flop (round 1) start
    holdemTable.rise(1, 10000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    holdemTable.rise(3, 20000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.callOrCheck(5)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 1
    holdemTable.callOrCheck(1)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 1
    assert holdemTable.mainPot == 152500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 5
    # Round 1 end
    holdemTable.flop()
    # Round 2 start
    holdemTable.rise(1, 20000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.fold(2)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    holdemTable.fold(3)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.rise(5, 10000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 1
    holdemTable.fold(1)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 4
    assert holdemTable.mainPot == 232500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 2

    # Round 2 end

    holdemTable.turnOrRiver()
    # Round 3 start
    holdemTable.rise(4, 1000000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.callOrCheck(5)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 4
    assert holdemTable.mainPot == 2232500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 2
    # Round 3 end

    holdemTable.turnOrRiver()
    # Round 3 start

    holdemTable.rise(4, 10000000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.fold(5)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 4
    assert holdemTable.mainPot == 12232500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 1
    # End


def test_story2():
    class MemberTest:
        id = 1
    owner = MemberTest()
    holdemTable = HoldemTable(None, owner)
    holdemTable.addPlayer(1)
    holdemTable.addPlayer(2)
    holdemTable.addPlayer(3)
    holdemTable.addPlayer(4)
    holdemTable.addPlayer(5)
    holdemTable.gameStart()
    # Game start
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    # pre-flop (round 1) start
    holdemTable.rise(1, 10000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    holdemTable.rise(3, 20000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.callOrCheck(5)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 1
    holdemTable.callOrCheck(1)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 1
    assert holdemTable.mainPot == 152500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 5
    # Round 1 end
    holdemTable.flop()
    # Round 2 start
    holdemTable.rise(1, 20000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.fold(2)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    holdemTable.fold(3)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.rise(5, 10000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 1
    holdemTable.fold(1)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 4
    assert holdemTable.mainPot == 232500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 2

    # Round 2 end

    holdemTable.turnOrRiver()
    # Round 3 start
    holdemTable.rise(4, 1000000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.callOrCheck(5)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 4
    assert holdemTable.mainPot == 2232500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 2
    # Round 3 end

    holdemTable.turnOrRiver()
    # Round 3 start

    holdemTable.rise(4, 10000000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.callOrCheck(5)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 4
    assert holdemTable.mainPot == 22232500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 2
    # End
