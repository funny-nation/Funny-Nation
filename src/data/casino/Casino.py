import random
from src.data.casino.table.BlackJackTable import BlackJackTable
from src.data.casino.table.Table import Table
from discord import Message


class Casino:
    def __init__(self):
        self.tables = {}

    def getTableNumber(self) -> int:
        return len(self.tables)

    def createBlackJackTableByID(self, tableID: int, money: int, inviteMessage: Message) -> bool:
        """
        Return true if table created success
        Return false if someone is using this table
        :param inviteMessage:
        :param tableID:
        :param money:
        :return:
        """
        if tableID in self.tables:
            return False
        self.tables[tableID] = BlackJackTable(money, inviteMessage, 5, inviteMessage.author)
        return True

    def getTable(self, tableID: int) -> Table or None:
        if tableID not in self.tables:
            return None
        return self.tables[tableID]

    def deleteTable(self, tableID: int):
        del self.tables[tableID]

    def getTableByPlayerID(self, playerID: int) -> Table or None:
        for tableID in self.tables:
            table: Table = self.tables[tableID]
            if table.hasPlayer(playerID):
                return table
        return None
