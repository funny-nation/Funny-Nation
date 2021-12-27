from discord import Client, Message, Reaction, TextChannel, User, Member
from pymysql import Connection

from src.controller.onMessage.holdem.checkOutMoneyAndEnd import holdemCheckOutMoneyAndEnd
from src.controller.onMessage.holdem.endGame import holdemEndGame
from src.controller.onMessage.holdem.joinGame import joinHoldemGame
from src.controller.onMessage.holdem.next.nextRound import holdemNextRound
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.controller.onMessage.blackJack.joinGame import joinBlackJack
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.onMessage.holdem.sendPromptMsg import sendPromptMsg

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
    await sendPromptMsg(channel, nextPlayerID, table.mainPot, table.getAmountOfMoneyToCall(nextPlayerID))


async def whenEveryoneAllIn(table: HoldemTable, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):

    isEnd = await holdemNextRound(table, channel, self, db, casino, gamePlayerWaiting)
    while not isEnd:
        isEnd = await holdemNextRound(table, channel, self, db, casino, gamePlayerWaiting)

    return

