from discord import Client, Message
from pymysql import Connection
from util.casino.Casino import Casino
from src.controller.onMessage.blackJack.hit import blackJackHitWithPrivateMessage
from src.controller.onMessage.blackJack.stay import blackJackStayWithPrivateMsg

import re


async def onPrivateMessage(self: Client, message: Message, db: Connection, casino: Casino):

    if re.match(f"^要$", message.content):
        await blackJackHitWithPrivateMessage(self, message, casino)

    if re.match(f"^不要$", message.content):
        await blackJackStayWithPrivateMsg(self, message, casino)
