from typing import List

import discord

from src.data.casino.table.Table import Table
from data.poker.BlackJackPoker import BlackJackPoker
from src.data.poker.Card import Card
from discord import Message, Member


class BlackJackTable(Table):

    def __init__(self, money: int, inviteMessage: Message, maxPlayer, owner: Member):
        Table.__init__(self, 'blackJack', inviteMessage, maxPlayer, owner)
        self.poker: BlackJackPoker = BlackJackPoker()
        self.money: int = money

    def gameStart(self) -> bool:
        if self.getPlayerCount() == 1:
            return False
        self.poker.shuffle()
        for playerID in self.players:
            cardA: Card = self.poker.getACard()
            cardB: Card = self.poker.getACard()
            self.players[playerID]['cards'] = [cardA, cardB]
            self.players[playerID]['stay'] = False
        self.gameStarted = True
        return True

    def viewCards(self, playerID: int) -> [Card]:
        return self.players[playerID]['cards']

    def hit(self, playerID) -> Card:
        card: Card = self.poker.getACard()
        self.players[playerID]['cards'].append(card)
        return card

    def stay(self, playerID):
        self.players[playerID]['stay'] = True

    def isOver(self) -> bool:
        for playerID in self.players:
            if not self.players[playerID]['stay']:
                return False
        return True

    def shouldStopHitting(self, playerID) -> bool:
        """
        Return true if player's rank is not less than 21 with ace as 1 rank
        :param playerID:
        :return:
        """
        cards: [Card] = self.players[playerID]['cards']
        rank: int = self.poker.calculateRankBlackJack(cards)
        return rank >= 21

    def endAndGetWinner(self):
        playersArr = []
        for playerID in self.players:
            playersArr.append({
                'id': playerID,
                'cards': self.players[playerID]['cards']
            })
        result: int = self.poker.compareForBlackJack(playersArr[0]['cards'], playersArr[1]['cards'])
        if result == 1:
            return playersArr[0]['id']
        if result == 2:
            return playersArr[1]['id']
        return None

    def getTheHighHand(self) -> List[int]:
        """
        Get the highest hand
        :return:
        A list of winner player id
        """
        playerList: list = list(self.players.keys())
        highHand: list = [playerList[0]]
        for i in range(1, len(playerList)):
            cardsCurrentHighHand: List[Card] = self.viewCards(highHand[0])
            cardsCompareTo: List[Card] = self.viewCards(playerList[i])
            compareResult = self.poker.compareForBlackJack(cardsCurrentHighHand, cardsCompareTo)
            if compareResult == 1:
                continue
            if compareResult == 2:
                highHand = [playerList[i]]
                continue
            if compareResult == 0:
                highHand.append(playerList[i])

        return highHand


def test_BlackJackTable():
    table = BlackJackTable(10, 'discord.Message()', 3)
    assert table.addPlayer(123) is True
    assert table.gameStart() is False
    assert table.addPlayer(456) is True
    assert table.addPlayer(789) is True
    assert table.addPlayer(135) is False
    assert table.gameStart() is True
    assert table.isOver() is False
    while not table.shouldStopHitting(123):
        table.hit(123)
    while not table.shouldStopHitting(456):
        table.hit(456)
    table.stay(123)
    assert table.isOver() is False
    table.stay(456)
    table.stay(789)
    assert table.isOver() is True

    print('\n')
    for card in table.viewCards(123):
        print(card.getString())
    print('----')
    for card in table.viewCards(456):
        print(card.getString())
    print('----')
    for card in table.viewCards(789):
        print(card.getString())
    print('Winner: ')
    print(table.getTheHighHand())
