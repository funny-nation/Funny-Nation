import os
import configparser
import re

from src.controller.onMessage.checkBalance import checkBalance
from src.controller.onMessage.getLeaderBoard import getLeaderBoardTop10
from src.controller.onMessage.checkCashFlow import checkCashFlow, checkCashFlowWithFilter
from src.controller.onMessage.holdem.newGame import newHoldemGame
from src.controller.onMessage.holdem.rise import holdemRise
from src.controller.onMessage.transferMoney import transferMoney
from src.controller.onMessage.sendGift import sendGift
from src.controller.onMessage.buyVIP import buyVIP

from src.controller.onMessage.blackJack.newBlackJackGame import newBlackJackGame
from src.controller.onMessage.startGame import gameStartByTableOwner
from src.controller.onMessage.pauseGame import pauseGame

from src.controller.onMessage.liveGift import liveGift
from src.controller.onMessage.joinGame import joinGame
from src.controller.onMessage.quitGame import quitGame
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.onMessage.addMoneyAdmin import addMoneyAdmin

from discord import Client, Message, TextChannel
from pymysql import Connection

from src.utils.casino.Casino import Casino

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
commandPrefix = config['command']['prefix'] + ' '
commandPrefixLen = len(commandPrefix)


async def onPublicMessage(self: Client, message: Message, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting, announcementChannel: TextChannel, vipRoles: dict, admin: list):
    """
    Parse message
    Identify whether it is a command to this bot, or just a normal message
    :param gamePlayerWaiting:
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
    command: str = message.content[commandPrefixLen:]
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
        await checkCashFlowWithFilter(self, message, db, command)
        return
    if re.match(f"^转账 [0-9]+\.?[0-9]* \<\@\![0-9]+\>$", command):
        await transferMoney(self, db, message, command)
        return
    if re.match(f"^管理员加钱 [0-9]+\.?[0-9]* \<\@\![0-9]+\>$", command):
        await addMoneyAdmin(self, db, message, command, admin)
        return
    if re.match(f"^礼物 (.+) [1-9][0-9]* \<\@\![0-9]+\>$", command):
        await liveGift(self, db, message, command)
        return
    if re.match(f"^送 .+ \<\@\![0-9]+\>$", command):
        await sendGift(self, db, message, command, announcementChannel)
        return

    if re.match(f"^买vip$", command):
        await buyVIP(self, message, db, announcementChannel, vipRoles)
        return

    if re.match(f"^开局21点 [0-9]+\.?[0-9]*$", command):
        await newBlackJackGame(self, message, db, command, casino, gamePlayerWaiting)
        return

    if re.match(f"^开局德州扑克$", command):
        await newHoldemGame(self, message, db, casino, gamePlayerWaiting)
        return
    if re.match(f"^加注 [0-9]+$", command):
        await holdemRise(self, message, db, command, casino, gamePlayerWaiting)

    if re.match(f"^加入$", command):
        await joinGame(self, message, db, casino, gamePlayerWaiting)
        return
    if re.match(f"^退出$", command):
        await quitGame(self, message, db, casino)
        return
    if re.match(f"^开$", command):
        await gameStartByTableOwner(self, message, casino, gamePlayerWaiting, db)
        return
    if re.match(f"^掀桌$", command):
        await pauseGame(self, message, casino, db, gamePlayerWaiting)
        return
