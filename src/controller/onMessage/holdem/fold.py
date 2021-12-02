from discord import Client, Message, Reaction, TextChannel, User, Member
from pymysql import Connection

from src.controller.onMessage.holdem.joinGame import joinHoldemGame
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.controller.onMessage.blackJack.joinGame import joinBlackJack
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting


async def fold(table: HoldemTable, user: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    table.whosTurn = table.players[user.id]['next']
    table.fold(user.id)
    casino.onlinePlayer.remove(user.id)

    if table.getPlayerCount() <= 1:

        return

    await channel.send(f"玩家{user.display_name}弃牌")
