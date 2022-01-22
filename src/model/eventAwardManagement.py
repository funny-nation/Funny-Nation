from loguru import logger
from datetime import datetime
import uuid
from pymysql import Connection
from pymysql.cursors import Cursor

def newAward(db: Connection, senderID: int, messageID: int, money: int, eventName: str) -> str:
    if db is None:
        return ''

    newUUID = str(uuid.uuid1())
    try:
        recipient = "{}"
        cursor: Cursor = db.cursor()
        cursor.execute(f"INSERT INTO `eventAward` (`eventID`, `eventManagerID`, `eventMsgID`, `money`, `eventName`, `recipient`) VALUES ('{newUUID}', {senderID}, {messageID}, {money}, {eventName}, {recipient});")
        db.commit()

    except Exception as err:
        logger.error(err)
        return ''

    return newUUID

def deletAward(db: Connection,  uuidForDelete: str) -> bool:
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"DELETE FROM `eventAward` WHERE `uuid` = '{uuidForDelete}';")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True

def takeAward(db: Connection, messageID: int, money: int):
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        sql = f"UPDATE `eventAward` SET `award` = '{money}' WHERE `eventAward`.`eventMsgID` = '{messageID}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True

def getEventAward(db: Connection, messageID: int):
    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `eventAward` WHERE `eventMsgID` = '{messageID}';")
        result: tuple = cursor.fetchone()
    except Exception as err:
        logger.error(err)
        return None
    return result

def editRecipient(db: Connection, messageID: int, Recipient: str):
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        sql = f"UPDATE `eventAward` SET  `recipient` - {Recipient} WHERE `eventAward` . `senderMsgID` = '{messageID}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True



