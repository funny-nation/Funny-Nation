from datetime import datetime

from discord import Message, Member
from pymysql import Connection
from src.model.userManagement import getUser, addMoneyToUser, editUser
from src.model.cashFlowManagement import addNewCashFlow
from src.utils.readConfig import getGeneralConfig, getCashFlowMsgConfig
from loguru import logger
import embedLib.checkIn

generalConfig = getGeneralConfig()
moneyAddForSubscriberCheckin: int = int(generalConfig['moneyEarning']['boosterCheckinEarning'])
cashFlowConfig = getCashFlowMsgConfig()
checkInCashFlowName = cashFlowConfig['dailyMoneyEarning']['checkIn']

async def checkInEarning(message: Message, db: Connection):
    """
    For check in purpose, pre rote
    Only subscriber can check in
    :param message:
    :param db:
    :return:
    """

    thisMember: Member = message.author
    userInfo: tuple = getUser(db, thisMember.id)
    now: datetime = datetime.utcnow()
    if now.day == userInfo[3].day:
        return

    if thisMember.premium_since is None:
       return

    if not addMoneyToUser(db, thisMember.id, moneyAddForSubscriberCheckin):
        logger.error(f"Cannot add money to user {thisMember}")
        return

    addNewCashFlow(db, thisMember.id, moneyAddForSubscriberCheckin, checkInCashFlowName)

    if not editUser(db, thisMember.id, lastCheckIn=now.strftime("%Y-%m-%d %H:%M:%S")):
        logger.error(f"Cannot change user last checkin for {thisMember}")
        return

    embed = embedLib.checkIn.getEmbed(moneyAddForSubscriberCheckin / 100, thisMember)
    await message.channel.send(embed=embed)



