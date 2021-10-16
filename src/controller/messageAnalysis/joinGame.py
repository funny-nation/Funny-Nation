from src.model.userManagement import getUser

from discord import Client, Message
from pymysql import Connection
from src.data.casino.Casino import Casino
from src.data.casino.table import Table
from src.controller.messageAnalysis.blackJack.joinGame import joinBlackJack


async def joinGame(self: Client, message: Message, db: Connection, casino: Casino):
    table: Table = casino.getTable(message.channel.id)
    playerID = message.author.id
    if table is None:
        await message.channel.send("这里没人开游戏")
        return
    if table.hasPlayer(playerID):
        await message.channel.send("你已经加入了")
        return
    userInfo: tuple = getUser(db, playerID)
    if userInfo[1] < table.money:
        await message.channel.send("你好像不太够钱")
        return

    if table.game == 'blackJack':
        await joinBlackJack(table, playerID, message, self)

