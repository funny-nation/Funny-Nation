from pymysql import Connection
from discord import Member
from src.model.activityStatManagement import addActivityPointToUser, getActivityStatByUser, newActivityStatForUser
from loguru import logger
from src.utils.readConfig import getGeneralConfig

def addActivityPointToUserForMessage(db: Connection, member: Member):
    """
    Adding activity point to user.
    If user does not shown on the activity stat, this script would create a new one.
    :param db:
    :param member:
    :return:
    """
    generalConfig = getGeneralConfig()
    if getActivityStatByUser(db, member.id) is None:
        if not newActivityStatForUser(db, member.id, int(generalConfig['moneyEarning']['activityPointPerMessage'])):
            logger.info(f"Cannot add activityStat to user {member}")
        return
    if not addActivityPointToUser(db, member.id, int(generalConfig['moneyEarning']['activityPointPerMessage'])):
        logger.info(f"Cannot add activity point to user {member}")
