from discord import Client, TextChannel
from pymysql import Connection

from src.controller.routes.holdem.endGame import holdemEndGame
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.runWhenBotStart.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting

from src.utils.poker.pokerImage import getPokerImage


async def holdemNextRound(table: HoldemTable, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting) -> bool:
    """

    :param table:
    :param channel:
    :param self:
    :param db:
    :param casino:
    :param gamePlayerWaiting:
    :return:
    return True if Ended
    """
    async def afterFlopTurnRiver():
        await channel.send("公开牌：")
        await channel.send(file=getPokerImage(table.board))
        moneyDisplayForPot = table.mainPot / 100
        await channel.send(f"目前底池有{moneyDisplayForPot}元")

    if len(table.board) == 0:
        table.flop()
        await afterFlopTurnRiver()
    elif (len(table.board) == 3) or (len(table.board) == 4):
        table.turnOrRiver()
        await afterFlopTurnRiver()
    elif len(table.board) == 5:
        await holdemEndGame(table, channel, self, db, casino, gamePlayerWaiting)
        return True

    return False

