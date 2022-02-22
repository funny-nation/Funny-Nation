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
        reduceFactorBetweenPeriods = int(generalConfig['moneyEarning']['reduceFactorBetweenPeriods'])
        potInThisPeriod = initialPot * (reduceFactorBetweenPeriods ** (totalReducingPeriodPassed + 1))

        moneyDistribution = {}

        activityStats = getAllActivityStat(db)

        if len(activityStats) == 0:
            continue

        distributionSum = 0

        for activityStat in activityStats:
            userID = activityStat[0]
            activityPoint = activityStat[1]

            moneyDistributionForThisUser = activityPoint ** (1 / antiInvolutionFactor)

            distributionSum += moneyDistributionForThisUser

            moneyDistribution[userID] = moneyDistributionForThisUser

        for userID in moneyDistribution:
            moneyAdd = math.ceil((distributionSum / moneyDistribution[userID]) * potInThisPeriod)
            addMoneyToUser(db, userID, moneyAdd)
            addNewCashFlow(db, userID, moneyAdd, cashFlowMsgConfig['dailyMoneyEarning']['onlineEarning'])

        deleteAllActivityStat(db)
        db.close()
