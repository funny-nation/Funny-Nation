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


async def holdemAllIn(table: HoldemTable, user: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):

    table.allIn(user.id, 1000)
    await channel.send(f"玩家{user.display_name}全压")
    logger.info(f"Player {user.id} all in holdem table {channel.id}")
    return
