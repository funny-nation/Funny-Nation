from discord import Client, TextChannel, Member
from pymysql import Connection

from src.controller.routes.holdem.checkOutMoneyAndEnd import holdemCheckOutMoneyAndEnd
from src.controller.routes.holdem.endGame import holdemEndGame
from src.controller.routes.holdem.next.nextPlayer import holdemNextPlayer
from src.controller.routes.holdem.next.nextRound import holdemNextRound
from src.model.cashFlowManagement import addNewCashFlow
from src.model.holdemRecordManagement import addMoneyToHoldemRecord
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.model.userManagement import getUser, addMoneyToUser
from loguru import logger
import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')



async def holdemAllIn(table: HoldemTable, user: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):

    userInfo: tuple = getUser(db, user.id)
    allInMoney: int = userInfo[1] + 0
    databaseResult = True
    databaseResult = databaseResult and addMoneyToUser(db, user.id, -allInMoney)
    databaseResult = databaseResult and addNewCashFlow(db, user.id, -allInMoney, config['cashFlowMessage']['holdemSpent'])
    databaseResult = databaseResult and addMoneyToHoldemRecord(db, user.id, table.uuid, allInMoney)
    if not databaseResult:
        await channel.send(f"炸了，麻烦通知一下群主")
        logger.error("Database Error while remove money from user")
        return

    table.allIn(user.id, allInMoney)

    allInMoneyDisplay = allInMoney / 100
    await channel.send(f"玩家{user.display_name}全压上他仅存的{allInMoneyDisplay}元")
    logger.info(f"Player {user.id} all in holdem table {channel.id}")
    await holdemNextPlayer(table, channel, self, db, casino, gamePlayerWaiting)
    return
