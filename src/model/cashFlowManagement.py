from loguru import logger
from datetime import datetime

from pymysql import Connection
from pymysql.cursors import Cursor


def addNewCashFlow(db: Connection, userID: int, amount: int, msg: str) -> bool:
    """
    Add new cash flow to database
    :param db: database connection object
    :param userID: user's ID int
    :param amount: amount of money, could be negative, int
    :param msg: String
    :return: boolean true if no error.
    """
    if db is None:
        return False
    now: datetime = datetime.utcnow()
    currentTime: str = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"INSERT INTO `cashFlow` (`flowID`, `userID`, `amount`, `message`, `date`) VALUES (NULL, {userID}, {amount}, '{msg}', '{currentTime}');")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def deleteCashFlow(db: Connection, flowID: int) -> bool:
    """
    Delete existed Cash flow
    :param db: database object
    :param flowID: cash flow unique id
    :return: boolean, true if no error
    """
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"DELETE FROM `cashFlow` WHERE `flowID` = {flowID};")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def deleteCashFlowByUserID(db: Connection, userID: int) -> bool:
    """
    Delete existed Cash flow
    :param db: database object
    :param userID: userID
    :return: boolean, true if no error
    """
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"DELETE FROM `cashFlow` WHERE `userID` = {userID};")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def getCashflowsByUserID(db: Connection, userID: int) -> tuple or None:
    """
    Get cash flows by user's ID
    :param db: database object
    :param userID: user's ID
    :return: Tuple of cash flow
    ((flowID, userID, amount, message, date), ((flowID, userID, amount, message, date)))
    """
    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `cashFlow` WHERE `userID` = '{userID}';")
        results: tuple = cursor.fetchall()
    except Exception as err:
        logger.error(err)
        return None
    return results


def get10RecentCashflowsByUserID(db: Connection, userID: int, msg: str or None) -> tuple or None:
    """
    Get 10 cash flows by user's ID
    :param msg: message detail for cash flow
    :param db: database object
    :param userID: user's ID
    :return: Tuple of cash flow
    ((flowID, userID, amount, message, date), ((flowID, userID, amount, message, date)))
    """
    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        if msg is None:
            cursor.execute(f"SELECT * FROM `cashFlow` WHERE `userID` = {userID} ORDER BY `cashFlow`.`date` DESC LIMIT 10;")
        else:
            args: str = msg
            cursor.execute(f"SELECT * FROM `cashFlow` WHERE `userID` = {userID} AND `message` LIKE %s ORDER BY `cashFlow`.`date` DESC LIMIT 10;", args)
        results: tuple = cursor.fetchall()
    except Exception as err:
        logger.error(err)
        return None
    return results


