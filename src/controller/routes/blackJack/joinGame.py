from src.utils.casino.table.BlackJackTable import BlackJackTable
from discord import User, Client, TextChannel, Member
from src.controller.routes.blackJack.gameStart import blackJackGameStart
from pymysql import Connection

from loguru import logger
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.model.blackJackRecordManagement import newBlackJackRecord
from src.utils.casino.Casino import Casino
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting

import configparser

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


async def joinBlackJack(table: BlackJackTable, player: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    userInfo: tuple = getUser(db, player.id)
    if userInfo is None:
        moneyNotEnough = str(languageConfig["blackJack"]["moneyNotEnough"])\
            .replace("?@user", f" {player.display_name} ")
        await channel.send(moneyNotEnough)
        return
    if userInfo[1] < table.money:
        moneyNotEnough = str(languageConfig["blackJack"]["moneyNotEnough"])\
            .replace("?@user", f" {player.display_name} ")
        await channel.send(moneyNotEnough)
        return

    if userInfo[0] in casino.onlinePlayer:
        youWereInOtherGame = str(languageConfig["blackJack"]["youWereInOtherGame"])\
            .replace("?@user", f" {player.display_name} ")
        await channel.send(youWereInOtherGame)
        return

    databaseResult = True
    databaseResult = databaseResult and addMoneyToUser(db, userInfo[0], -table.money)
    databaseResult = databaseResult and addNewCashFlow(db, userInfo[0], -table.money, config['cashFlowMessage']['blackJackSpend'])
    databaseResult = databaseResult and newBlackJackRecord(db, userInfo[0], table.money, channel.id, table.uuid)

    if not databaseResult:
        error = str(languageConfig["error"]["dbError"])
        await channel.send(error)
        logger.error("Database Error while remove money from user")
        return

    if not table.addPlayer(player.id):
        error = str(languageConfig["error"]["dbError"])
        await channel.send(error)
        logger.error("Cannot add player to table")
        return
    casino.onlinePlayer.append(userInfo[0])
    playerIn = str(languageConfig["blackJack"]["playerIn"])\
        .replace("?@user", f"{player.display_name}")
    await channel.send(playerIn)
    logger.info(f"{player.id} join a blackJack table {channel.id}")
    if table.getPlayerCount() >= table.maxPlayer:
        await blackJackGameStart(table, table.inviteMessage, self, gamePlayerWaiting, casino, db)
        logger.info(f"Table {channel.id} started automatically due to full")
