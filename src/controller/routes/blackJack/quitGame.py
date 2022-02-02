from src.utils.casino.table.BlackJackTable import BlackJackTable
from discord import User, Client, TextChannel
from pymysql import Connection

from loguru import logger
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.model.blackJackRecordManagement import setGameStatus
from src.utils.readConfig import getLanguageConfig, getCashFlowMsgConfig

languageConfig = getLanguageConfig()
cashFlowMsgConfig = getCashFlowMsgConfig()



async def quitBlackJack(table: BlackJackTable, player: User, channel: TextChannel, self: Client, db: Connection):
    databaseResult = True
    databaseResult = databaseResult and addMoneyToUser(db, player.id, table.money)
    databaseResult = databaseResult and addNewCashFlow(db, player.id, table.money, cashFlowMsgConfig['blackJack']['blackJackRefund'])
    databaseResult = databaseResult and setGameStatus(db, player.id, table.uuid, 4)

    if not databaseResult:
        errorMsg = str(languageConfig["error"]["dbError"])
        await channel.send(errorMsg)
        logger.error(f"Database error while player {player.id} quiting the game")
    table.dropPlayer(player.id)
    logger.info(f"Player {player.id} quit the table")
    gameQuit = str(languageConfig["blackJack"]["gameQuit"])\
        .replace("?@user", f"{player.display_name}")
    await channel.send(gameQuit)
