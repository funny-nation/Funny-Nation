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
from src.utils.readConfig import getGiftConfig, getLanguageConfig, getGeneralConfig

giftConfig = getGiftConfig()
languageConfig = getLanguageConfig()

generalConfig = getGeneralConfig()

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
    giftName: str = re.findall(f"^送 (.+) \<\@\!?[0-9]+\>$", command)[0]
    sender: Member = message.author
    if giftName not in giftConfig.sections():
        giftNotFound = str(languageConfig["gift"]["giftNotFound"])\
            .replace('?@user', message.author.display_name)
        await message.channel.send(giftNotFound)
        return

    if len(message.mentions) == 0:
        userNotFound = str(languageConfig["gift"]["userNotFound"])\
            .replace('?@user', message.author.display_name)
        await message.channel.send(userNotFound)
        return

    receiver: Member = message.mentions[0]
    if receiver.id == sender.id:
        notSelf = str(languageConfig["gift"]["notSelf"]) \
            .replace('?@user', message.author.display_name)
        await message.channel.send(notSelf)
        return

    moneyAmount = int(giftConfig[giftName]['amount'])
    userInfo: tuple = getUser(db, sender.id)
    if userInfo[1] < moneyAmount:
        notEnoughMoney = str(languageConfig["gift"]["notEnoughMoney"]) \
            .replace('?@user', message.author.display_name)
        await message.channel.send(notEnoughMoney)
        return

    receiverInfo = getUser(db, receiver.id)
    if receiverInfo is None:
        receiverNotFound = str(languageConfig["gift"]["receiverNotFound"]) \
            .replace('?@user', message.author.display_name)
        await message.channel.send(receiverNotFound)
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

    giftMsg = giftConfig[giftName]['msgFormat']\
        .replace("?@sender", f" <@{sender.id}> ")\
        .replace("?@receiver", f" <@{receiver.id}> ")
    sendSuccess = str(languageConfig["gift"]["sendSuccess"])\
        .replace('?@user', message.author.display_name)
    await message.channel.send(sendSuccess)
    await giftAnnouncementChannel.send(giftMsg)

    path = generalConfig['img']['giftImgPath']
    filePaths = glob.glob(path + '*')
    for filePath in filePaths:
        if Path(filePath).stem == giftName:
            await giftAnnouncementChannel.send(file=File(filePath))

