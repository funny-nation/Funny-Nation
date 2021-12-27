from loguru import logger
from datetime import datetime

from pymysql import Connection
from pymysql.cursors import Cursor
from src.model.makeDatabaseConnection import makeDatabaseConnection
import uuid


def newBlackJackRecord(db: Connection, userID: int, money: int, tableID: int, talbeUUID: str) -> bool:
    if db is None:
        return False
    now: datetime = datetime.utcnow()
    currentTime: str = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"INSERT INTO `blackJackGameRecord` (`userID`, `money`, `status`, `tableID`, `time`, `uuid`) VALUES ({userID}, {money}, '0', {tableID}, '{currentTime}', '{talbeUUID}');")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def dropBlackJackRecord(db: Connection, userID: int, tableUUID: str) -> bool:
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"DELETE FROM `blackJackGameRecord` WHERE `uuid` = '{tableUUID}' AND `userID` = {userID};")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def getBlackJackRecord(db: Connection, userID: int, tableUUID: str) -> tuple or None:
    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `blackJackGameRecord` WHERE `userID` = {userID} AND `uuid` = '{tableUUID}';")
        results: tuple = cursor.fetchall()
    except Exception as err:
        logger.error(err)
        return None
    return results


def getBlackJackRecordsFromATable(db: Connection, tableUUID: str) -> tuple or None:
    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `blackJackGameRecord` WHERE `uuid` = '{tableUUID}';")
        results: tuple = cursor.fetchall()
    except Exception as err:
        logger.error(err)
        return None
    return results


def setGameStatus(db: Connection, userID: int, tableUUID: str, status: int) -> bool:
    """
    Change the game status in database
    :param db:
    :param userID:
    :param tableUUID:
    :param status:
    0 represent in progress; 1 represent lose; 2 represent win; 3 represent draw; 4 represent closed;
    :return:
    """
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        sql: str = f"UPDATE `blackJackGameRecord` SET `status` = {status} WHERE `blackJackGameRecord`.`userID` = '{userID}' AND `uuid` = '{tableUUID}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True

