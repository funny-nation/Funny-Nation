from discord import Client, Message
from src.utils.casino.Casino import Casino
from src.utils.casino.table.Table import Table
from pymysql import Connection


async def pauseGame(self: Client, message: Message, casino: Casino, db: Connection):
    table: Table = casino.getTable(message.channel.id)
    if table is None:
        await message.channel.send("这里没人开游戏")
        return
    if table.owner != message.author:
        await message.channel.send("你不是桌主")
        return
    if table.gameStarted:
        await message.channel.send("游戏已经开了，掀个毛")
        return

    casino.deleteTable(message.channel.id)
    await message.channel.send("游戏关闭")
