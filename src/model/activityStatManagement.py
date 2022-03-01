from loguru import logger
from datetime import datetime

from pymysql import Connection
from pymysql.cursors import Cursor

def newActivityStatForUser(db: Connection, userID: int, activityPoint = 0) -> bool:
    """
    Add new user to activityStat database
    :param activityPoint:
    :param db: database object instance
    :param userID: User ID
    :return: Boolean True if no error
    """
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"INSERT INTO `activityStat` (`userID`, `activityPoint`) VALUES ({userID}, {activityPoint});")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def deleteAllActivityStat(db: Connection) -> bool:
    """
    Delete all activity stat in that table
    :param db:
    :return:
    """
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"DELETE FROM `activityStat`;")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True

def getActivityStatByUser(db: Connection, userID: int) -> tuple or None:
    """
    Get how many activity point that user has
    :param db:
    :param userID:
    :return:
    """
    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `activityStat` WHERE `userID` = {userID};")
        result: tuple = cursor.fetchone()
    except Exception as err:
        logger.error(err)
        return None
    return result

def getAllActivityStat(db: Connection) -> tuple or None:
    if db is None:
        return None
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM `activityStat` ORDER BY `activityPoint` DESC;")
        result: tuple = cursor.fetchall()
    except Exception as err:
        logger.error(err)
        return None
    return result


def addActivityPointToUser(db: Connection, userID: int, adding: int = 1) -> bool:
    """
    Add minute to onlineMinute column
    :param userID:
    :param adding: how much minute you want to add
    :param db:
    :return:
    True if no error
    """
    try:
        cursor: Cursor = db.cursor()
        sql: str = f"UPDATE `activityStat` SET `activityPoint` = `activityPoint` + {adding} WHERE `userID` = {userID};"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True