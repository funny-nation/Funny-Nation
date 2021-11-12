from typing import List

from src.utils.casino.table.Table import Table
from src.utils.poker.BlackJackPoker import BlackJackPoker
from src.utils.poker.Card import Card
from discord import Message, Member


class BlackJackTable(Table):

    def __init__(self, money: int, inviteMessage: Message or str, maxPlayer, owner: Member or str):
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

    def gameStartWithoutCards(self) -> bool:
        if self.getPlayerCount() == 1:
            return False
        self.poker.shuffle()
        for playerID in self.players:
            self.players[playerID]['cards'] = []
            self.players[playerID]['stay'] = False
        self.gameStarted = True
        return True


    def viewCards(self, playerID: int) -> [Card]:
        return self.players[playerID]['cards']

    def hit(self, playerID) -> Card:
        card: Card = self.poker.getACard()
        self.players[playerID]['cards'].append(card)
        return card

    def blackBackgroundHit(self, playerID, suit, rank) -> Card:
        card: Card = Card(suit, rank)
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
        rank: int = BlackJackPoker.calculateRankBlackJackWithAceAs1(cards)
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
        highHandVal: int = BlackJackPoker.calculateValue(self.viewCards(highHand[0]))
        highHandCards: List[Card] = self.viewCards(playerList[0])
        for i in range(1, len(playerList)):
            cardsCompareTo: List[Card] = self.viewCards(playerList[i])
            valueOfCardsCompareTo: int = BlackJackPoker.calculateValue(cardsCompareTo)
            if valueOfCardsCompareTo > highHandVal:
                highHand = [playerList[i]]
                highHandVal = valueOfCardsCompareTo
                highHandCards = cardsCompareTo
                continue
            if valueOfCardsCompareTo == highHandVal:
                if (highHandVal == 21) and (len(cardsCompareTo) < len(highHandCards)):
                    highHand = [playerList[i]]
                    highHandVal = valueOfCardsCompareTo
                    highHandCards = cardsCompareTo
                    continue
                elif (highHandVal == 21) and (len(cardsCompareTo) == len(highHandCards)):
                    highHand.append(playerList[i])
                    continue
                elif highHandVal < 21:
                    highHand.append(playerList[i])
                    continue

        return highHand


def test_BlackJackTable():
    table = BlackJackTable(10, 'test', 3, "test")
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


def test_anotherBlackJackTable():
    table = BlackJackTable(10, 'test', 3, "test")
    assert table.addPlayer(123) is True
    assert table.addPlayer(456) is True
    assert table.addPlayer(789) is True
    table.gameStartWithoutCards()
    table.blackBackgroundHit(123, 2, 10)
    table.blackBackgroundHit(123, 1, 11)
    table.blackBackgroundHit(456, 0, 12)
    table.blackBackgroundHit(456, 1, 1)
    table.blackBackgroundHit(789, 0, 6)
    table.blackBackgroundHit(789, 0, 7)
    table.blackBackgroundHit(789, 2, 11)
    table.stay(123)
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