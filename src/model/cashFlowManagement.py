from loguru import logger
from datetime import datetime
from makeDatabaseConnection import makeDatabaseConnection


def addNewCashFlow(db, userID, amount, msg) -> bool:
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
    now = datetime.utcnow()
    currentTime = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO `cashFlow` (`flowID`, `userID`, `amount`, `message`, `date`) VALUES (NULL, {userID}, {amount}, '{msg}', '{currentTime}');")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def deleteCashFlow(db, flowID) -> bool:
    """
    Delete existed Cash flow
    :param db: database object
    :param flowID: cash flow unique id
    :return: boolean, true if no error
    """
    if db is None:
        return False
    try:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM `cashFlow` WHERE `flowID` = {flowID};")
        db.commit()
    except Exception as err:
        logger.error(err)
        return False
    return True


def getCashflowsByUserID(db, userID):
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
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `cashFlow` WHERE `userID` = '{userID}';")
        results = cursor.fetchall()
    except Exception as err:
        logger.error(err)
        return None
    return results


def get10RecentCashflowsByUserID(db, userID, msg):
    """
    Get 10 cash flows by user's ID
    :param db: database object
    :param userID: user's ID
    :return: Tuple of cash flow
    ((flowID, userID, amount, message, date), ((flowID, userID, amount, message, date)))
    """
    if db is None:
        return None
    try:
        cursor = db.cursor()
        if msg is None:
            cursor.execute(f"SELECT * FROM `cashFlow` WHERE `userID` = {userID} ORDER BY `cashFlow`.`date` DESC LIMIT 10;")
        else:
            args = msg
            cursor.execute(f"SELECT * FROM `cashFlow` WHERE `userID` = {userID} AND `message` LIKE %s ORDER BY `cashFlow`.`date` DESC LIMIT 10;", args)
        results = cursor.fetchall()
    except Exception as err:
        logger.error(err)
        return None
    return results


def test_addNewCashFlow():
    db = makeDatabaseConnection()
    assert addNewCashFlow(db, '123123123', 100, "转账") is True
    assert addNewCashFlow(db, '123123123', -50, "转账") is True
    cashflow = getCashflowsByUserID(db, '123123123')
    cashFlow10Result = get10RecentCashflowsByUserID(db, '123123123', "转账")
    assert len(cashFlow10Result) == 2
    assert cashflow is not None
    assert len(cashflow) == 2
    assert deleteCashFlow(db, cashflow[0][0]) is True
    assert deleteCashFlow(db, cashflow[1][0]) is True
    db.close()