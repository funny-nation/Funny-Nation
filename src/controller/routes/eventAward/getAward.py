import json
from typing import List
from discord import Client, TextChannel, Guild, Member, message, DMChannel, RawReactionActionEvent
from pymysql import Connection
import src.model.eventAwardManagement as eventAwardManagement
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.utils.readConfig import getLanguageConfig, getMajorConfig
from loguru import logger

async def getAward(self: Client, event: RawReactionActionEvent, db: Connection, channelID: int):
    languageConfig = getLanguageConfig()




