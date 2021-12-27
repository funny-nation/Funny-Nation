import re
from typing import List
from discord import Client, TextChannel, Member, Message, User
from pymysql import Connection

from src.controller.onMessage.holdem.checkOutMoneyAndEnd import holdemCheckOutMoneyAndEnd
from src.controller.onMessage.holdem.endGame import holdemEndGame
from src.controller.onMessage.holdem.next.nextPlayer import holdemNextPlayer
from src.controller.onMessage.holdem.next.nextRound import holdemNextRound
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from loguru import logger


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
    table.rise(user.id, money)
    await channel.send(f"玩家{user.display_name}加注")

    await holdemNextPlayer(table, channel, self, db, casino, gamePlayerWaiting)
