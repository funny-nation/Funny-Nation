from typing import Dict, List

from src.data.casino.table.BlackJackTable import BlackJackTable

from src.data.casino.Casino import Casino
from src.data.casino.table.Table import Table
from discord import Client, Message, Member, User
from loguru import logger
from src.controller.onMessage.blackJack.endGame import blackJackEndGame


async def blackJackStayWithPrivateMsg(self: Client, message: Message, casino: Casino):
    tables: Dict[int, Table] = casino.tables
    playerID = message.author.id
    tableInviteMsg = None
    for tableID in tables:
        if tables[tableID].hasPlayer(playerID):
            tableInviteMsg = tables[tableID].inviteMessage
            break
    if tableInviteMsg is None:
        await message.channel.send("你说啥呢")
        return
    member = message.author
    table: BlackJackTable = casino.getTable(tableInviteMsg.channel.id)
    table.stay(playerID)
    await tableInviteMsg.channel.send(f"玩家{member.display_name}可以开牌了")
    if table.isOver():
        await blackJackEndGame(self, table, tableInviteMsg, casino)


async def blackJackStay(self: Client, message: Message, casino: Casino, playerID: int, user: Member):
    table: BlackJackTable = casino.getTable(message.channel.id)
    if table is None:
        await message.channel.send("这里没人开游戏")
        return
    if not table.hasPlayer(playerID):
        await message.channel.send("你不在这场牌局里")
        return
    table.stay(playerID)
    await message.channel.send(f"玩家{user.display_name}可以开牌了")
    if table.isOver():
        await blackJackEndGame(self, table, message, casino)

