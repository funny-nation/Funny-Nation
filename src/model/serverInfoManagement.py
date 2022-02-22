from loguru import logger
from datetime import datetime

from pymysql import Connection
from pymysql.cursors import Cursor

def getOnlineMinute(db: Connection) -> int or None:
    """
    Get server online time in minute
    :param db:
    :return:
    """
    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"SELECT `onlineMinute` FROM `serverInfo`;")
        result: tuple = cursor.fetchone()
    except Exception as err:
        logger.error(err)
        return None
    return result[0]

def addMinuteOnlineMinute(db: Connection, adding: int = 1) -> bool:
    """
    Add minute to onlineMinute column
    :param adding: how much minute you want to add
    :param db:
    :return:
    True if no error
    """
    try:
        cursor: Cursor = db.cursor()
        sql: str = f"UPDATE `serverInfo` SET `onlineMinute` = `onlineMinute` + {adding};"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True