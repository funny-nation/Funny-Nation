from typing import List

from src.utils.casino.table.BlackJackTable import BlackJackTable

from discord import Client, Message, Member, DMChannel
from loguru import logger

from src.utils.casino import Casino
from src.utils.poker.Card import Card
from src.utils.poker.pokerImage import getPokerImage
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.onMessage.blackJack.stay import blackJackStay, blackJackStayWithPrivateMsg


async def blackJackHit(self: Client, message: Message, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
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
    logger.info(f"Player {playerID} hit on black jack")
    await dmChannel.send("你还要吗")

    async def timeoutFun():
        await message.channel.send(f"玩家{user.display_name}由于太久没没反应，自动开牌")
        await blackJackStay(self, message, casino, playerID, user, gamePlayerWaiting, removeWait=True)

    async def warningFun():
        await message.channel.send(f"玩家{user.display_name}由于太久没没反应，将会在5秒内自动开牌")

    await gamePlayerWaiting.newWait(playerID, timeoutFun, warningFun)


async def blackJackHitWithPrivateMessage(self: Client, message: Message, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
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
    logger.info(f"Player {player.id} hit on black jack")

    async def timeoutFun():
        await message.channel.send("由于你太久没没反应，系统自动开牌了")
        await blackJackStayWithPrivateMsg(self, message, casino, gamePlayerWaiting, removeWait=False)

    async def warningFun():
        await message.channel.send("由于你太久没没反应，系统将会在5秒后自动开牌")

    await gamePlayerWaiting.newWait(player.id, timeoutFun, warningFun)
