from typing import List

from src.utils.casino.table.BlackJackTable import BlackJackTable

from discord import Client, Message, Member, DMChannel
from loguru import logger

from src.utils.casino import Casino
from src.utils.poker.Card import Card
from src.utils.poker.pokerImage import getPokerImage
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.routes.blackJack.stay import blackJackStayWithPrivateMsg
from src.model.makeDatabaseConnection import makeDatabaseConnection

from src.utils.readConfig import getLanguageConfig

languageConfig = getLanguageConfig()



async def blackJackHitWithPrivateMessage(self: Client, message: Message, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    player: Member = message.author
    table: BlackJackTable = casino.getTableByPlayerID(player.id)
    if table is None:
        notInGame = str(languageConfig["game"]["notInGame"])\
            .replace('?@user', player.display_name)
        await message.channel.send(notInGame)
        return
    if table.shouldStopHitting(player.id):
        noHit = str(languageConfig["blackJack"]["noHit"])
        await message.channel.send(noHit)
        return
    if table.gameOver:
        return
    table.hit(player.id)
    cards: List[Card] = table.viewCards(player.id)
    await message.channel.send(file=getPokerImage(cards))
    doYouWantToHit = str(languageConfig["blackJack"]["doYouWantToHit"])
    await message.channel.send(doYouWantToHit)
    logger.info(f"Player {player.id} hit on black jack")

    async def timeoutFun():
        db = makeDatabaseConnection()
        await blackJackStayWithPrivateMsg(self, db, message, casino, gamePlayerWaiting, removeWait=False)
        db.close()

    async def warningFun():
        warning = str(languageConfig["blackJack"]["timeOutWarningInPrivateMSG"])
        await message.channel.send(warning)

    await gamePlayerWaiting.newWait(player.id, timeoutFun, warningFun)
