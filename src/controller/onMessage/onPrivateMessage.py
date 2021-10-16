from discord import Client, Message
from pymysql import Connection
from src.data.casino.Casino import Casino
from src.controller.onMessage.blackJack.hit import blackJackHitWithPrivateMessage

import re


async def onPrivateMessage(self: Client, message: Message, db: Connection, casino: Casino):

    if re.match(f"^要牌$", message.content):
        await blackJackHitWithPrivateMessage(self, message, casino)
