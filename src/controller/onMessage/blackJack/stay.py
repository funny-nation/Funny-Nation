from typing import Dict
from loguru import logger
from pymysql import Connection

from src.utils.casino.table.BlackJackTable import BlackJackTable

from src.utils.casino.Casino import Casino
from src.utils.casino.table.Table import Table
from discord import Client, Message, Member, TextChannel, Invite
from src.controller.onMessage.blackJack.endGame import blackJackEndGame
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting


async def blackJackStayWithPrivateMsg(self: Client, db: Connection, message: Message, casino: Casino, gamePlayerWaiting: GamePlayerWaiting, removeWait=True):
    tables: Dict[int, Table] = casino.tables
    playerID = message.author.id
    tableInviteMsg = None
    for tableID in tables:
        if tables[tableID].hasPlayer(playerID):
            tableInviteMsg = tables[tableID].inviteMessage
            break
    if tableInviteMsg is None:
        await message.channel.send("你说啥呢")
        return
    member = message.author
    table: BlackJackTable = casino.getTable(tableInviteMsg.channel.id)
    if table.gameOver:
        return
    table.stay(playerID)
    tableChannel: TextChannel = tableInviteMsg.channel
    await tableChannel.send(f"玩家{member.display_name}可以开牌了")
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
        await message.channel.send("这里没人开游戏")
        return
    if not table.hasPlayer(playerID):
        await message.channel.send("你不在这场牌局里")
        return
    if table.gameOver:
        return
    table.stay(playerID)
    logger.info(f"Player {playerID} stay in Black Jack")
    await message.channel.send(f"玩家{user.display_name}可以开牌了")
    if removeWait:
        await gamePlayerWaiting.removeWait(playerID)
    if table.isOver():
        await blackJackEndGame(self, table, message, casino, db)

