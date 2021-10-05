import os
import configparser
import sys

sys.path.append(os.path.dirname(__file__) + '/')
import checkBalance
import getLeaderBoard

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/../../../config.ini')
commandPrefix = config['command']['prefix'] + ' '
commandPrefixLen = len(commandPrefix)


async def messageParser(self, message, db):
    if message.content[:commandPrefixLen] != commandPrefix:
        return
    command = message.content[3:]
    if command == "余额":
        await checkBalance.checkBalance(message, db)
    if command == "富豪榜":
        await getLeaderBoard.getLeaderBoard(self, message, db)
