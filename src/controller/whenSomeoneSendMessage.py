import sys
import os

from loguru import logger

sys.path.append(os.path.dirname(__file__) + '/../model')
import makeDatabaseConnection
import userManagement
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/../../config.ini')


def whenSomeoneSendMessage(userID, hasBoosted, db) -> bool:
    """
    Call if someone send message
    :param db: Database object
    :param userID: User ID int(64)
    :param hasBoosted: boolean, user has boosted or not
    :return: True if no error
    """
    if db is None:
        return False
    # get user information
    userInfo = userManagement.getUser(db, userID)
    # Check if user existed
    if userInfo is None:
        # not existed? create a new account
        if not userManagement.addNewUser(db, userID):
            logger.error(f"Cannot create new account to {userID} when sending message. ")
            return False
        userInfo = userManagement.getUser(db, userID)
        logger.info("New account created for " + userID)
        if userInfo is None:
            logger.error(f"Cannot get {userID} information")
            return False
    addMoneyToUserForMessageResult = addMoneyToUserForMessage(db, userInfo)
    userInfo = userManagement.getUser(db, userID)
    addMoneyToUserForCheckInResult = addMoneyToUserForCheckIn(db, userInfo, hasBoosted)
    return addMoneyToUserForMessageResult and addMoneyToUserForCheckInResult


def addMoneyToUserForMessage(db, userInfo) -> bool:
    """
    Add money to user from sending message
    :param db: Database connection Object
    :param userInfo: user information tuple
    :return: True if no error
    """
    now = datetime.utcnow()
    nowTimeStamp = datetime.timestamp(now)
    lastEarnFromMessageTimeStamp = datetime.timestamp(userInfo[2])
    moneyAdded = int(userInfo[1]) + int(config['moneyEarning']['perMessage'])
    if (nowTimeStamp - lastEarnFromMessageTimeStamp) >= 60:
        logger.info(f"Added {int(config['moneyEarning']['perMessage'])} to user {userInfo[0]}")
        return userManagement.editUser(db, userInfo[0], money=moneyAdded,
                                       lastEarnFromMessage=now.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info(f"No added to {userInfo[0]}")
    return True


def addMoneyToUserForCheckIn(db, userInfo, hasBoosted) -> bool:
    """
    Add money to user from daily check in
    :param db:
    :param userInfo:
    :param hasBoosted:
    :return: True if no error
    """
    now = datetime.utcnow()
    if now.day != userInfo[3].day:
        moneyAdded = userInfo[1] + int(config['moneyEarning']['perCheckIn'])
        moneyDelta = int(config['moneyEarning']['perCheckIn'])
        if hasBoosted:
            moneyAdded += 2 * int(config['moneyEarning']['perCheckIn'])
            moneyDelta *= 3
        logger.info(f"Added {moneyDelta} to user {userInfo[0]}")
        return userManagement.editUser(db, userInfo[0], money=moneyAdded, lastCheckIn=now.strftime("%Y-%m-%d %H:%M:%S"))
    return True


def test_whenSomeoneSendMessage():
    db = makeDatabaseConnection.makeDatabaseConnection()
    assert whenSomeoneSendMessage('123', False, db) is True
    assert whenSomeoneSendMessage('123', False, db) is True
    userinfo = userManagement.getUser(db, '123')
    assert userinfo[1] == 0  # Check if send message within 1 minute
    assert userManagement.editUser(db, '123', lastEarnFromMessage='2000-1-1 1:1:1', lastCheckIn='2000-1-1 1:1:1') is True
    assert whenSomeoneSendMessage('123', False, db) is True
    userinfo = userManagement.getUser(db, '123')
    moneyShouldBe = int(config['moneyEarning']['perMessage']) + int(config['moneyEarning']['perCheckIn'])
    assert userinfo[1] == moneyShouldBe  # Check if message send after more than one day
    now = datetime.utcnow()
    assert datetime.timestamp(now) - datetime.timestamp(userinfo[2]) < 10
    assert datetime.timestamp(now) - datetime.timestamp(userinfo[3]) < 10
    assert userManagement.deleteUser(db, '123') is True
    db.close()


def test_whenSomeoneSendMessageForBoostedUser():
    db = makeDatabaseConnection.makeDatabaseConnection()
    assert whenSomeoneSendMessage('123', True, db) is True
    assert whenSomeoneSendMessage('123', True, db) is True
    userinfo = userManagement.getUser(db, '123')
    assert userinfo[1] == 0  # Check if send message within 1 minute
    assert userManagement.editUser(db, '123', lastEarnFromMessage='2000-1-1 1:1:1', lastCheckIn='2000-1-1 1:1:1') is True
    assert whenSomeoneSendMessage('123', True, db) is True
    userinfo = userManagement.getUser(db, '123')
    moneyShouldBe = int(config['moneyEarning']['perMessage']) + (int(config['moneyEarning']['perCheckIn']) * 3)
    assert userinfo[1] == moneyShouldBe  # Check if message send after more than one day
    now = datetime.utcnow()
    assert datetime.timestamp(now) - datetime.timestamp(userinfo[2]) < 10
    assert datetime.timestamp(now) - datetime.timestamp(userinfo[3]) < 10
    assert userManagement.deleteUser(db, '123') is True
    db.close()
