from loguru import logger
from datetime import datetime
from makeDatabaseConnection import makeDatabaseConnection


def addNewUser(db, userID):
    """
    Add new user to database
    :param db: database object instance
    :param userID: User ID int(64)
    :return: Boolean True if no error
    """
    if db is None:
        return False
    now = datetime.now()
    currentTime = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO `user` (`userID`, `money`, `lastMessage`, `lastCheckIn`) VALUES ('{userID}', '0', '{currentTime}', '{currentTime}');")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def deleteUser(db, userID):
    """
    Delete existed user
    :param db: database object instance
    :param userID: User ID int(64)
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


def getUser(db, userID):
    """
    Get User Information
    :param db: database object instance
    :param userID: User ID int(64)
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




def test_():
    db = makeDatabaseConnection()
    assert addNewUser(db, '123') is True
    assert getUser(db, '123') is not None
    assert deleteUser(db, '123') is True
    assert getUser(db, '123') is None
    db.close()
