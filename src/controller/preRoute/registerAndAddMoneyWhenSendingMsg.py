import sys
import os

from loguru import logger
from pymysql import Connection

from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.model.userManagement import getUser, addNewUser, editUser, deleteUser
from src.model.cashFlowManagement import addNewCashFlow
from datetime import datetime
import configparser
from src.utils.readConfig import getGeneralConfig, getCashFlowMsgConfig

generalConfig = getGeneralConfig()
cashFlowMsgConfig = getCashFlowMsgConfig()


def registerAndAddMoneyWhenSendingMsg(userID: int, hasBoosted: bool, db: Connection) -> bool:
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
    userInfo: tuple = getUser(db, userID)
    # Check if user existed
    if userInfo is None:
        # not existed? create a new account
        if not addNewUser(db, userID):
            logger.error(f"Cannot create new account to {userID} when sending message. ")
            return False
        userInfo: tuple = getUser(db, userID)
        logger.info(f"New account created for {userID}")
        if userInfo is None:
            logger.error(f"Cannot get {userID} information")
            return False
    addMoneyToUserForMessageResult: bool = addMoneyToUserForMessage(db, userInfo)
    userInfo: tuple = getUser(db, userID)
    addMoneyToUserForCheckInResult: bool = addMoneyToUserForCheckIn(db, userInfo, hasBoosted)
    return addMoneyToUserForMessageResult and addMoneyToUserForCheckInResult


def addMoneyToUserForMessage(db, userInfo) -> bool:
    """
    Add money to user from sending message
    :param db: Database connection Object
    :param userInfo: user information tuple
    :return: True if no error
    """
    now: datetime = datetime.utcnow()
    nowTimeStamp: float = datetime.timestamp(now)
    lastEarnFromMessageTimeStamp: float = datetime.timestamp(userInfo[2])
    moneyAdded: int = int(userInfo[1]) + int(generalConfig['moneyEarning']['perMessage'])
    if (nowTimeStamp - lastEarnFromMessageTimeStamp) >= 60:
        editUserResult: bool = editUser(db, userInfo[0], money=moneyAdded, lastEarnFromMessage=now.strftime("%Y-%m-%d %H:%M:%S"))
        if editUserResult:
            logger.info(f"Added {generalConfig['moneyEarning']['perMessage']} to user {str(userInfo[0])}")
            if not addNewCashFlow(db, userInfo[0], generalConfig['moneyEarning']['perMessage'], cashFlowMsgConfig['dailyMoneyEarning']['earnMoneyFromMessage']):
                logger.error(f"Cannot add to cash flow for {userInfo[0]}")
            return True
        else:
            return False
    logger.info(f"No added to {str(userInfo[0])}")
    return True


def addMoneyToUserForCheckIn(db, userInfo, hasBoosted) -> bool:
    """
    Add money to user from daily check in
    :param db:
    :param userInfo:
    :param hasBoosted:
    :return: True if no error
    """
    now: datetime = datetime.utcnow()
    if now.day != userInfo[3].day:
        moneyAdded: int = userInfo[1] + int(generalConfig['moneyEarning']['perCheckIn'])
        moneyDelta: int = int(generalConfig['moneyEarning']['perCheckIn'])
        if hasBoosted:
            moneyAdded += 2 * int(generalConfig['moneyEarning']['perCheckIn'])
            moneyDelta *= 3
        editResult: bool = editUser(db, userInfo[0], money=moneyAdded, lastCheckIn=now.strftime("%Y-%m-%d %H:%M:%S"))
        if editResult:
            logger.info(f"Added {moneyDelta} to user {str(userInfo[0])}")
            if not addNewCashFlow(db, userInfo[0], moneyDelta, cashFlowMsgConfig['dailyMoneyEarning']['earnFromCheckIn']):
                logger.error(f"Cannot add to cash flow for {userInfo[0]}")
            return True
        else:
            return False

    return True

