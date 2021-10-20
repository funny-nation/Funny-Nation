from typing import Dict

from src.data.casino.table.BlackJackTable import BlackJackTable

from src.data.casino.Casino import Casino
from src.data.casino.table.Table import Table
from src.data.poker.pokerImage import getPokerImage
from discord import Client, Message, Member, User


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
    await blackJackStay(self, tableInviteMsg, casino, member.id, member)


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

        await message.channel.send("牌局结束，正在判断结果")
        winnerID: int = table.endAndGetWinner()
        for eachPlayerID in table.players:
            eachPlayer = await self.fetch_user(eachPlayerID)
            await message.channel.send(f"玩家{eachPlayer.display_name}的牌: ")
            cards = table.viewCards(eachPlayerID)
            await message.channel.send(file=getPokerImage(cards))
        if winnerID is not None:
            winner: User or None = await self.fetch_user(winnerID)
            await message.channel.send(f"{winner.display_name}胜利")
        else:
            await message.channel.send(f"平局")

        casino.deleteTable(message.channel.id)
