from loguru import logger
from datetime import datetime

from pymysql import Connection
from pymysql.cursors import Cursor


def addNewLottery(db: Connection, publisherId: int, msgId: int, name: str, price: int, quantity: int, isOpen: int) -> bool:
    """
    Add a new lottery entry
    :param db: database object instance
    :param publisherId: lottery publisher ID
    :param msgId: lottery message ID
    :param name: reward name
    :param price: reward price
    :param quantity: reward quantity
    :param isOpen: if the lottery is open: 0 is open, 1 is closed
    :return: True if no error
    """
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"INSERT INTO `lottery` (`publisherId`, `msgId`, `name`, `quantity`, `price`, `isOpen`) VALUES ('{publisherId}', '{msgId}', '{name}', {quantity}, {price}, '{isOpen}');")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def getLottery(db: Connection, msgID: int) -> tuple or None:
    """
    Get a lottery information
    :param db: database object instance
    :param msgID: lottery message ID
    :return: tuple User information from database
    return none if not found
    """
    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `lottery` WHERE `msgId` = '{msgID}';")
        result: tuple = cursor.fetchone()
    except Exception as err:
        logger.error(err)
        return None
    return result


def updateLottery(db: Connection, msgId: int, *,
                  publisherId: int = None,
                  name: str = None,
                  price: int = None,
                  quantity: int = None,
                  isOpen: int = None) -> bool:
    """
    Update lottery information
    :param db: database object instance
    :param msgId: lottery message ID
    :param publisherId: ID of the publisher who initiated the lottery
    :param name: reward name
    :param price: price of the lottery
    :param quantity: max capacity of the lottery
    :param isOpen: if the lottery is open
    :return: True if no error
    """
    if db is None:
        return False
    sqlFragment = ''
    if publisherId is not None:
        sqlFragment += f" `publisherID` = '{publisherId}',"
    if name is not None:
        sqlFragment += f" `name` = '{name}',"
    if price is not None:
        sqlFragment += f" `price` = '{price}',"
    if quantity is not None:
        sqlFragment += f" `quantity` = {quantity},"
    if isOpen is not None:
        sqlFragment += f" `isOpen` = {isOpen},"
    try:
        cursor: Cursor = db.cursor()
        sql: str = f"UPDATE `lottery` SET{sqlFragment[:-1]} WHERE `lottery`.`msgID` = '{msgId}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def deleteLottery(db: Connection, msgID: int) -> bool:
    """
    Delete lottery information
    :param db: database object instance
    :param msgID: Message ID
    :return: Boolean True if no error
    """
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"DELETE FROM `lottery` WHERE `msgID` = {msgID};")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def addNewLotteryRecipient(db: Connection, recipientId: int, msgId: int) -> bool:
    """
    Add a new lottery recipient information
    :param db: database object instance
    :param recipientId: participant ID of those who participated the lottery
    :param msgId: lottery message ID
    :return: True if no error
    """
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"INSERT INTO `lotteryRecipient` (`recipientID`, `msgID`) VALUES ('{recipientId}', '{msgId}');")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def getLotteryRecipient(db: Connection, msgId: int) -> list[int] or None:
    """
    Get a collection of recipient information
    :param db: database object instance
    :param msgId: lottery message ID
    :return: a collection of recipients who participated the lottery or None if there's error
    """
    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `lotteryRecipient` WHERE `msgID` = '{msgId}';")
        result: list = list(cursor.fetchall())
    except Exception as err:
        logger.error(err)
        return None
    return result


def deleteLotteryRecipient(db: Connection, msgId: int) -> bool:
    """
    Delete a lottery recipient information
    :param db: database object instance
    :param msgId: lottery message ID
    :return: True if no error
    """
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"DELETE FROM `lotteryRecipient` WHERE `msgID` = {msgId};")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True
