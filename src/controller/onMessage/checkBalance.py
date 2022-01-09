from configparser import ConfigParser

from loguru import logger
import configparser
from src.model.userManagement import getUser
from discord import Message, Member
from pymysql import Connection
from pathlib import Path

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read("config.ini")

async def checkBalance(message: Message, db: Connection):
    """
    Reply user's balance result
    :param message: Message obj
    :param db: Database obj
    :return: None
    """
    user: Member = message.author
    userInfo: tuple = getUser(db, user.id)
    if userInfo is None:
        logger.error(f"User {user.id} check balance failed")
        messageSendBack: str = str(languageConfig['error']["dbError"])
    else:
        displayFormat: str = str(languageConfig['balance']['displayFormat'])
        displayMoney: float = userInfo[1] / 100
        messageSendBack = displayFormat\
            .replace("?@user", f"{user.display_name}")\
            .replace("?@displayMoney", f"{displayMoney}")
    await message.channel.send(messageSendBack)
