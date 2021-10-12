import os
import configparser
import sys
import re

sys.path.append(os.path.dirname(__file__) + '/')
import checkBalance
import getLeaderBoard
import checkCashFlow
import transferMoney
import playBlackJack

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
    if len(message.content) > 100:
        await message.channel.send("你说的太长了")
        return
    command = message.content[3:]
    if re.match(f"^余额$", command):
        await checkBalance.checkBalance(message, db)
    if re.match(f"^富豪榜$", command):
        await getLeaderBoard.getLeaderBoard(self, message, db)
    if re.match(f"^账单$", command):
        await checkCashFlow.checkCashFlow(self, message, db)
    if re.match(f"^账单 .+", command):
        await checkCashFlow.checkCashFlowWithFilter(self, message, db)
    if re.match(f"^转账 [0-9]+\.?[0-9]* \<\@\![0-9]+\>$", command):
        await transferMoney.transferMoney(self, db, message, command)
    if re.match(f"^玩 21点 [0-9]+\.?[0-9]* \<\@\![0-9]+\>$"):
        await playBlackJack.playBlackJack(self, message, db, command)
