import json
from typing import List
from discord import Client, TextChannel, Guild, Member, Message
from pymysql import Connection
from loguru import logger
from src.model.eventAwardManagement import deletAward, newAward, editRecipient, takeAward, getEventAward
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.model.luckyMoneyManagement import newLuckyMoney
from src.utils.readConfig import getLanguageConfig, getMajorConfig

def adminProof(self:Client, message: Message, db: Connection, involve: List):
    for each in range(len(involve)):
        await involve[each]
        await message.add_reaction("alal")
    logger.error(f"Cannot add money to user {message.mentions[0].id}")
    