from discord import Client, TextChannel
from pymysql import Connection

from src.controller.routes.holdem.next.nextRound import holdemNextRound
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.runWhenBotStart.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.routes.holdem.sendPromptMsg import sendPromptMsg
from src.model.userManagement import getUser


async def holdemNextPlayer(table: HoldemTable, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):


    if table.toNext():
        isEnd = await holdemNextRound(table, channel, self, db, casino, gamePlayerWaiting)
        if isEnd:
            return
    nextPlayerID = table.whosTurn
    if nextPlayerID is None:
        await whenEveryoneAllIn(table, channel, self, db, casino, gamePlayerWaiting)
        return
    userInfo: tuple = getUser(db, nextPlayerID)
    amountOfMoneyToCall: int = table.getAmountOfMoneyToCall(nextPlayerID)
    allInOnly = userInfo[1] <= amountOfMoneyToCall
    await sendPromptMsg(channel, nextPlayerID, table.mainPot, table.getAmountOfMoneyToCall(nextPlayerID), allInOnly)


async def whenEveryoneAllIn(table: HoldemTable, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):

    isEnd = await holdemNextRound(table, channel, self, db, casino, gamePlayerWaiting)
    while not isEnd:
        isEnd = await holdemNextRound(table, channel, self, db, casino, gamePlayerWaiting)

    return

