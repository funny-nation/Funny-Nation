from typing import List
from discord import Client, Message
from src.utils.poker.pokerImage import getPokerImage
from loguru import logger
from src.utils.casino.Casino import Casino
from src.utils.casino.table.BlackJackTable import BlackJackTable


async def blackJackEndGame(self: Client, table: BlackJackTable, message: Message, casino: Casino):
    if table.gameOver:
        return
    table.gameOver = True
    await message.channel.send("牌局结束，正在判断结果")
    for eachPlayerID in table.players:
        eachPlayer = await self.fetch_user(eachPlayerID)
        await message.channel.send(f"玩家{eachPlayer.display_name}的牌: ")
        cards = table.viewCards(eachPlayerID)
        await message.channel.send(file=getPokerImage(cards))
        casino.onlinePlayer.remove(eachPlayerID)
    winnerList: List[int] = table.getTheHighHand()
    if len(winnerList) == 1:
        winner = await self.fetch_user(winnerList[0])
        await message.channel.send(f"{winner.display_name}胜利")
    else:
        await message.channel.send("以下玩家牌面一样，都胜利")
        for winnerID in winnerList:
            winner = await self.fetch_user(winnerID)
            await message.channel.send(f"{winner.display_name}")
    casino.deleteTable(message.channel.id)
    logger.info(f"Game ended in table {message.channel.id}")