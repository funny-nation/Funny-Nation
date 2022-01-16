import re
from loguru import logger
from typing import List
import configparser
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow

from discord import Client, Message
from pymysql import Connection

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read("config.ini")


async def transferMoney(self: Client, db: Connection, message: Message, command: str):
    systemError = str(languageConfig['error']["dbError"])
    moneyStrings: List[str] = re.findall(f"^转账 ([0-9]+\.?[0-9]*) \<\@\!?[0-9]+\>$", command)
    if len(moneyStrings) == 0:
        amountNotFound = str(languageConfig['transfer']["amountNotFound"])\
            .replace('?@user', message.author.display_name)
        await message.channel.send(amountNotFound)
        return
    if len(message.mentions) == 0:
        userNotFound = str(languageConfig['transfer']["userNotFound"]) \
            .replace('?@user', message.author.display_name)
        await message.channel.send(userNotFound)
        return

    moneyTransfer: int = int(float(moneyStrings[0]) * 100)
    if moneyTransfer == 0:
        amountLess = str(languageConfig['transfer']["amountLess"]) \
            .replace('?@user', message.author.display_name)
        await message.channel.send(amountLess)
        return
    userInfo: tuple = getUser(db, message.author.id)
    if userInfo is None:
        await message.channel.send(systemError)
        logger.error(f"Get user info {message.author.id} failed")
        return

    if userInfo[1] < moneyTransfer:
        moneyNotEnough = str(languageConfig['transfer']["moneyNotEnough"]) \
            .replace('?@user', message.author.display_name)
        await message.channel.send(moneyNotEnough)
        return

    receiverInfo: tuple = getUser(db, message.mentions[0].id)
    if receiverInfo is None:
        receiverNotFound = str(languageConfig['transfer']["receiverNotFound"]) \
            .replace('?@user', message.author.display_name)
        await message.channel.send(receiverNotFound)
        return

    if not addMoneyToUser(db, userInfo[0], -moneyTransfer):
        logger.error(f"Cannot reduce money from user {userInfo[0]}")
        await message.channel.send(systemError)
        return
    if not addNewCashFlow(db, userInfo[0], -moneyTransfer, '转账'):
        logger.error(f"Cannot create cash flow for user {userInfo[0]}")
    if not addMoneyToUser(db, message.mentions[0].id, moneyTransfer):
        logger.error(f"Cannot add money to user {message.mentions[0].id}")
        await message.channel.send(systemError)
        return
    if not addNewCashFlow(db, message.mentions[0].id, moneyTransfer, '转账'):
        logger.error(f"Cannot create cash flow for user {message.mentions[0].id}")

    transferSuccess = str(languageConfig["transfer"]["transferSuccess"])\
        .replace("?@receiver", f" <@{message.mentions[0].id}>")\
        .replace("?@amount", f"{moneyTransfer / 100}")
    await message.channel.send(transferSuccess)


