from discord import Message
from pymysql import Connection
from src.controller.preRoute.registerIfNew import registerIfNew
from src.controller.preRoute.addActivityPointToUserForMessage import addActivityPointToUserForMessage
from src.controller.preRoute.checkInEarning import checkInEarning


async def preRouter(message: Message, db: Connection):
    """
    Run when bot receive a public message.
    This would execute before getting to router
    :param message:
    :param isBooster: Does this user boost the server?
    :param db: Database connection
    :return:
    """
    registerIfNew(message.author, db)
    addActivityPointToUserForMessage(db, message.author)
    await checkInEarning(message, db)
