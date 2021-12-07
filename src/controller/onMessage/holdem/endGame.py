from discord import Client, Message, Reaction, TextChannel, User, Member
from pymysql import Connection

from src.controller.onMessage.holdem.checkOutMoneyAndEnd import holdemCheckOutMoneyAndEnd
from src.controller.onMessage.holdem.joinGame import joinHoldemGame
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.controller.onMessage.blackJack.joinGame import joinBlackJack
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting

async def holdemEndGame(table: HoldemTable, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    return