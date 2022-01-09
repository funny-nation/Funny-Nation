import re
from loguru import logger
from typing import List
import configparser
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from discord import Client, Message
from pymysql import Connection

async def addMoneyAdmin(self: Client, db: Connection, message: Message, command: str, admin: List):
    adminString = re.findall(f"^管理员加钱 ([0-9]+\.?[0-9]*) \<\@\![0-9]+\>$", command)
    moneyTransfer: int = int(float(adminString[0]) * 100)
    author = message.author.id
    if author not in admin:
        await message.channel.send("加钱失败")
        return

    if not addMoneyToUser(db, message.mentions[0].id, moneyTransfer):
        logger.error(f"Cannot add money to user {message.mentions[0].id}")
        await message.channel.send("error")
        return
    if not addNewCashFlow(db, message.mentions[0].id, moneyTransfer, '管理员加钱'):
        logger.error(f"Cannot create cash flow for user {message.mentions[0].id}")
        return

    await message.channel.send("加钱成功")



