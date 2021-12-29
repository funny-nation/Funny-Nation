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
    """

    :param db:
    :param userID:
    :param tableUUID:
    :param status:
        0 represent in progress; 1 represent lose or fold; 2 represent win; 3 represent game close
    :return:
    """
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


def addMoneyToHoldemRecord(db: Connection, userID: int, tableUUID: str, money: int) -> bool:

    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        sql = f"UPDATE `holdemGameRecord` SET `moneyInvested` = `moneyInvested` + {money} WHERE `userID` = '{userID}' AND `tableUUID` = '{tableUUID}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True




