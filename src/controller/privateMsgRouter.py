from discord import Client, Message
from pymysql import Connection

from src.Storage import Storage
from src.utils.casino.Casino import Casino
from src.controller.routes.blackJack.hit import blackJackHitWithPrivateMessage
from src.controller.routes.blackJack.stay import blackJackStayWithPrivateMsg
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.routes.anonymityBoard import anonymityBoard
from src.controller.routes.help.getHelp import getHelp
from src.controller.routes.help.getHelpForMoney import getHelpForMoney
from src.controller.routes.help.getHelpForAnnomity import getHelpForAnnomity
from src.controller.routes.help.getHelpForBlackJack import getHelpForBlackJack
from src.controller.routes.help.getHelpForCommand import getHelpForCommand
from src.controller.routes.help.getHelpForGift import getHelpForGift
from src.controller.routes.help.getHelpForLottery import getHelpForLottery
from src.controller.routes.help.getHelpForTaxesPoker import getHelpForTaxesPoker
from src.controller.routes.help.getHelpForVIP import getHelpForVIP

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

    if re.match(f"^帮助$", message.content):
        await getHelp(self, message)
        return

    if re.match(f"^1$", message.content):
        await getHelpForMoney(self, message)
        return

    if re.match(f"^2$", message.content):
        await getHelpForCommand(self, message)
        return

    if re.match(f"^3$", message.content):
        await getHelpForGift(self, message)
        return

    if re.match(f"^4$", message.content):
        await getHelpForVIP(self, message)
        return

    if re.match(f"^5$", message.content):
        await getHelpForBlackJack(self, message)
        return

    if re.match(f"^6$", message.content):
        await getHelpForTaxesPoker(self, message)
        return

    if re.match(f"^7$", message.content):
        await getHelpForLottery(self, message)
        return

    if re.match(f"^8$", message.content):
        await getHelpForAnnomity(self, message)
        return