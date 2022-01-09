import re

from typing import List
from loguru import logger

from src.model.userManagement import getUser, addMoneyToUser
from discord import Client, Message
from pymysql import Connection
from src.controller.onMessage.pauseGame import pauseGame
from src.utils.casino.table.Table import Table
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
import src.model.blackJackRecordManagement as bjRecords
import src.model.cashFlowManagement as cashFlow
from src.utils.casino.Casino import Casino
from src.model.makeDatabaseConnection import makeDatabaseConnection
import configparser
languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


async def newBlackJackGame(self: Client, message: Message, db: Connection, command: str, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    moneyStrings: List[str] = re.findall(f"^开局21点 ([0-9]+\.?[0-9]*)$", command)
    money: int = int(float(moneyStrings[0]) * 100)
    playerInfo: tuple = getUser(db, message.author.id)
    if playerInfo[1] < money:
        moneyNotEnough = str(languageConfig["blackJack"]["moneyNotEnough"])\
            .replace('?@user', playerInfo[0])
        await message.channel.send(moneyNotEnough)
        return

    if playerInfo[0] in casino.onlinePlayer:
        youWereInOtherGame = str(languageConfig["blackJack"]["youWereInOtherGame"])\
            .replace('?@user', playerInfo[0])
        await message.channel.send(youWereInOtherGame)
        return

    if not casino.createBlackJackTableByID(message.channel.id, money, message):
        channelAlreadyInUse = str(languageConfig["blackJack"]["channelAlreadyInUse"])\
            .replace('?@user', playerInfo[0])
        await message.channel.send(channelAlreadyInUse)
        return

    table: Table = casino.getTable(message.channel.id)
    databaseResult = True
    databaseResult = databaseResult and bjRecords.newBlackJackRecord(db, playerInfo[0], money, message.channel.id, table.uuid)
    databaseResult = databaseResult and addMoneyToUser(db, playerInfo[0], -money)
    databaseResult = databaseResult and cashFlow.addNewCashFlow(db, playerInfo[0], -money, config['cashFlowMessage']['blackJackSpend'])

    if not databaseResult:
        errorMsg = str(languageConfig["error"]["dbError"])
        await message.channel.send(errorMsg)
        logger.error("Database error while someone create a new black jack table")
        casino.deleteTable(message.channel.id)
        return


    casino.onlinePlayer.append(playerInfo[0])
    table.addPlayer(message.author.id)

    gameBulidMsg = str(languageConfig["blackJack"]["gameHasCreated"])\
        .replace("?@amount", f"{money / 100}")

    await message.add_reaction('\N{White Heavy Check Mark}')
    await message.channel.send(gameBulidMsg)

    async def timeOutFunction():
        dbTemp = makeDatabaseConnection()
        await pauseGame(self, message, casino, dbTemp, gamePlayerWaiting, removeWait=False)
        dbTemp.close()
        timeOut = str(languageConfig["blackJack"]["timeOutForClosingGame"])
        await message.channel.send(timeOut)

    async def timeWarning():
        warning = str(languageConfig["blackJack"]["timeOutWarningForClosingGame"])
        await message.channel.send(warning)

    await gamePlayerWaiting.newWait(playerInfo[0], timeOutFunction, timeWarning, 100)
    logger.info(f"{message.author.id} create a blackJack Table in channel {message.channel.id}")
