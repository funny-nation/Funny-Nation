from src.utils.casino.Casino import Casino
from datetime import datetime


def printCasinoLog(casino: Casino, log):
    msgTable = 'Current active tables: '
    for tableID in casino.tables:
        msgTable += str(tableID) + ' '

    msgOnlinePlayer = 'Current active players: '

    for playerID in casino.onlinePlayer:
        msgOnlinePlayer += str(playerID) + ' '

    log.info(msgTable)
    log.info(msgOnlinePlayer)

