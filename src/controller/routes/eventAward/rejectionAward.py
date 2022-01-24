import src.model.eventAwardManagement as eventAwardManagement
from discord import Client, TextChannel, Guild, Member, Message
from pymysql import Connection
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
import list
from src.utils.readConfig import getLanguageConfig, getMajorConfig
import re

async def rejectAward(self: Client, messageID: int, db: Connection, channelID: int, userID: int):
    return