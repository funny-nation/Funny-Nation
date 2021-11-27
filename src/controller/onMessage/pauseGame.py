from discord import Client, Message
from src.utils.casino.Casino import Casino
from src.utils.casino.table.Table import Table
from src.utils.casino.table.BlackJackTable import BlackJackTable
from pymysql import Connection
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.model.userManagement import addMoneyToUser
import src.model.blackJackRecordManagement as bjRecords
from src.model.cashFlowManagement import addNewCashFlow
from loguru import logger
import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


async def pauseGame(self: Client, message: Message, casino: Casino, db: Connection, gamePlayerWaiting: GamePlayerWaiting, removeWait=True):
    table: Table = casino.getTable(message.channel.id)
    if table is None:
        await message.channel.send("这里没人开游戏")
        return
    if table.owner != message.author:
        await message.channel.send("你不是桌主")
        return
    if table.gameStarted:
        await message.channel.send("游戏已经开了，掀个毛")
        return
    databaseResult = True
    for playerID in table.players:
        if table.game == 'blackJack':
            table: BlackJackTable
            databaseResult = databaseResult and addMoneyToUser(db, playerID, table.money)
            databaseResult = databaseResult and addNewCashFlow(db, playerID, table.money, config['cashFlowMessage']['blackJackRefund'])
            databaseResult = databaseResult and bjRecords.setGameStatus(db, playerID, table.uuid, 4)
        casino.onlinePlayer.remove(playerID)

    if not databaseResult:
        logger.error("Database Error occur while closing a black jack game")
        await message.channel.send("数据库炸了，麻烦告诉一下群主")

    if removeWait:
        await gamePlayerWaiting.removeWait(message.author.id)
    casino.deleteTable(message.channel.id)
    await message.channel.send("游戏关闭")
