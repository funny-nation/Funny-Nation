import re
from loguru import logger
from discord import Client, Reaction, Member, RawReactionActionEvent, Guild, TextChannel, PartialEmoji
from typing import List
from src.controller.routes.getReward import getRward
import configparser
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from discord import Client, Message
from pymysql import Connection

async def eventReaction(self: Client, db: Connection, event: RawReactionActionEvent, message: Message, command: str, eventAdmin: List):
    emoji: PartialEmoji = event.emoji


    await getRward(self)
