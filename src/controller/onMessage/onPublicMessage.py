import os
import configparser
import re

from src.controller.onMessage.checkBalance import checkBalance
from src.controller.onMessage.getLeaderBoard import getLeaderBoardTop10
from src.controller.onMessage.checkCashFlow import checkCashFlow
from src.controller.onMessage.transferMoney import transferMoney

from src.controller.onMessage.blackJack.newBlackJackGame import newBlackJackGame
from src.controller.onMessage.blackJack.hit import blackJackHit
from src.controller.onMessage.blackJack.stay import blackJackStay
from src.controller.onMessage.startGame import gameStartByTableOwner
from src.controller.onMessage.pauseGame import pauseGame

from src.controller.onMessage.liveGift import liveGift
from src.controller.onMessage.joinGame import joinGame

from discord import Client, Message
from pymysql import Connection

from util.casino.Casino import Casino

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/../../../config.ini')
commandPrefix = config['command']['prefix'] + ' '
commandPrefixLen = len(commandPrefix)


async def onPublicMessage(self: Client, message: Message, db: Connection, casino: Casino):
    """
    Parse message
    Identify whether it is a command to this bot, or just a normal message
    :param casino:
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
    command: str = message.content[3:]
    if re.match(f"^余额$", command):
        await checkBalance(message, db)
        return
    if re.match(f"^富豪榜$", command):
        await getLeaderBoardTop10(self, message, db)
        return
    if re.match(f"^账单$", command):
        await checkCashFlow(self, message, db)
        return
    if re.match(f"^账单 .+", command):
        await checkCashFlow(self, message, db)
        return
    if re.match(f"^转账 [0-9]+\.?[0-9]* \<\@\![0-9]+\>$", command):
        await transferMoney(self, db, message, command)
        return
    if re.match(f"^礼物 (.+) [1-9][0-9]* \<\@\![0-9]+\>$", command):
        await liveGift(self, db, message, command)
        return

    if re.match(f"^开局21点 [0-9]+\.?[0-9]*$", command):
        await newBlackJackGame(self, message, db, command, casino)
        return
    if re.match(f"^要牌$", command):
        await blackJackHit(self, message, casino)
        return
    if re.match(f"^开牌$", command):
        member = message.author
        await blackJackStay(self, message, casino, member.id, member)
        return

    if re.match(f"^加入$", command):
        await joinGame(self, message, db, casino)
        return
    if re.match(f"^开$", command):
        await gameStartByTableOwner(self, message, casino)
        return
    if re.match(f"^掀桌$", command):
        await pauseGame(self, message, casino)
        return
