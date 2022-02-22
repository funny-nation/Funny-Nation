from src.model.userManagement import getUser, addNewUser
from discord import Member
from pymysql import Connection
from loguru import logger

def registerIfNew(member: Member, db: Connection):
    """
    Register for user when he/she sending message
    :param member:
    :param db:
    """
    userInfo: tuple = getUser(db, member.id)
    if userInfo is None:
        if not addNewUser(db, member.id):
            logger.error(f"Cannot create new account to {member} when sending message. ")
            return
        logger.info(f"New account created for {member}")


