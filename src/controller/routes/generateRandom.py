from loguru import logger
import configparser
import random
from src.model.userManagement import getUser
from discord import Message, Member
from pymysql import Connection
from pathlib import Path
from src.utils.readConfig import getLanguageConfig

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
    elif ranges <= 0 or ranges > 100:
        logger.error(f"User has entered an illegal range value")
        messageSendBack: str = str(languageConfig['randomNumber']['rangesError'])
    elif repeatTime <= 0:
        logger.error(f"User has entered an illegal repeat time value")
        messageSendBack: str = str(languageConfig['randomNumber']['repeatTimeError'])
    elif repeatTime > ranges:
        logger.error(f"Because this random system is non-repeatable, repeat time have to bigger than ranges")
        messageSendBack: str = str(languageConfig['randomNumber']['rangesAndRepeatTimeError'])
    else:
        displayFormat: str = str(languageConfig['randomNumber']['randomNumberFormat'])
        displayRandom: str = str(random.sample(range(1, ranges), repeatTime))
        messageSendBack = displayFormat \
            .replace("?@user", f"{user.display_name}") \
            .replace("?@displayRandomNumber", f"{displayRandom}")
    await message.channel.send(messageSendBack)
