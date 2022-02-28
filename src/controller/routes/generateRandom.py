from loguru import logger
import configparser
import random
from src.model.userManagement import getUser
from discord import Message, Member
from pymysql import Connection
from pathlib import Path
from src.utils.readConfig import getLanguageConfig
import embedLib.randomNumber
languageConfig = getLanguageConfig()


async def generateRandom(message: Message, db: Connection):
    """
    Reply a Non-repeating random numbers from 0-100
    :param message: Message obj
    :param db: Database obj
    :return: None
    """
    global rangesMax, rangesMin
    user: Member = message.author
    messageContent: str = message.content
    messageUseContent = messageContent.strip().split()
    if not if_integer(messageUseContent[2]) or not if_integer(messageUseContent[3]):
        logger.error(f"User has entered a non-integer range value")
        messageSendBack: str = str(languageConfig['randomNumber']['rangesNonIntegerError'])
        await message.channel.send(messageSendBack)
        return
    rangesMin = int(messageUseContent[2])
    rangesMax = int(messageUseContent[3])
    rangesSize = int(rangesMax - rangesMin + 1)
    if not if_integer(messageUseContent[4]):
        logger.error(f"User has entered a non-integer repeat time value")
        messageSendBack: str = str(languageConfig['randomNumber']['reportTimeNonIntegerError'])
        await message.channel.send(messageSendBack)
        return
    repeatTime = int(messageUseContent[4])
    userInfo: tuple = getUser(db, user.id)
    if userInfo is None:
        logger.error(f"User {user.id} check balance failed")
        messageSendBack: str = str(languageConfig['error']["dbError"])
        await message.channel.send(messageSendBack)
    if rangesMin == rangesMax:
        logger.error(f"User has entered a same min and max ranges")
        messageSendBack: str = str(languageConfig['randomNumber']['rangesAndRepeatTimeError'])
        await message.channel.send(messageSendBack)
        return
    if rangesMin > rangesMax:
        logger.error(f"Maximum range is less than minimum range")
        messageSendBack: str = str(languageConfig['randomNumber']['rangesMaxLessThanMinError'])
        await message.channel.send(messageSendBack)
        return
    if repeatTime <= 0:
        logger.error(f"User has entered a negative repeat time value")
        messageSendBack: str = str(languageConfig['randomNumber']['repeatTimeNegativeError'])
        await message.channel.send(messageSendBack)
        return
    if repeatTime >= rangesSize:
        logger.error(f"Because this random system is non-repeatable, repeat time have to bigger or equal than ranges")
        messageSendBack: str = str(languageConfig['randomNumber']['rangesAndRepeatTimeError'])
        await message.channel.send(messageSendBack)
        return
    else:
        randomNumber : str = str(random.sample(range(rangesMin, rangesMax), repeatTime))
        embedMsg = embedLib.randomNumber.getEmbed(user.display_name, randomNumber)
        await message.channel.send(embed=embedMsg)
        # displayFormat: str = str(languageConfig['randomNumber']['randomNumberFormat'])

        # messageSendBack = displayFormat \
        #     .replace("?@user", f"{user.display_name}") \
        #     .replace("?@displayRandomNumber", f"{displayRandom}")
        # displayRandom: str = str(random.sample(range(1, ranges), repeatTime))


def if_integer(string):
    if string[0] == '-' or string[0] == '+':
        return string[1:].isdigit()

    else:
        return string.isdigit()
