import re

from typing import List
from loguru import logger
import asyncio

from src.model.userManagement import getUser
from src.utils.gameWaiting.main import newWait
from discord import Client, Message
from pymysql import Connection
from src.controller.onMessage.pauseGame import pauseGame

from src.utils.casino.Casino import Casino


async def newBlackJackGame(self: Client, message: Message, db: Connection, command: str, casino: Casino):
    moneyStrings: List[str] = re.findall(f"^开局21点 ([0-9]+\.?[0-9]*)$", command)
    money: int = int(float(moneyStrings[0]) * 100)
    playerInfo: tuple = getUser(db, message.author.id)
    if playerInfo[1] < money:
        await message.channel.send("你不够钱")
        return
    if not casino.createBlackJackTableByID(message.channel.id, money, message):
        await message.channel.send("这个频道有人用了，你换一个")
        return
    casino.getTable(message.channel.id).addPlayer(message.author.id)
    await message.add_reaction('\N{White Heavy Check Mark}')
    await message.channel.send("牌局已建立，等待玩家加入，想加入的可以点击上面的✅图标")

    async def timeOutFunction():
        print("结束")
        casino.deleteTable(message.channel.id)

    async def timeWarning():
        client: Client = self
        print(await client.fetch_channel(message.channel.id))

        print("还有10秒超时")

    newWait(playerInfo[0], timeOutFunction, timeWarning)
    logger.info(f"{message.author.id} create a blackJack Table in channel {message.channel.id}")
