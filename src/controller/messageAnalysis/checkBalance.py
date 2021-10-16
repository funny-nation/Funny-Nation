from loguru import logger
from src.model.userManagement import getUser
from discord import Message, Member
from pymysql import Connection


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
        messageSendBack: str = '系统错误'
    else:
        displayMoney: float = userInfo[1] / 100
        messageSendBack: str = f"{user.display_name}，你还有{displayMoney}元"
    await message.channel.send(messageSendBack)
