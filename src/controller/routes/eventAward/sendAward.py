from discord import Client, Message, User
from pymysql import Connection
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.model.luckyMoneyManagement import newLuckyMoney
from src.utils.readConfig import getLanguageConfig, getMajorConfig

def sendAward(self: Client, message: Message, db: Connection, money: int, quantity: int):

    return