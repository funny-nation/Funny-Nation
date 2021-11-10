from typing import List
from discord import Client, Message, User
from src.utils.poker.pokerImage import getPokerImage
from loguru import logger
from src.utils.casino.Casino import Casino
from src.utils.casino.table.BlackJackTable import BlackJackTable
from pymysql import Connection
from src.model.cashFlowManagement import addNewCashFlow
from src.model.userManagement import addMoneyToUser
from src.model.blackJackRecordManagement import setGameStatus

import configparser
config = configparser.ConfigParser()
config.read('config.ini')


async def blackJackEndGame(self: Client, table: BlackJackTable, message: Message, casino: Casino, db: Connection):
    if table.gameOver:
        return
    table.gameOver = True
    databaseResult = True
    await message.channel.send("牌局结束，正在判断结果")
    for eachPlayerID in table.players:
        eachPlayer = await self.fetch_user(eachPlayerID)
        await message.channel.send(f"玩家{eachPlayer.display_name}的牌: ")
        cards = table.viewCards(eachPlayerID)
        await message.channel.send(file=getPokerImage(cards))
        casino.onlinePlayer.remove(eachPlayerID)
        databaseResult = databaseResult and setGameStatus(db, eachPlayerID, table.uuid, 1)

    winnerList: List[int] = table.getTheHighHand()
    totalMoney = len(table.players) * table.money
    if len(winnerList) == 1:
        winner: User = await self.fetch_user(winnerList[0])
        databaseResult = databaseResult and addMoneyToUser(db, winner.id, totalMoney)
        databaseResult = databaseResult and addNewCashFlow(db, winner.id, totalMoney, config['cashFlowMessage']['blackJackWin'])
        databaseResult = databaseResult and setGameStatus(db, winner.id, table.uuid, 2)
        await message.channel.send(f"{winner.display_name}胜利，你将获得{totalMoney / 100}元")
    else:
        prizeMoney = int(totalMoney / len(winnerList))
        await message.channel.send(f"以下玩家牌面一样，将会平分奖金，你们每人获得{prizeMoney / 100}元")
        for winnerID in winnerList:
            winner = await self.fetch_user(winnerID)
            databaseResult = databaseResult and addMoneyToUser(db, winner.id, prizeMoney)
            databaseResult = databaseResult and addNewCashFlow(db, winner.id, prizeMoney, config['cashFlowMessage']['blackJackWin'])
            databaseResult = databaseResult and setGameStatus(db, winner.id, table.uuid, 2)
            await message.channel.send(f"{winner.display_name}")
    if not databaseResult:
        await message.channel.send(f"数据库炸了，你的奖金可能卡住了，请联系一下群主")
        logger.error(f"Database error while game {table.uuid} is ending")
    casino.deleteTable(message.channel.id)
    logger.info(f"Game ended in table {message.channel.id}")