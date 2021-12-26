from discord import Client, Message, Reaction, TextChannel, User, Member
from pymysql import Connection

from src.controller.onMessage.holdem.checkOutMoneyAndEnd import holdemCheckOutMoneyAndEnd
from src.controller.onMessage.holdem.joinGame import joinHoldemGame
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.controller.onMessage.blackJack.joinGame import joinBlackJack
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.utils.poker.pokerImage import getPokerImage


async def holdemEndGame(table: HoldemTable, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    await channel.send("Game end")
    for eachPlayerID in table.players:
        if not table.players[eachPlayerID]['fold']:
            eachPlayer = await self.fetch_user(eachPlayerID)
            await channel.send(f"玩家{eachPlayer.display_name}的牌: ")
            cards = table.viewCards(eachPlayerID)
            await channel.send(file=getPokerImage(cards))

    return
