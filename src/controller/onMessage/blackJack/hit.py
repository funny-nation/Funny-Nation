from typing import List

from src.utils.casino.table.BlackJackTable import BlackJackTable

from discord import Client, Message, Member, DMChannel
from loguru import logger

from src.utils.casino import Casino
from src.utils.poker.Card import Card
from src.utils.poker.pokerImage import getPokerImage
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.onMessage.blackJack.stay import blackJackStay, blackJackStayWithPrivateMsg
from src.model.makeDatabaseConnection import makeDatabaseConnection

import configparser

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read("config.ini")

async def blackJackHit(self: Client, message: Message, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    table: BlackJackTable = casino.getTable(message.channel.id)
    playerID: int = message.author.id
    user: Member = message.author
    if table is None:
        notInGame = str(languageConfig["game"]["notInGame"])
        await message.channel.send(notInGame)
        return
    if not table.hasPlayer(playerID):
        notInGame = str(languageConfig["blackJack"]["notInGame"])
        await message.channel.send(notInGame)
        return

    if table.shouldStopHitting(playerID):
        noHit = str(languageConfig["blackJack"]["noHit"])
        await message.channel.send(noHit)
        return
    if table.gameOver:
        return
    table.hit(playerID)
    cards = table.viewCards(playerID)
    dmChannel: DMChannel = await user.create_dm()
    await dmChannel.send(file=getPokerImage(cards))
    logger.info(f"Player {playerID} hit on black jack")
    hit = str(languageConfig["blackJack"]["hit"])
    await dmChannel.send(hit)

    async def timeoutFun():
        db = makeDatabaseConnection()
        timeOut = str(languageConfig["blackJack"]["timeOut"])
        timeOutMsg = timeOut.replace("?@user", f" {user.display_name} ")
        await message.channel.send(timeOutMsg)
        await blackJackStay(self, db, message, casino, playerID, user, gamePlayerWaiting, removeWait=True)
        db.close()

    async def warningFun():
        warning = str(languageConfig["blackJack"]["warning"])
        warningMsg = warning.replace("?@user", f" {user.display_name} ")
        await message.channel.send(warningMsg)

    await gamePlayerWaiting.newWait(playerID, timeoutFun, warningFun)


async def blackJackHitWithPrivateMessage(self: Client, message: Message, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    player: Member = message.author
    table: BlackJackTable = casino.getTableByPlayerID(player.id)
    if table is None:
        notInGame = str(languageConfig["blackJack"]["notInGame"])
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
    hit = str(languageConfig["blackJack"]["hit"])
    await message.channel.send(hit)
    logger.info(f"Player {player.id} hit on black jack")

    async def timeoutFun():
        db = makeDatabaseConnection()
        timeOut = str(languageConfig["blackJack"]["timeOut1"])
        await message.channel.send(timeOut)
        await blackJackStayWithPrivateMsg(self, db, message, casino, gamePlayerWaiting, removeWait=False)
        db.close()

    async def warningFun():
        warning = str(languageConfig["blackJack"]["warning1"])
        await message.channel.send(warning)

    await gamePlayerWaiting.newWait(player.id, timeoutFun, warningFun)
