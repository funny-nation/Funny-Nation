import random
from src.data.casino.table.BlackJackTable import BlackJackTable
from src.data.casino.table.Table import Table


class Casino:
    def __init__(self):
        self.tables = {}

    def getTableNumber(self) -> int:
        return len(self.tables)

    def createBlackJackTableByID(self, tableID: int, money: int) -> bool:
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

    def getTable(self, tableID: int) -> Table or None:
        if tableID not in self.tables:
            return None
        return self.tables[tableID]
