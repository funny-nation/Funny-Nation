from loguru import logger
from datetime import datetime

from pymysql import Connection
from pymysql.cursors import Cursor


def addNewUser(db: Connection, userID: int) -> bool:
    """
    Add new user to database
    :param db: database object instance
    :param userID: User ID
    :return: Boolean True if no error
    """
    if db is None:
        return False
    now: datetime = datetime.utcnow()
    currentTime: str = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"INSERT INTO `user` (`userID`, `money`, `lastEarnFromMessage`, `lastCheckIn`, `robSince`) VALUES ('{userID}', '0', '{currentTime}', '{currentTime}', '{currentTime}');")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def deleteUser(db: Connection, userID: int) -> bool:
    """
    Delete existed user
    :param db: database object instance
    :param userID: User ID
    :return: Boolean True if no error
    """
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"DELETE FROM `user` WHERE `userID` = {userID};")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def getUser(db: Connection, userID: int) -> tuple or None:
    """
    Get User Information
    :param db: database object instance
    :param userID: User ID
    :return: tuple User information from database
    return none if not founded.
    """
    if db is None:
        return None
    try:
        cursor: Cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `user` WHERE `userID` = '{userID}';")
        result: tuple = cursor.fetchone()
    except Exception as err:
        logger.error(err)
        return None
    return result


def editUser(db: Connection, userID: int, *,
             money: int = None,
             lastCheckIn: str = None,
            lastEarnFromMessage: str = None
             ) -> bool:
    """
    Edit user information
    :param db: database object instance
    :param userID: User ID
    :param money: money
    :param lastCheckIn: last check in time
    :param lastEarnFromMessage: last message that earned money
    :return: True if no error
    """
    if db is None:
        return False
    sqlFragment = ''
    if lastEarnFromMessage is not None:
        sqlFragment += f" `lastEarnFromMessage` = '{lastEarnFromMessage}',"
    if money is not None:
        sqlFragment += f" `money` = '{money}',"
    if lastCheckIn is not None:
        sqlFragment += f" `lastCheckIn` = '{lastCheckIn}',"
    try:
        cursor: Cursor = db.cursor()
        sql: str = f"UPDATE `user` SET{sqlFragment[:-1]} WHERE `user`.`userID` = '{userID}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def getLeaderBoard(db: Connection) -> tuple or None:
    """
    get leader board of top 10
    :param db: Database object
    :return: Tuple of user with money
    ((userid, money), (user2ID, money))
    """
    if db is None:
        return None
    try:
        cursor = db.cursor()
        cursor.execute("SELECT `userID`, `money` FROM `user` ORDER BY `money` DESC LIMIT 10;")
        result: tuple = cursor.fetchall()
    except Exception as err:
        logger.error(err)
        return None
    return result


def addMoneyToUser(db: Connection, userID: int, money: int) -> bool:
    """
    Add money to user
    :param db: database object instance
    :param userID: User id
    :param money: amount that add to user's account
    :return: True if no error
    """
    if db is None:
        return False
    try:
        cursor: Cursor = db.cursor()
        sql = f"UPDATE `user` SET `money` = `money` + {money} WHERE `user`.`userID` = '{userID}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True

