import re
from loguru import logger
from typing import List
import configparser
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.controller.routes.eventReaction import eventReaction
from discord import Client, Message
from pymysql import Connection

async def eventPublish(self: Client, db: Connection, message: Message, command: str, eventAdmin: List):
    adminString = re.findall(f"^领奖" +"!活动" +"[0-9]+\.?[0-9]$", command)
    author = message.author.id
    if author not in eventAdmin:
        await message.channel.send("你不是管理员哦")
        return
    await eventReaction(self, db, message, command)