from discord import Client, TextChannel, Member
from pymysql import Connection

from src.controller.onMessage.holdem.checkOutMoneyAndEnd import holdemCheckOutMoneyAndEnd
from src.controller.onMessage.holdem.endGame import holdemEndGame
from src.controller.onMessage.holdem.next.nextPlayer import holdemNextPlayer
from src.controller.onMessage.holdem.next.nextRound import holdemNextRound
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from loguru import logger


async def fold(table: HoldemTable, user: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    table.fold(user.id)
    await channel.send(f"玩家{user.display_name}弃牌")
    logger.info(f"Player {user.id} fold in holdem table {channel.id}")

    if table.numberOfPlayersNotFold == 1:
        await holdemEndGame(table, channel, self, db, casino, gamePlayerWaiting)
        return

    await holdemNextPlayer(table, channel, self, db, casino, gamePlayerWaiting)

