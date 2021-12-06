from discord import Client, Message, Reaction, TextChannel, User, Member, Guild
from pymysql import Connection

from src.utils.casino.table.holdem.HoldemTable import HoldemTable



async def holdemCheckOutMoneyAndEnd(self: Client, user: Member, channel: TextChannel, moneyToPlayers: list):
    myGuild: Guild = self.guilds[0]
    for moneyToPlayer in moneyToPlayers:
        player: Member = await myGuild.fetch_member(moneyToPlayer[0])
        displayMoney = moneyToPlayer[1] / 100
        await channel.send(f"玩家{player.display_name}获得{displayMoney}元")
    await channel.send(f"游戏结束")
