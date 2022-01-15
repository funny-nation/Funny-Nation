from loguru import logger
from datetime import datetime
import uuid
from pymysql import Connection
from pymysql.cursors import Cursor


def newLuckyMoney(db: Connection, senderID: int, messageID: int, quantity: int, money: int) -> str:
    if db is None:
        return False

    newUUID = str(uuid.uuid1())

    try:
        whoTakeInit = "{}"
        cursor: Cursor = db.cursor()
        cursor.execute(f"INSERT INTO `luckyMoney` (`uuid`, `sender`, `moneyLeft`, `quantityLeft`, `senderMsgID`, `whoTake`) VALUES ('{newUUID}', {senderID}, {money}, {quantity}, {messageID}, '{whoTakeInit}');")
        db.commit()
    except Exception as err:
        logger.error(err)
        return ''

    return newUUID


def deleteLuckyMoney(db: Connection, uuidForDelete: str) -> bool:

    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"DELETE FROM `luckyMoney` WHERE `uuid` = '{uuidForDelete}';")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def takeLuckyMoney(db: Connection, messageID: int, money: int):

    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        sql = f"UPDATE `luckyMoney` SET `moneyLeft` = `moneyLeft` - {money}, `quantityLeft` = `quantityLeft` - 1 WHERE `luckyMoney`.`senderMsgID` = '{messageID}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True

def getLuckyMoney(db: Connection, messageID: int):
    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `luckyMoney` WHERE `senderMsgID` = '{messageID}';")
        result: tuple = cursor.fetchone()
    except Exception as err:
        logger.error(err)
        return None
    return result


def editWhoTake(db: Connection, messageID: int, whoTake: str):

    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        sql = f"UPDATE `luckyMoney` SET `whoTake` = '{whoTake}' WHERE `luckyMoney`.`senderMsgID` = '{messageID}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True