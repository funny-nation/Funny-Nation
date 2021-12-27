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
giftConfig.read('giftConfig.ini', encoding='utf-8')

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

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
        notFoundGift=str(languageConfig["gift"]["notFoundGift"])
        await message.channel.send(notFoundGift)
        return

    if len(message.mentions) == 0:
        notFoundUser = str(languageConfig["gift"]["notFoundUser"])
        await message.channel.send(notFoundUser)
        return

    receiver: Member = message.mentions[0]
    if receiver.id == sender.id:
        notSelf = str(languageConfig["gift"]["notSelf"])
        await message.channel.send(notSelf)
        return

    moneyAmount = int(giftConfig[giftName]['amount'])
    userInfo: tuple = getUser(db, sender.id)
    if userInfo[1] < moneyAmount:
        moneyNotEnough = str(languageConfig["gift"]["moneyNotEnough"])
        await message.channel.send(moneyNotEnough)
        return

    receiverInfo = getUser(db, receiver.id)
    if receiverInfo is None:
        notFoundReceiver = str(languageConfig["gift"]["notFoundReceiver"])
        await message.channel.send(notFoundReceiver)
        return

    if not addMoneyToUser(db, userInfo[0], -moneyAmount):
        logger.error(f"Cannot reduce money from user {userInfo[0]}")
        systemError = str(languageConfig['error']["dbError"])
        await message.channel.send(systemError)
        return
    if not addNewCashFlow(db, userInfo[0], -moneyAmount, '送礼'):
        logger.error(f"Cannot create cash flow for user {userInfo[0]}")
    if not addMoneyToUser(db, receiver.id, moneyAmount):
        logger.error(f"Cannot add money to user {receiver.id}")
        systemError = str(languageConfig['error']["dbError"])
        await message.channel.send(systemError)
        return
    if not addNewCashFlow(db, receiver.id, moneyAmount, '收礼'):
        logger.error(f"Cannot create cash flow for user {receiver.id}")

    giftMsgFormat = giftConfig[giftName]['msgFormat']
    giftMsg = giftMsgFormat.replace("?@sender", f" <@{sender.id}> ")
    giftMsg = giftMsg.replace("?@receiver", f" <@{receiver.id}> ")
    sendS = str(languageConfig["gift"]["sendS"])
    await message.channel.send(sendS)
    await giftAnnouncementChannel.send(giftMsg)

    path = config['img']['giftImgPath']
    filePaths = glob.glob(path + '*')
    for filePath in filePaths:
        if Path(filePath).stem == giftName:
            await giftAnnouncementChannel.send(file=File(filePath))

