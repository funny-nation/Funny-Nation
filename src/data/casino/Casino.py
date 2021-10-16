import random
from src.data.casino.table.BlackJackTable import BlackJackTable


class Casino:
    def __init__(self):
        self.tables = {}

    def getTableNumber(self):
        return len(self.tables)

    def createBlackJackTableByID(self, tableID, money):
        """
        Return true if table created success
        Return false if someone is using this table
        :param tableID:
        :param money:
        :return:
        """
        if tableID in self.tables:
            return False
        self.tables[tableID] = BlackJackTable(money)
        return True

    def getTable(self, tableID):
        if tableID not in self.tables:
            return None
        return self.tables[tableID]
