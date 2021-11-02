from discord import Client, Message, Reaction, TextChannel, User
from pymysql import Connection
from src.utils.casino.Casino import Casino
from src.utils.casino.table import Table
from src.controller.onMessage.blackJack.quitGame import quitBlackJack


async def quitGame(self: Client, message: Message, db: Connection, casino: Casino):
    table: Table = casino.getTable(message.channel.id)
    playerID = message.author.id
    if table is None:
        await message.channel.send("这里没人开游戏")
        return
    if not table.hasPlayer(playerID):
        await message.channel.send("你不在这局游戏里")
        return

    if table.gameStarted:
        await message.channel.send("游戏已经开始了，你来不及退了")
        return

    if table.owner == message.author:
        await message.channel.send("你是房主，不能退出，只能关闭")
        return

    casino.onlinePlayer.remove(playerID)

    if table.game == 'blackJack':
        await quitBlackJack(table, message.author, message.channel, self, db)


async def quitGameByReaction(table: Table, user: User, channel: TextChannel, self: Client, db: Connection, casino: Casino):
    if table.gameStarted:
        await channel.send(f"{user.display_name}，游戏已经开始了，你来不及退了")
        return

    if not table.hasPlayer(user.id):
        await channel.send(f"{user.display_name}，你不在这局游戏里")
        return

    if table.owner == user:
        await channel.send(f"{user.display_name}，你是房主，不能退出，只能关闭")
        return

    casino.onlinePlayer.remove(user.id)
    if table.game == 'blackJack':
        await quitBlackJack(table, user, channel, self, db)
