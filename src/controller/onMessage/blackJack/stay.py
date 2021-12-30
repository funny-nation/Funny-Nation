from typing import Dict
from loguru import logger
from pymysql import Connection

from src.utils.casino.table.BlackJackTable import BlackJackTable

from src.utils.casino.Casino import Casino
from src.utils.casino.table.Table import Table
from discord import Client, Message, Member, TextChannel, Invite
from src.controller.onMessage.blackJack.endGame import blackJackEndGame
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
import configparser

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


async def blackJackStayWithPrivateMsg(self: Client, db: Connection, message: Message, casino: Casino, gamePlayerWaiting: GamePlayerWaiting, removeWait=True):
    tables: Dict[int, Table] = casino.tables
    playerID = message.author.id
    tableInviteMsg = None
    for tableID in tables:
        if tables[tableID].hasPlayer(playerID):
            tableInviteMsg = tables[tableID].inviteMessage
            break
    if tableInviteMsg is None:
        notInGame = str(languageConfig["blackJack"]["notInGame"])
        await message.channel.send(notInGame)
        return
    member = message.author
    table: BlackJackTable = casino.getTable(tableInviteMsg.channel.id)
    if table.gameOver:
        return
    table.stay(playerID)
    tableChannel: TextChannel = tableInviteMsg.channel
    playerCouldShowTheCard = str(languageConfig["blackJack"]["playerCouldShowTheCard"])\
        .replace("?@user", f" {member.display_name} ")
    await tableChannel.send(playerCouldShowTheCard)
    logger.info(f"Player {playerID} stay in Black Jack")
    invite: Invite = await tableChannel.create_invite(max_age=60)
    await message.channel.send(invite.url)
    if removeWait:
        await gamePlayerWaiting.removeWait(playerID)
    if table.isOver():
        await blackJackEndGame(self, table, tableInviteMsg, casino, db)


async def blackJackStay(self: Client, db: Connection, message: Message, casino: Casino, playerID: int, user: Member, gamePlayerWaiting: GamePlayerWaiting, removeWait=True):
    table: BlackJackTable = casino.getTable(message.channel.id)
    if table is None:
        noGameHere = str(languageConfig['game']["noGameHere"])\
            .replace("?@user", message.author.display_name)
        await message.channel.send(noGameHere)
        return
    if not table.hasPlayer(playerID):
        notInGame = str(languageConfig["game"]["notInGame"])\
            .replace("?@user", message.author.display_name)
        await message.channel.send(notInGame)
        return
    if table.gameOver:
        return
    table.stay(playerID)
    logger.info(f"Player {playerID} stay in Black Jack")
    playerCouldShowTheCard = str(languageConfig["blackJack"]["playerCouldShowTheCard"])\
        .replace("?@user", f" {user.display_name} ")
    await message.channel.send(playerCouldShowTheCard)
    if removeWait:
        await gamePlayerWaiting.removeWait(playerID)
    if table.isOver():
        await blackJackEndGame(self, table, message, casino, db)

