import re
from loguru import logger
from discord import Client, Reaction, Member, RawReactionActionEvent, Guild, TextChannel, PartialEmoji
from typing import List
import configparser
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from discord import Client, Message
from pymysql import Connection

async def getRward(self: Client, db: Connection, event: RawReactionActionEvent, message: Message, command: str, eventAdmin: List):
    if not addMoneyToUser(db, message.mentions[0].id):
        logger.error(f"Cannot add money to user {message.mentions[0].id}")
        await message.channel.send("error")
        return
    if not addNewCashFlow(db, message.mentions[0].id, "领奖"):
        logger.error(f"Cannot create cash flow for user {message.mentions[0].id}")
        return
    return