import configparser
import re

from loguru import logger
import configparser
from src.model.cashFlowManagement import get10RecentCashflowsByUserID

from discord import Client, Message
from pymysql import Connection
from pathlib import Path
from src.utils.readConfig import getLanguageConfig

languageConfig = getLanguageConfig()


async def checkCashFlow(self: Client, message: Message, db: Connection):
    cashFlowData: tuple = get10RecentCashflowsByUserID(db, message.author.id, None)
    messageSendBack: str = ''
    if cashFlowData is None:
        logger.error(f"User {message.author.id} check cash flow failed")
        messageSendBack: str = str(languageConfig['error']["dbError"])
    else:
        recentRecord = str(languageConfig["cashFlow"]["recentRecord"])
        messageSendBack += recentRecord+'\n'
        for cashFlow in cashFlowData:
            cashMsg = str(languageConfig["cashFlow"]["lineDisplayFormat"]).replace("?@time", f" {cashFlow[4].strftime('%Y-%m-%d %H:%M:%S')} ")\
                .replace("?@amount1", f" {cashFlow[3]} ")\
                .replace("?@amount2", f" {cashFlow[2] / 100}")
            messageSendBack += cashMsg+"\n---------------------\n"

    await message.channel.send(messageSendBack)


async def checkCashFlowWithFilter(self: Client, message: Message, db: Connection, command: str):
    filterMessage: str = re.findall(f"^账单 (.+)", command)[0]
    cashFlowData: tuple = get10RecentCashflowsByUserID(db, message.author.id, filterMessage)
    messageSendBack: str = ''
    if cashFlowData is None:
        logger.error(f"User {message.author.id} check cash flow failed")
        systemError = str(languageConfig['error']["dbError"])
        messageSendBack: str = systemError
    else:
        if len(cashFlowData) == 0:
            recordNotFound = str(languageConfig["cashFlow"]["recordNotFound"])
            messageSendBack += recordNotFound
        else:
            recordFound = str(languageConfig["cashFlow"]["recordFound"])
            messageSendBack += recordFound+'\n'
            for cashFlow in cashFlowData:
                cashMsg = str(languageConfig["cashFlow"]["lineDisplayFormat"])\
                    .replace("?@time", f" {cashFlow[4].strftime('%Y-%m-%d %H:%M:%S')} ")\
                    .replace("?@amount1", f" {cashFlow[3]} ")\
                    .replace("?@amount2", f" {cashFlow[2] / 100}")
                messageSendBack += cashMsg + "\n---------------------\n"

    await message.channel.send(messageSendBack)
