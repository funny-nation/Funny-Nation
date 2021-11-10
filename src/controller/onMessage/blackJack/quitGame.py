from src.utils.casino.table.BlackJackTable import BlackJackTable
from discord import User, Client, TextChannel
from pymysql import Connection

from loguru import logger
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.model.blackJackRecordManagement import setGameStatus
import configparser
config = configparser.ConfigParser()
config.read('config.ini')


async def quitBlackJack(table: BlackJackTable, player: User, channel: TextChannel, self: Client, db: Connection):
    databaseResult = True
    databaseResult = databaseResult and addMoneyToUser(db, player.id, table.money)
    databaseResult = databaseResult and addNewCashFlow(db, player.id, table.money, config['cashFlowMessage']['blackJackRefund'])
    databaseResult = databaseResult and setGameStatus(db, player.id, table.uuid, 4)

    if not databaseResult:
        await channel.send(f"{player.display_name}，由于数据库错误，你的钱好像卡在这里了，请私聊一下群主")
        logger.error(f"Database error while player {player.id} quiting the game")
    table.dropPlayer(player.id)
    logger.info(f"Player {player.id} quit the table")
    await channel.send(f"{player.display_name}退出了游戏")
