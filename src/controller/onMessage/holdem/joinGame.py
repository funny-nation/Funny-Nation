from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.utils.casino.table.BlackJackTable import BlackJackTable
from discord import User, Client, TextChannel, Member
from src.controller.onMessage.blackJack.gameStart import blackJackGameStart
from pymysql import Connection

from loguru import logger
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.model.blackJackRecordManagement import newBlackJackRecord
from src.utils.casino.Casino import Casino
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting

import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


async def joinHoldemGame(table: HoldemTable, player: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    userInfo: tuple = getUser(db, player.id)
    if userInfo is None:
        await channel.send(f"{player.display_name}，你好像不太够钱")
        return
    if userInfo[1] < 1000:
        await channel.send(f"{player.display_name}，你好像不太够钱")
        return

    if userInfo[0] in casino.onlinePlayer:
        await channel.send("你已经在另一个游戏里了")
        return

    databaseResult = True
    databaseResult = databaseResult and addMoneyToUser(db, userInfo[0], -table.ante)
    databaseResult = databaseResult and addNewCashFlow(db, userInfo[0], -table.ante, config['cashFlowMessage']['holdemAnte'])
    table.mainPot += table.ante

    if not databaseResult:
        await channel.send("数据库炸了，请告诉一下群主")
        logger.error("Database Error while remove money from user")
        return

    if not table.addPlayer(player.id):
        await channel.send("炸了")
        logger.error("Cannot add player to table")
        return
    casino.onlinePlayer.append(userInfo[0])
    await channel.send(f"{player.display_name}，加入")
    logger.info(f"{player.id} join a blackJack table {channel.id}")