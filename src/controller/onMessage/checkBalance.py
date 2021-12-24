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
config.read("Cconfig.ini")

async def checkBalance(message: Message, db: Connection):
    """
    Reply user's balance result
    :param message: Message obj
    :param db: Database obj
    :return: None
    """
    user: Member = message.author
    userInfo: tuple = getUser(db, user.id)
    messageSendBack: str = ''
    if userInfo is None:
        logger.error(f"User {user.id} check balance failed")
        systemError=str(languageConfig['error']["dbError"])
        messageSendBack: str = systemError
    else:
        displayFormat = str(languageConfig['balance']['displayFormat'])
        moneyMsg = displayFormat.replace("?@user", f" @{user.display_name} ")
        displayMoney: float = userInfo[1] / 100
        moneyMsg = moneyMsg.replace("？@displayMoney", f" {displayMoney} ")
        messageSendBack: str = moneyMsg
    await message.channel.send(messageSendBack)
