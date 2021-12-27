from discord import Client, TextChannel, Member
from pymysql import Connection

from src.controller.onMessage.holdem.next.nextPlayer import holdemNextPlayer
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from loguru import logger


async def holdemCallAndCheck(table: HoldemTable, user: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    amountOfMoneyToSpend = table.getAmountOfMoneyToCall(user.id) + 0
    table.callOrCheck(user.id)
    if amountOfMoneyToSpend == 0:
        await channel.send(f"玩家{user.display_name}过牌")
        logger.info(f"Player {user.id} called in holdem table {channel.id}")
    else:
        await channel.send(f"玩家{user.display_name}跟牌")
        logger.info(f"Player {user.id} checked in holdem table {channel.id}")

    await holdemNextPlayer(table, channel, self, db, casino, gamePlayerWaiting)
