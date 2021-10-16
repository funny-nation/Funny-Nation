from typing import List

from src.data.casino.table.BlackJackTable import BlackJackTable

from discord import Client, Message, Member, DMChannel

from src.data.casino import Casino
from src.data.poker.Card import Card
from src.data.poker.pokerImage import getPokerImage


async def blackJackHit(self: Client, message: Message, casino: Casino):
    table: BlackJackTable = casino.getTable(message.channel.id)
    playerID: int = message.author.id
    user: Member = message.author
    if table is None:
        await message.channel.send("这里没人开游戏")
        return
    if not table.hasPlayer(playerID):
        await message.channel.send("你不在这场牌局里")
        return

    if table.shouldStopHitting(playerID):
        await message.channel.send("你不能再要了")
        return
    table.hit(playerID)
    cards = table.viewCards(playerID)
    dmChannel: DMChannel = await user.create_dm()
    await dmChannel.send(file=getPokerImage(cards))
    await dmChannel.send("你还要吗")


async def blackJackHitWithPrivateMessage(self: Client, message: Message, casino: Casino):
    player: Member = message.author
    table: BlackJackTable = casino.getTableByPlayerID(player.id)
    if table is None:
        await message.channel.send("你好像不在牌局里")
        return
    if table.shouldStopHitting(player.id):
        await message.channel.send("你不能再要了")
        return
    table.hit(player.id)
    cards: List[Card] = table.viewCards(player.id)
    await message.channel.send(file=getPokerImage(cards))
    await message.channel.send("你还要吗")
