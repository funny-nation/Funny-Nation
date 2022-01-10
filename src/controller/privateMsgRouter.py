from discord import Client, Message
from pymysql import Connection

from src.Storage import Storage
from src.utils.casino.Casino import Casino
from src.controller.routes.blackJack.hit import blackJackHitWithPrivateMessage
from src.controller.routes.blackJack.stay import blackJackStayWithPrivateMsg
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting

import re


async def privateMsgRouter(self: Client, message: Message, db: Connection, storage: Storage):

    if re.match(f"^要$", message.content):
        await blackJackHitWithPrivateMessage(self, message, storage.casino, storage.gamePlayerWaiting)

    if re.match(f"^不要$", message.content):
        await blackJackStayWithPrivateMsg(self, db, message, storage.casino, storage.gamePlayerWaiting)
