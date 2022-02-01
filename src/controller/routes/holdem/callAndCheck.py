from discord import Client, TextChannel, Member
from pymysql import Connection

from src.controller.routes.holdem.next.nextPlayer import holdemNextPlayer
from src.model.cashFlowManagement import addNewCashFlow
from src.model.holdemRecordManagement import addMoneyToHoldemRecord
from src.model.userManagement import addMoneyToUser
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from loguru import logger
from src.utils.readConfig import getCashFlowMsgConfig
cashFlowMsgConfig = getCashFlowMsgConfig()


async def holdemCallAndCheck(table: HoldemTable, user: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    amountOfMoneyToSpend = table.getAmountOfMoneyToCall(user.id) + 0
    if amountOfMoneyToSpend > 0:
        databaseResult = True
        databaseResult = databaseResult and addMoneyToUser(db, user.id, -amountOfMoneyToSpend)
        databaseResult = databaseResult and addNewCashFlow(db, user.id, -amountOfMoneyToSpend, cashFlowMsgConfig['holdem']['holdemSpent'])
        databaseResult = databaseResult and addMoneyToHoldemRecord(db, user.id, table.uuid, amountOfMoneyToSpend)
        if not databaseResult:
            await channel.send(f"炸了，麻烦通知一下群主")
            logger.error("Database Error while remove money from user")
            return
    table.callOrCheck(user.id)
    if amountOfMoneyToSpend == 0:
        await channel.send(f"玩家{user.display_name}过牌")
        logger.info(f"Player {user.id} called in holdem table {channel.id}")
    else:
        await channel.send(f"玩家{user.display_name}跟牌")
        logger.info(f"Player {user.id} checked in holdem table {channel.id}")

    await holdemNextPlayer(table, channel, self, db, casino, gamePlayerWaiting)
