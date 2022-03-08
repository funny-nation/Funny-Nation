import time
import _thread
from pymysql import Connection
from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.utils.readConfig import getGeneralConfig, getCashFlowMsgConfig
from src.model.activityStatManagement import getActivityStatByUser, getAllActivityStat, deleteAllActivityStat
from src.model.serverInfoManagement import getOnlineMinute
from loguru import logger
import math
from src.model.userManagement import addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow



def addMoneyToUserByActivity():
    """
    Add money to user based on their activity stats
    :param db:
    :return:
    """
    _thread.start_new_thread(__helper, ())

def __helper():
    """
    This would run once per minutes defined in generalConfig.ini
    :param db:
    :return:
    """

    generalConfig = getGeneralConfig()
    cashFlowMsgConfig = getCashFlowMsgConfig()
    antiInvolutionFactor = float(generalConfig['moneyEarning']['antiInvolutionFactor'])

    periodOfRunInSecond = int(generalConfig['moneyEarning']['earningPeriodInMinute']) * 60
    while True:
        time.sleep(periodOfRunInSecond)
        db: Connection = makeDatabaseConnection()
        serverOnlineTime = getOnlineMinute(db)
        if serverOnlineTime is None:
            logger.error(f"Cannot fetch server online time from database. ")
            continue

        totalReducingPeriodPassed = serverOnlineTime // int(generalConfig['moneyEarning']['reducePeriodInMinute'])
        initialPot = int(generalConfig['moneyEarning']['initialPeriodEarning'])
        reduceFactorBetweenPeriods = float(generalConfig['moneyEarning']['reduceFactorBetweenPeriods'])
        potInThisPeriod = initialPot * (reduceFactorBetweenPeriods ** totalReducingPeriodPassed)

        logger.info(f"Pot in this period is {potInThisPeriod}")

        moneyDistribution = {}

        activityStats = getAllActivityStat(db)

        if len(activityStats) == 0:
            logger.info(f"One earning period passed; no one earning this")
            continue

        distributionSum = 0

        for activityStat in activityStats:
            userID = activityStat[0]
            activityPoint = activityStat[1]

            moneyDistributionForThisUser = activityPoint ** (1 / antiInvolutionFactor)

            distributionSum += moneyDistributionForThisUser

            moneyDistribution[userID] = moneyDistributionForThisUser
        totalMoneyAdded = 0
        for userID in moneyDistribution:
            moneyAdd = round((moneyDistribution[userID] / distributionSum) * potInThisPeriod)
            totalMoneyAdded += moneyAdd
            addMoneyToUser(db, userID, moneyAdd)
            addNewCashFlow(db, userID, moneyAdd, cashFlowMsgConfig['dailyMoneyEarning']['onlineEarning'])

        deleteAllActivityStat(db)
        db.close()
        logger.info(f"One earning period passed; there are {len(activityStats)} users totally receive {totalMoneyAdded}")
