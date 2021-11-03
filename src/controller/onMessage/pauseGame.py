from discord import Client, Message
from src.utils.casino.Casino import Casino
from src.utils.casino.table.Table import Table
from pymysql import Connection
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting


async def pauseGame(self: Client, message: Message, casino: Casino, db: Connection, gamePlayerWaiting: GamePlayerWaiting):
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

    for playerID in table.players:
        casino.onlinePlayer.remove(playerID)
    await gamePlayerWaiting.removeWait(message.author.id)
    casino.deleteTable(message.channel.id)
    await message.channel.send("游戏关闭")
