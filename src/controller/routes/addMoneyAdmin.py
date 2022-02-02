import re
from loguru import logger
from typing import List
from discord import Client, TextChannel, Guild, Member, Message, Role
from src.utils.readConfig import getLanguageConfig
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from discord import Client, Message
from pymysql import Connection

async def addMoneyAdmin(self: Client, db: Connection, message: Message, command: str, eventAdmin: dict,):
    languageConfig = getLanguageConfig()
    adminString = re.findall(f"^印钞 ([0-9]+\.?[0-9]*) \<\@\!?[0-9]+\>$", command)
    moneyTransfer: int = int(float(adminString[0]) * 100)
    msgSender: Member = message.author
    rolesBelongsToMember: List[Role] = msgSender.roles

    if eventAdmin['admin'] not in rolesBelongsToMember:
        msg = languageConfig['eventAward']['notEventAdmin'] \
            .replace('?@user_name', msgSender.display_name)
        await message.channel.send(msg)
        return

    if not addMoneyToUser(db, message.mentions[0].id, moneyTransfer):
        logger.error(f"Cannot add money to user {message.mentions[0].id}")
        await message.channel.send("error")
        return
    if not addNewCashFlow(db, message.mentions[0].id, moneyTransfer, '管理员加钱'):
        logger.error(f"Cannot create cash flow for user {message.mentions[0].id}")
        return

    await message.channel.send("印钞成功")



