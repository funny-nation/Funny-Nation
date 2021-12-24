from discord import Client, Message
from src.utils.casino.Casino import Casino
from src.utils.casino.table.Table import Table
from src.utils.casino.table.BlackJackTable import BlackJackTable
from pymysql import Connection

from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.model.userManagement import addMoneyToUser
import src.model.blackJackRecordManagement as bjRecords
from src.model.cashFlowManagement import addNewCashFlow
from loguru import logger
import configparser

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


async def pauseGame(self: Client, message: Message, casino: Casino, db: Connection, gamePlayerWaiting: GamePlayerWaiting, removeWait=True):
    table: Table = casino.getTable(message.channel.id)
    if table is None:
        nobodyInGame = str(languageConfig['game']["nobodyInGame"])
        await message.channel.send(nobodyInGame)
        return
    if table.owner != message.author:
        notOwner = str(languageConfig['game']["notOwner"])
        await message.channel.send(notOwner)
        return
    if table.gameStarted:
        gameStart = str(languageConfig['game']["gameStart"])
        await message.channel.send(gameStart)
        return
    databaseResult = True
    for playerID in table.players:
        if table.game == 'blackJack':
            table: BlackJackTable
            databaseResult = databaseResult and addMoneyToUser(db, playerID, table.money)
            databaseResult = databaseResult and addNewCashFlow(db, playerID, table.money, config['cashFlowMessage']['blackJackRefund'])
            databaseResult = databaseResult and bjRecords.setGameStatus(db, playerID, table.uuid, 4)
        if table.game == 'holdem':
            table: HoldemTable
            databaseResult = databaseResult and addMoneyToUser(db, playerID, table.ante)
            databaseResult = databaseResult and addNewCashFlow(db, playerID, table.ante, config['cashFlowMessage']['holdemAnteRefund'])
        casino.onlinePlayer.remove(playerID)

    if not databaseResult:
        logger.error("Database Error occur while closing a black jack game")
        systemError = str(languageConfig['error']["dbError"])
        await message.channel.send(systemError)

    if removeWait:
        await gamePlayerWaiting.removeWait(message.author.id)
    casino.deleteTable(message.channel.id)
    systemError = str(languageConfig['error']["dbError"])
    await message.channel.send(systemError)
