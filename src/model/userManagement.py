from loguru import logger
from datetime import datetime
from src.model.makeDatabaseConnection import makeDatabaseConnection


def addNewUser(db, userID) -> bool:
    """
    Add new user to database
    :param db: database object instance
    :param userID: User ID
    :return: Boolean True if no error
    """
    if db is None:
        return False
    now = datetime.utcnow()
    currentTime = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO `user` (`userID`, `money`, `lastEarnFromMessage`, `lastCheckIn`, `robSince`) VALUES ('{userID}', '0', '{currentTime}', '{currentTime}', '{currentTime}');")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def deleteUser(db, userID) -> bool:
    """
    Delete existed user
    :param db: database object instance
    :param userID: User ID
    :return: Boolean True if no error
    """
    if db is None:
        return False
    try:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM `user` WHERE `userID` = {userID};")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def getUser(db, userID) -> tuple:
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
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `user` WHERE `userID` = '{userID}';")
        result = cursor.fetchone()
    except Exception as err:
        logger.error(err)
        return None
    return result


def editUser(db, userID, *,
             money=None,
             lastCheckIn=None,
            lastEarnFromMessage=None
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
        cursor = db.cursor()
        sql = f"UPDATE `user` SET{sqlFragment[:-1]} WHERE `user`.`userID` = '{userID}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def getLeaderBoard(db) -> tuple:
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
        result = cursor.fetchall()
    except Exception as err:
        logger.error(err)
        return None
    return result


def addMoneyToUser(db, userID, money) -> bool:
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
        cursor = db.cursor()
        sql = f"UPDATE `user` SET `money` = `money` + {money} WHERE `user`.`userID` = '{userID}';"
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def test_():
    testingTime1 = '2000-01-01 01:01:01'
    testingTime2 = '2001-02-02 02:02:02'
    db = makeDatabaseConnection()
    assert addNewUser(db, '123') is True
    assert editUser(db, '123', money=1000, lastCheckIn=testingTime1, lastEarnFromMessage=testingTime2) is True
    getUserResult = getUser(db, '123')
    assert getUserResult[2].strftime("%Y-%m-%d %H:%M:%S") == testingTime2
    assert getUserResult[3].strftime("%Y-%m-%d %H:%M:%S") == testingTime1
    assert addMoneyToUser(db, '123', 10)
    getUserResult = getUser(db, '123')
    assert getUserResult[1] == 1010
    assert addMoneyToUser(db, '123', -20)
    assert getUser(db, '123')[1] == 990
    assert getLeaderBoard(db) is not None
    assert deleteUser(db, '123') is True
    assert getUser(db, '123') is None
    db.close()
