from src.utils.casino.table.Table import Table
from discord import Message, Member
from src.utils.poker.Poker import Poker
from typing import List
from src.utils.casino.table.holdem.calculateNumberlizedCardValueForPlayer import calculateNumberlizedCardValueForPlayer

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
        self.allInedWithNewBat = False
        self.numberOfPlayersNotFold = 0
        self.numberOfPlayersNotFoldOrAllIn = 0

    def gameStart(self):
        self.poker.shuffle()
        self.gameStarted = True
        playersIDs = list(self.players.keys())
        previousPlayerID = playersIDs[-1]
        for playerID in self.players:
            self.numberOfPlayersNotFold += 1
            self.numberOfPlayersNotFoldOrAllIn += 1
            self.mainPot += self.ante
            self.players[previousPlayerID]['next'] = playerID
            previousPlayerID = playerID
            self.players[playerID]['fold'] = False
            self.players[playerID]['allIn'] = False
            self.players[playerID]['moneyInvested'] = self.ante
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
        if self.whosTurn is None:
            return True
        nextPlayerID: int = self.players[self.whosTurn]['next'] + 0
        currentPlayerID: int = self.whosTurn + 0
        def exeWhenEndOfRound():
            if self.numberOfPlayersNotFoldOrAllIn == 1:
                self.whosTurn = None
        def cleanCurrentPot():
            self.currentBet = 0
            self.whoBet = None
            for playerID in self.players:
                self.players[playerID]['tempPot'] = 0
            whosTurn = self.owner.id
            while self.players[whosTurn]['fold'] or self.players[whosTurn]['allIn']:
                whosTurn = self.players[whosTurn]['next']
            self.whosTurn = whosTurn

        while self.players[nextPlayerID]['fold'] or self.players[nextPlayerID]['allIn']:
            nextPlayerID = self.players[nextPlayerID]['next'] # Find the next player
            if nextPlayerID == currentPlayerID:
                self.whosTurn = None
                exeWhenEndOfRound()
                return True
        self.whosTurn = nextPlayerID
        if self.whoBet is None: # No one bet, means this round would end til nextPlayerID is back to owner or player right of the owner.
            startBetID = self.owner.id
            while self.players[startBetID]['fold'] or self.players[startBetID]['allIn']:
                startBetID = self.players[startBetID]['next']
            if nextPlayerID == startBetID:
                cleanCurrentPot()
                exeWhenEndOfRound()
                return True
            else:
                return False
        else:
            if nextPlayerID == self.whoBet:
                cleanCurrentPot()
                exeWhenEndOfRound()
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
        moneyToPot = money + self.getAmountOfMoneyToCall(playerID)
        self.mainPot += moneyToPot
        self.players[playerID]['moneyInvested'] += moneyToPot
        self.currentBet += money
        self.players[playerID]['tempPot'] = self.currentBet
        self.whoBet = playerID

        return

    def callOrCheck(self, playerID):
        moneyInvest = self.getAmountOfMoneyToCall(playerID)
        self.mainPot += moneyInvest
        self.players[playerID]['moneyInvested'] += moneyInvest
        self.players[playerID]['tempPot'] = self.currentBet
        if self.allInedWithNewBat is True:
            self.whoBet = playerID
            self.allInedWithNewBat = False
        return

    def getAmountOfMoneyToCall(self, playerID):
        return self.currentBet - self.players[playerID]['tempPot']


    def allIn(self, playerID, money: int):
        self.players[playerID]['allIn'] = True
        self.numberOfPlayersNotFoldOrAllIn -= 1
        self.players[playerID]['moneyInvested'] += money
        amountOfMoneyToCall = self.getAmountOfMoneyToCall(playerID)
        self.mainPot += money
        self.players[playerID]['tempPot'] += money
        if amountOfMoneyToCall < money:
            self.currentBet += money - amountOfMoneyToCall
            self.whoBet = playerID
            self.allInedWithNewBat = True
        return

    def fold(self, playerID):
        self.numberOfPlayersNotFold -= 1
        self.numberOfPlayersNotFoldOrAllIn -= 1
        self.players[playerID]['fold'] = True


    def numberlizeTheCardForPlayers(self):
        for userID in self.players:
            if not self.players[userID]['fold']:
                self.players[userID]['cardsNumberlizedValue'] = calculateNumberlizedCardValueForPlayer(self.players[userID]['cards'], self.board)


    def getSortedPlayerIDList(self):
        userIDs: List[int] = list(self.players.keys())

        for i in range(0, len(self.players)):
            for j in range(i + 1, len(self.players)):
                if self.players[userIDs[i]]['moneyInvested'] > self.players[userIDs[j]]['moneyInvested']:
                    temp = userIDs[i]
                    userIDs[i] = userIDs[j]
                    userIDs[j] = temp

        return userIDs



    def getWinner(self) -> List[int]:
        highestNumberlizedCardsValue = 0
        winnerPlayers = []
        for userID in self.players:
            if not self.players[userID]['fold']:
                numberlizedCardsValue = calculateNumberlizedCardValueForPlayer(self.players[userID]['cards'], self.board)
                if numberlizedCardsValue > highestNumberlizedCardsValue:
                    highestNumberlizedCardsValue = numberlizedCardsValue
                    winnerPlayers = [userID]
                elif numberlizedCardsValue == highestNumberlizedCardsValue:
                    winnerPlayers.append(userID)

        return winnerPlayers



    def end(self):
        """
        get winners,
        calculate money to players
        :return:
        {
            playerID: money,
            playerID: money
        }
        """
        winners = self.getWinner()




