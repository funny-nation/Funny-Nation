import configparser
import re

from loguru import logger
import configparser
from src.model.cashFlowManagement import get10RecentCashflowsByUserID

from discord import Client, Message
from pymysql import Connection
from pathlib import Path

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read("Cconfig.ini")


async def checkCashFlow(self: Client, message: Message, db: Connection):
    cashFlowData: tuple = get10RecentCashflowsByUserID(db, message.author.id, None)
    messageSendBack: str = ''
    if cashFlowData is None:
        logger.error(f"User {message.author.id} check cash flow failed")
        systemError = str(languageConfig['error']["dbError"])
        messageSendBack: str = systemError
    else:
        recentRecord=str(languageConfig["cashFlow"]["recentRecord"])
        messageSendBack += recentRecord+'\n'
        for cashFlow in cashFlowData:
            cashD=str(languageConfig["cashFlow"]["cashD"])
            cashMsg=cashD.replace("?@time", f" {cashFlow[4].strftime('%Y-%m-%d %H:%M:%S')} ")
            cashMsg=cashMsg.replace("?@amount1", f" {cashFlow[3]} ")
            cashMsg=cashMsg.replace("?@amount2", f" {cashFlow[2] / 100}")
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
                cashD = str(languageConfig["cashFlow"]["cashD"])
                cashMsg = cashD.replace("?@time", f" {cashFlow[4].strftime('%Y-%m-%d %H:%M:%S')} ")
                cashMsg = cashMsg.replace("?@amount1", f" {cashFlow[3]} ")
                cashMsg = cashMsg.replace("?@amount2", f" {cashFlow[2] / 100}")
                messageSendBack += cashMsg + "\n---------------------\n"

    await message.channel.send(messageSendBack)