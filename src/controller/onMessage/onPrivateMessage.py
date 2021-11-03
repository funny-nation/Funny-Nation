from discord import Client, Message
from pymysql import Connection
from src.utils.casino.Casino import Casino
from src.controller.onMessage.blackJack.hit import blackJackHitWithPrivateMessage
from src.controller.onMessage.blackJack.stay import blackJackStayWithPrivateMsg
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting

import re


async def onPrivateMessage(self: Client, message: Message, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):

    if re.match(f"^要$", message.content):
        await blackJackHitWithPrivateMessage(self, message, casino, gamePlayerWaiting)

    if re.match(f"^不要$", message.content):
        await blackJackStayWithPrivateMsg(self, message, casino, gamePlayerWaiting)
