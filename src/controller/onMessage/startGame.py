from discord import Client, Message
from util.casino.Casino import Casino
from util.casino.table.BlackJackTable import BlackJackTable
from src.controller.onMessage.blackJack.gameStart import blackJackGameStart


async def gameStartByTableOwner(self: Client, message: Message, casino: Casino):
    table: BlackJackTable = casino.getTable(message.channel.id)
    if table is None:
        await message.channel.send("没人开游戏")
        return
    if table.getPlayerCount() == 1:
        await message.channel.send("人数不够")
        return
    if table.owner != message.author:
        await message.channel.send("你不是桌主")
        return
    if table.gameStarted:
        await message.channel.send("游戏已经开了")
        return

    if table.game == 'blackJack':
        await blackJackGameStart(table, message, self)
