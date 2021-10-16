import re

from typing import List

from src.model.userManagement import getUser

from discord import Client, Message
from pymysql import Connection

from src.data.casino.Casino import Casino


async def newBlackJackGame(self: Client, message: Message, db: Connection, command: str, casino: Casino):
    moneyStrings: List[str] = re.findall(f"^开局21点 ([0-9]+\.?[0-9]*)元$", command)
    money: int = int(float(moneyStrings[0]) * 100)
    alphaPlayerInfo: tuple = getUser(db, message.author.id)
    if alphaPlayerInfo[1] < money:
        await message.channel.send("你不够钱")
        return
    if not casino.createBlackJackTableByID(message.channel.id, money):
        await message.channel.send("这个频道有人用了，你换一个")
        return
    casino.getTable(message.channel.id).addPlayer(message.author.id)
    await message.channel.send("牌局已建立，等待一名玩家加入")
