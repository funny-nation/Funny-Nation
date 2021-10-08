import os
import configparser
import sys

sys.path.append(os.path.dirname(__file__) + '/')
import checkBalance
import getLeaderBoard
import checkCashFlow

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/../../../config.ini')
commandPrefix = config['command']['prefix'] + ' '
commandPrefixLen = len(commandPrefix)


async def messageParser(self, message, db):
    """
    Parse message
    Identify whether it is a command to this bot, or just a normal message
    :param self: Discord's client object
    :param message: Message obj
    :param db: Database object
    :return: None
    """
    if message.content[:commandPrefixLen] != commandPrefix:
        return
    command = message.content[3:]
    if command == "余额":
        await checkBalance.checkBalance(message, db)
    if command == "富豪榜":
        await getLeaderBoard.getLeaderBoard(self, message, db)
    if command == "流水记录":
        await checkCashFlow.checkCashFlow(self, message, db)
