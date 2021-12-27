from src.utils.casino.table.BlackJackTable import BlackJackTable
from discord import User, Client, TextChannel
from pymysql import Connection

from loguru import logger
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.model.blackJackRecordManagement import setGameStatus
import configparser

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


async def quitBlackJack(table: BlackJackTable, player: User, channel: TextChannel, self: Client, db: Connection):
    databaseResult = True
    databaseResult = databaseResult and addMoneyToUser(db, player.id, table.money)
    databaseResult = databaseResult and addNewCashFlow(db, player.id, table.money, config['cashFlowMessage']['blackJackRefund'])
    databaseResult = databaseResult and setGameStatus(db, player.id, table.uuid, 4)

    if not databaseResult:
        error = str(languageConfig["blackJack"]["error1"])
        errorMsg = error.replace("?@user", f" <@{player.display_name}> ")
        await channel.send(errorMsg)
        logger.error(f"Database error while player {player.id} quiting the game")
    table.dropPlayer(player.id)
    logger.info(f"Player {player.id} quit the table")
    gameQuit = str(languageConfig["blackJack"]["gameQuit"])
    quitMsg = gameQuit.replace("?@user", f" <@{player.display_name}> ")
    await channel.send(quitMsg)
