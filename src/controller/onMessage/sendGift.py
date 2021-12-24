from discord import Client, Message, Member, TextChannel, File
from pymysql import Connection
import configparser

from typing import List, Dict
import re
from loguru import logger
import glob
from pathlib import Path
from src.model.userManagement import getUser
from src.model.userManagement import addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow

giftConfig = configparser.ConfigParser()
giftConfig.read('giftConfig.ini')

config = configparser.ConfigParser()
config.read('config.ini')

# img: Dict[str, File] = {}
#
#
# def loadPictures():
#     path = config['img']['giftImgPath']
#     filePaths = glob.glob(path + '*')
#     for filePath in filePaths:
#         img[Path(filePath).stem] = File(filePath)
#
#
# loadPictures()


async def sendGift(self: Client, db: Connection, message: Message, command: str, giftAnnouncementChannel: TextChannel):
    giftName: str = re.findall(f"^送 (.+) \<\@\![0-9]+\>$", command)[0]
    sender: Member = message.author
    if giftName not in giftConfig.sections():
        await message.channel.send("找不到这个礼物")
        return

    if len(message.mentions) == 0:
        await message.channel.send("不知道你要送给谁")
        return

    receiver: Member = message.mentions[0]
    if receiver.id == sender.id:
        await message.channel.send("不能送给自己哦")
        return

    moneyAmount = int(giftConfig[giftName]['amount'])
    userInfo: tuple = getUser(db, sender.id)
    if userInfo[1] < moneyAmount:
        await message.channel.send("你钱包瘪了，再攒攒再送叭！")
        return

    receiverInfo = getUser(db, receiver.id)
    if receiverInfo is None:
        await message.channel.send('让ta在这个discord先发一条消息吧')
        return

    if not addMoneyToUser(db, userInfo[0], -moneyAmount):
        logger.error(f"Cannot reduce money from user {userInfo[0]}")
        await message.channel.send("炸了，麻烦通知一下群主")
        return
    if not addNewCashFlow(db, userInfo[0], -moneyAmount, '送礼'):
        logger.error(f"Cannot create cash flow for user {userInfo[0]}")
    if not addMoneyToUser(db, receiver.id, moneyAmount):
        logger.error(f"Cannot add money to user {receiver.id}")
        await message.channel.send("炸了，麻烦通知一下群主")
        return
    if not addNewCashFlow(db, receiver.id, moneyAmount, '收礼'):
        logger.error(f"Cannot create cash flow for user {receiver.id}")

    giftMsgFormat = giftConfig[giftName]['msgFormat']
    giftMsg = giftMsgFormat.replace("?@sender", f" <@{sender.id}> ")
    giftMsg = giftMsg.replace("?@receiver", f" <@{receiver.id}> ")
    await message.channel.send("送礼成功，ta收到了")
    await giftAnnouncementChannel.send(giftMsg)

    path = config['img']['giftImgPath']
    filePaths = glob.glob(path + '*')
    for filePath in filePaths:
        if Path(filePath).stem == giftName:
            await giftAnnouncementChannel.send(file=File(filePath))

