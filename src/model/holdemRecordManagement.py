from loguru import logger
from datetime import datetime

from pymysql import Connection
from pymysql.cursors import Cursor


def newHoldemRecord(db: Connection, userID: int, money: int, tableID: int, tableUUID: str) -> bool:
    if db is None:
        return False
    now: datetime = datetime.utcnow()
    currentTime: str = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"INSERT INTO `holdemGameRecord` (`userID`, `moneyInvested`, `status`, `tableID`, `time`, `tableUUID`) VALUES ({userID}, {money}, 0, {tableID}, '{currentTime}', '{tableUUID}');")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def removeHoldemRecord(db: Connection, userID: int, tableUUID: str) -> bool:
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"DELETE FROM `holdemGameRecord` WHERE `userID` = {userID} AND `tableUUID` = '{tableUUID}';")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def getHoldemRecord(db: Connection, userID: int, tableUUID: str) -> tuple or None:

    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `holdemGameRecord` WHERE `userID` = '{userID}' AND `tableUUID` = '{tableUUID}';")
        result: tuple = cursor.fetchone()
    except Exception as err:
        logger.error(err)
        return None
    return result

def setHoldemRecordStatus(db: Connection, userID: int, tableUUID: str, status: int) -> bool:
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        sql: str = f"UPDATE `holdemGameRecord` SET `status` = {status} WHERE `holdemGameRecord`.`userID` = '{userID}' AND `holdemGameRecord`.`tableUUID` = '{tableUUID}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True




