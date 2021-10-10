import sys
import os
from loguru import logger
sys.path.append(os.path.dirname(__file__) + '/../../model')
import userManagement


async def checkBalance(message, db):
    """
    Reply user's balance result
    :param message: Message obj
    :param db: Database obj
    :return: None
    """
    user = message.author
    userInfo = userManagement.getUser(db, user.id)
    messageSendBack = ''
    if userInfo is None:
        logger.error(f"User {user.id} check balance failed")
        messageSendBack = '系统错误'
    else:
        displayMoney = userInfo[1] / 100
        messageSendBack = f"{user.display_name}，你还有{displayMoney}元"
    await message.channel.send(messageSendBack)
