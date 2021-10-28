import re

from typing import List
from loguru import logger

from src.model.userManagement import getUser

from discord import Client, Message
from pymysql import Connection

from util.casino.Casino import Casino


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
    logger.info(f"{message.author.id} create a blackJack Table in channel {message.channel.id}")
