import re
from typing import List
from discord import Client, TextChannel, Message, User
from pymysql import Connection

from src.controller.routes.holdem.next.nextPlayer import holdemNextPlayer
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.model.holdemRecordManagement import addMoneyToHoldemRecord
from loguru import logger
from src.utils.readConfig import getCashFlowMsgConfig
cashFlowMsgConfig = getCashFlowMsgConfig()


async def holdemRise(self: Client, message: Message, db: Connection, command: str, casino, gamePlayerWaiting):
    moneyStrings: List[str] = re.findall(f"^加注 ([0-9]+)$", command)
    money: int = int(moneyStrings[0]) * 100
    channel: TextChannel = message.channel
    user: User = message.author
    table: HoldemTable = casino.getTable(channel.id)
    if table is None:
        await channel.send(f"{user.display_name}，你不在这场牌局")
        return

    if table.whosTurn != user.id:
        await channel.send(f"{user.display_name}，还没轮到你")
        return

    moneyInvest = money + table.getAmountOfMoneyToCall(user.id)
    userInfo: tuple = getUser(db, user.id)
    if userInfo[1] < moneyInvest:
        await channel.send(f"{user.display_name}，你不够钱")
        return
    databaseResult = True
    databaseResult = databaseResult and addMoneyToUser(db, user.id, -moneyInvest)
    databaseResult = databaseResult and addNewCashFlow(db, user.id, -moneyInvest, cashFlowMsgConfig['holdem']['holdemSpent'])
    databaseResult = databaseResult and addMoneyToHoldemRecord(db, user.id, table.uuid, moneyInvest)
    if not databaseResult:
        await channel.send(f"炸了，麻烦通知一下群主")
        logger.error("Database Error while remove money from user")
        return
    table.rise(user.id, money)
    await channel.send(f"玩家{user.display_name}加注")

    await holdemNextPlayer(table, channel, self, db, casino, gamePlayerWaiting)
