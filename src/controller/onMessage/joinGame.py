from discord import Client, Message, Reaction, TextChannel, User, Member
from pymysql import Connection
from src.utils.casino.Casino import Casino
from src.utils.casino.table import Table
from src.controller.onMessage.blackJack.joinGame import joinBlackJack
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting


async def joinGame(self: Client, message: Message, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
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
    if table.gameStarted:
        await message.channel.send(f"{message.author.display_name}，游戏已经开始了，等下一局吧")
        return

    if table.game == 'blackJack':
        await joinBlackJack(table, message.author, message.channel, self, db, casino, gamePlayerWaiting)


async def joinGameByReaction(table: Table, user: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    if table.hasPlayer(user.id):
        await channel.send(f"{user.display_name}，你已经加入了")
        return
    if table.gameStarted:
        await channel.send(f"{user.display_name}，游戏已经开始了，等下一局吧")
        return
    if table.getPlayerCount() >= table.maxPlayer:
        await channel.send(f"{user.display_name}，满人了")
        return
    if table.game == 'blackJack':
        await joinBlackJack(table, user, channel, self, db, casino, gamePlayerWaiting)
