from discord import Client, Message
from pymysql import Connection

from src.Storage import Storage
from src.controller.routes.blackJack.hit import blackJackHitWithPrivateMessage
from src.controller.routes.blackJack.stay import blackJackStayWithPrivateMsg
from src.controller.routes.anonymityBoard import anonymityBoard

import re


async def privateMsgRouter(self: Client, message: Message, db: Connection, storage: Storage):

    if re.match(f"^要$", message.content):
        await blackJackHitWithPrivateMessage(self, message, storage.casino, storage.gamePlayerWaiting)
        return

    if re.match(f"^不要$", message.content):
        await blackJackStayWithPrivateMsg(self, db, message, storage.casino, storage.gamePlayerWaiting)
        return

    if re.match(f"^匿名 .+", message.content):
        await anonymityBoard(self, message, message.content, db, storage.anonymityBoardChannel)
        return
