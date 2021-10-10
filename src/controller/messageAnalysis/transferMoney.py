import re
import sys
import os
from loguru import logger
sys.path.append(os.path.dirname(__file__) + '/../../model')
import userManagement
import cashFlowManagement


async def transferMoney(self, db, message, command):
    moneyStrings = re.findall(f"^转账 ([0-9]+\.?[0-9]*) \<\@\![0-9]+\>$", command)
    if len(moneyStrings) == 0:
        await message.channel.send("不知道你要转多少钱")
        return
    if len(message.mentions) == 0:
        await message.channel.send("不知道你要转给谁")
        return

    moneyTransfer = int(float(moneyStrings[0]) * 100)
    if moneyTransfer == 0:
        await message.channel.send("真抠门")
        return
    userInfo = userManagement.getUser(db, message.author.id)
    if userInfo is None:
        await message.channel.send("404")
        logger.error(f"Get user info {message.author.id} failed")
        return

    if userInfo[1] < moneyTransfer:
        await message.channel.send("你不够钱")
        return

    if not userManagement.addMoneyToUser(db, userInfo[0], -moneyTransfer):
        logger.error(f"Cannot reduce money from user {userInfo[0]}")
        await message.channel.send("404")
        return
    if not cashFlowManagement.addNewCashFlow(db, userInfo[0], -moneyTransfer, '转账'):
        logger.error(f"Cannot create cash flow for user {userInfo[0]}")
    if not userManagement.addMoneyToUser(db, message.mentions[0].id, moneyTransfer):
        logger.error(f"Cannot add money to user {message.mentions[0].id}")
        await message.channel.send("404")
        return
    if not cashFlowManagement.addNewCashFlow(db, message.mentions[0].id, moneyTransfer, '转账'):
        logger.error(f"Cannot create cash flow for user {message.mentions[0].id}")
    await message.channel.send(f"转账成功 <@{message.mentions[0].id}> 你收到了{moneyTransfer / 100} 元")


