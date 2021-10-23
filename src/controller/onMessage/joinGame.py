from src.model.userManagement import getUser

from discord import Client, Message, Reaction, TextChannel, User
from pymysql import Connection
from src.data.casino.Casino import Casino
from src.data.casino.table import Table
from src.controller.onMessage.blackJack.joinGame import joinBlackJack


async def joinGame(self: Client, message: Message, db: Connection, casino: Casino):
    table: Table = casino.getTable(message.channel.id)
    playerID = message.author.id
    if table is None:
        await message.channel.send("这里没人开游戏")
        return
    if table.hasPlayer(playerID):
        await message.channel.send("你已经加入了")
        return
    if table.getPlayerCount() >= table.maxPlayer:
        await message.channel.send(f"{message.author.display_name}，满人了")
        return

    if table.game == 'blackJack':
        await joinBlackJack(table, message.author, message.channel, self, db)


async def joinGameByReaction(table: Table, user: User, reaction: Reaction, self: Client, db: Connection):
    channel: TextChannel = reaction.message.channel
    if table.getPlayerCount() >= table.maxPlayer:
        await channel.send(f"{user.display_name}，满人了")
        return
    if table.game == 'blackJack':
        await joinBlackJack(table, user, channel, self, db)
