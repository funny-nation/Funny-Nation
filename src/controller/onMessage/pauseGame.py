from discord import User, DMChannel, File, Client, Message
from src.data.casino.Casino import Casino
from src.data.casino.table.Table import Table
from src.controller.onMessage.blackJack.gameStart import blackJackGameStart


async def pauseGame(self: Client, message: Message, casino: Casino):
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
