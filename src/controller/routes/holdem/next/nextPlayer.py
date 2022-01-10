from discord import Client, Message, Reaction, TextChannel, User, Member
from pymysql import Connection

from src.controller.routes.holdem.checkOutMoneyAndEnd import holdemCheckOutMoneyAndEnd
from src.controller.routes.holdem.endGame import holdemEndGame
from src.controller.routes.holdem.joinGame import joinHoldemGame
from src.controller.routes.holdem.next.nextRound import holdemNextRound
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.controller.routes.blackJack.joinGame import joinBlackJack
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.routes.holdem.sendPromptMsg import sendPromptMsg
from src.model.userManagement import getUser
from src.utils.poker.pokerImage import getPokerImage


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

