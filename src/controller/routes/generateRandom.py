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
    user: Member = message.author
    messageContent: str = message.content
    messageUseContent = messageContent.strip().split()
    ranges = int(messageUseContent[2])
    repeatTime = int(messageUseContent[3])
    userInfo: tuple = getUser(db, user.id)
    if userInfo is None:
        logger.error(f"User {user.id} check balance failed")
        messageSendBack: str = str(languageConfig['error']["dbError"])
        await message.channel.send(messageSendBack)
    elif ranges <= 0 or ranges > 100:
        logger.error(f"User has entered an illegal range value")
        messageSendBack: str = str(languageConfig['randomNumber']['rangesError'])
        await message.channel.send(messageSendBack)
    elif repeatTime <= 0:
        logger.error(f"User has entered an illegal repeat time value")
        messageSendBack: str = str(languageConfig['randomNumber']['repeatTimeError'])
        await message.channel.send(messageSendBack)
    elif repeatTime >= ranges:
        logger.error(f"Because this random system is non-repeatable, repeat time have to bigger or equal than ranges")
        messageSendBack: str = str(languageConfig['randomNumber']['rangesAndRepeatTimeError'])
        await message.channel.send(messageSendBack)
    else:
        randomNumber : str = str(random.sample(range(1, ranges), repeatTime))
        embedMsg = embedLib.randomNumber.getEmbed(user.display_name, randomNumber)
        await message.channel.send(embed=embedMsg)
        # displayFormat: str = str(languageConfig['randomNumber']['randomNumberFormat'])

        # messageSendBack = displayFormat \
        #     .replace("?@user", f"{user.display_name}") \
        #     .replace("?@displayRandomNumber", f"{displayRandom}")
        # displayRandom: str = str(random.sample(range(1, ranges), repeatTime))
