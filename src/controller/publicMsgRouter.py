import os
import configparser
import re

from src.Storage import Storage
from src.controller.routes.checkBalance import checkBalance
from src.controller.routes.getLeaderBoard import getLeaderBoardTop10
from src.controller.routes.checkCashFlow import checkCashFlow, checkCashFlowWithFilter
from src.controller.routes.holdem.newGame import newHoldemGame
from src.controller.routes.holdem.rise import holdemRise
from src.controller.routes.transferMoney import transferMoney
from src.controller.routes.sendGift import sendGift
from src.controller.routes.buyVIP import buyVIP
from src.controller.routes.lottery.initiateLottery import initiateLottery

from src.controller.routes.blackJack.newBlackJackGame import newBlackJackGame
from src.controller.routes.startGame import gameStartByTableOwner
from src.controller.routes.pauseGame import pauseGame
from src.controller.routes.joinGame import joinGame
from src.controller.routes.quitGame import quitGame
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.routes.addMoneyAdmin import addMoneyAdmin
from src.controller.routes.minusMoneyAdmin import minusMoneyAdmin
from src.controller.routes.luckyMoney.sendLuckyMoney import sendLuckyMoney
from src.controller.routes.eventAward.publishAward import publishAward
from src.controller.routes.eventAward.closeEvent import closeEvent
import src.Robot

from discord import Client, Message, TextChannel
from pymysql import Connection

from src.utils.casino.Casino import Casino

from src.utils.readConfig import getGeneralConfig

generalConfig = getGeneralConfig()
commandPrefix = generalConfig['command']['prefix'] + ' '
commandPrefixLen = len(commandPrefix)


async def publicMsgRouter(self: Client, message: Message, db: Connection, storage: Storage):
    """
    Parse message
    Identify whether it is a command to this bot, or just a normal message
    :param storage:
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
    if re.match(f"^转账 [0-9]+\.?[0-9]* \<\@\!?[0-9]+\>$", command):
        await transferMoney(self, db, message, command)
        return
    if re.match(f"^印钞 [0-9]+\.?[0-9]* \<\@\!?[0-9]+\>$", command):
        await addMoneyAdmin(self, db, message, command, storage.adminRole)
        return
    if re.match(f"^抢劫 [0-9]+\.?[0-9]* \<\@\!?[0-9]+\>$", command):
        await minusMoneyAdmin(self, db, message, command, storage.adminRole)
        return
    if re.match(f"^领奖 .+ [0-9]+$", command):
        moneyInPot = re.findall(f"^领奖 (.+) ([0-9]+)$", command)[0][1]
        await publishAward(self, message, db, int(moneyInPot) * 100, message.id, storage.adminRole, command)
        return
    if re.match(f"^关闭领奖 .+$", command):
        await closeEvent(self, message, db, message.id, storage.adminRole, command)

    if re.match(f"^送 .+ \<\@\!?[0-9]+\>$", command):
        await sendGift(self, db, message, command, storage.announcementChannel)
        return

    if re.match(f"^买vip$", command):
        await buyVIP(self, message, db, storage.announcementChannel, storage.vipRoles)
        return

    if re.match(f"^发红包 [0-9]+ [0-9]+$", command):
        moneyAndQuan: tuple = re.findall(f"^发红包 ([0-9]+) ([0-9]+)$", command)[0]

        await sendLuckyMoney(self, message, db, int(moneyAndQuan[0]) * 100, int(moneyAndQuan[1]))
        return

    if re.match(f"^开局21点 [0-9]+\.?[0-9]*$", command):
        await newBlackJackGame(self, message, db, command, storage.casino, storage.gamePlayerWaiting)
        return

    if re.match(f"^开局德州扑克$", command):
        await newHoldemGame(self, message, db, storage.casino, storage.gamePlayerWaiting)
        return
    if re.match(f"^加注 [0-9]+$", command):
        await holdemRise(self, message, db, command, storage.casino, storage.gamePlayerWaiting)

    if re.match(f"^加入$", command):
        await joinGame(self, message, db, storage.casino, storage.gamePlayerWaiting)
        return
    if re.match(f"^退出$", command):
        await quitGame(self, message, db, storage.casino)
        return
    if re.match(f"^开$", command):
        await gameStartByTableOwner(self, message, storage.casino, storage.gamePlayerWaiting, db)
        return
    if re.match(f"^掀桌$", command):
        await pauseGame(self, message, storage.casino, db, storage.gamePlayerWaiting)
        return
    if re.match(f"^抽奖 .+ [\\-0-9]+ [\\-0-9]+$", command):
        await initiateLottery(self, message, db, command)
        return
