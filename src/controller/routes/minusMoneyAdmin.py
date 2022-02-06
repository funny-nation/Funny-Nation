import re
from loguru import logger
from typing import List
from discord import Client, TextChannel, Guild, Member, Message, Role
from src.utils.readConfig import getLanguageConfig
from src.model.userManagement import getUser, minusMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from discord import Client, Message
from pymysql import Connection

async def minusMoneyAdmin(self: Client, db: Connection, message: Message, command: str, Admin: dict):
    languageConfig = getLanguageConfig()
    adminString = re.findall(f"^抢劫 ([0-9]+\.?[0-9]*) \<\@\!?[0-9]+\>$", command)
    moneyTransfer: int = int(float(adminString[0]) * 100)
    msgSender: Member = message.author
    rolesBelongsToMember: List[Role] = msgSender.roles

    if Admin['admin'] not in rolesBelongsToMember:
        msg = languageConfig['eventAward']['notAdmian'] \
            .replace('?@user_name', msgSender.display_name)
        await message.channel.send(msg)
        return

    if not minusMoneyToUser(db, message.mentions[0].id, moneyTransfer):
        logger.error(f"Cannot add money to user {message.mentions[0].id}")
        await message.channel.send("error")
        return

    if not addNewCashFlow(db, message.mentions[0].id, moneyTransfer, '管理员扣钱'):
        logger.error(f"Cannot create cash flow for user {message.mentions[0].id}")
        return

    await message.channel.send("抢劫成功")