import re

from typing import List
from loguru import logger
import asyncio

from src.model.userManagement import getUser
from discord import Client, Message
from pymysql import Connection
from src.controller.onMessage.pauseGame import pauseGame
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting

from src.utils.casino.Casino import Casino


async def newBlackJackGame(self: Client, message: Message, db: Connection, command: str, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    moneyStrings: List[str] = re.findall(f"^开局21点 ([0-9]+\.?[0-9]*)$", command)
    money: int = int(float(moneyStrings[0]) * 100)
    playerInfo: tuple = getUser(db, message.author.id)
    if playerInfo[1] < money:
        await message.channel.send("你不够钱")
        return
    if not casino.createBlackJackTableByID(message.channel.id, money, message):
        await message.channel.send("这个频道有人用了，你换一个")
        return
    if playerInfo[0] in casino.onlinePlayer:
        await message.channel.send("你已经在一局游戏了")
        return
    casino.onlinePlayer.append(playerInfo[0])

    casino.getTable(message.channel.id).addPlayer(message.author.id)
    await message.add_reaction('\N{White Heavy Check Mark}')
    await message.channel.send("牌局已建立，等待玩家加入，想加入的可以点击上面的✅图标")

    async def timeOutFunction():
        await pauseGame(self, message, casino, db, gamePlayerWaiting, removeWait=False)
        await message.channel.send("由于时间过长，牌局自动关闭")

    async def timeWarning():
        await message.channel.send("还有5秒钟牌局将会自动关闭")

    await gamePlayerWaiting.newWait(playerInfo[0], timeOutFunction, timeWarning, 100)
    logger.info(f"{message.author.id} create a blackJack Table in channel {message.channel.id}")
