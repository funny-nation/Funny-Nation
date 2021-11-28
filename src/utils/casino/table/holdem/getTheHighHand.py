from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from typing import List


def getTheHighHand(self: HoldemTable):
    """

    :param self:
    :return: List[winnerID]
    """
    handsValueTable: List[List[int]] = []
    """
    For handsValueTable
    [
        [playerID, cardType, HighCards]
    ]
    cardType: 
        0: zitch
        
    """

    return