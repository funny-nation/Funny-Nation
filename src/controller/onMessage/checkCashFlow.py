import re

from loguru import logger

from src.model.cashFlowManagement import get10RecentCashflowsByUserID

from discord import Client, Message
from pymysql import Connection


async def checkCashFlow(self: Client, message: Message, db: Connection):
    cashFlowData: tuple = get10RecentCashflowsByUserID(db, message.author.id, None)
    messageSendBack: str = ''
    if cashFlowData is None:
        logger.error(f"User {message.author.id} check cash flow failed")
        messageSendBack: str = '系统错误'
    else:
        messageSendBack += '最近的记录：\n'
        for cashFlow in cashFlowData:
            messageSendBack += f"{cashFlow[4].strftime('%Y-%m-%d %H:%M:%S')} - {cashFlow[3]} - {cashFlow[2] / 100} 元 \n---------------------\n"

    await message.channel.send(messageSendBack)


async def checkCashFlowWithFilter(self: Client, message: Message, db: Connection, command: str):
    filterMessage: str = re.findall(f"^账单 (.+)", command)[0]
    cashFlowData: tuple = get10RecentCashflowsByUserID(db, message.author.id, filterMessage)
    messageSendBack: str = ''
    if cashFlowData is None:
        logger.error(f"User {message.author.id} check cash flow failed")
        messageSendBack = '系统错误'
    else:
        if len(cashFlowData) == 0:
            messageSendBack += '未找到关于这个的记录'
        else:

            messageSendBack += '找到的记录：\n'
            for cashFlow in cashFlowData:
                messageSendBack += f"{cashFlow[4].strftime('%Y-%m-%d %H:%M:%S')} - {cashFlow[3]} - {cashFlow[2] / 100} 元 \n---------------------\n"

    await message.channel.send(messageSendBack)