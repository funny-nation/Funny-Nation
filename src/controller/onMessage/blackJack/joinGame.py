from src.data.casino.table.BlackJackTable import BlackJackTable
from discord import User, DMChannel, File, Client, Message, TextChannel
from src.controller.onMessage.blackJack.gameStart import blackJackGameStart
from pymysql import Connection

from loguru import logger
from src.model.userManagement import getUser


async def joinBlackJack(table: BlackJackTable, player: User, channel: TextChannel, self: Client, db: Connection):
    userInfo: tuple = getUser(db, player.id)
    if userInfo[1] < table.money:
        await channel.send(f"{player.display_name}，你好像不太够钱")
        return
    if table.gameStarted:
        await channel.send(f"{player.display_name}，游戏已经开始了，等下一局吧")
        return

    if not table.addPlayer(player.id):
        await channel.send("炸了")
        return

    await channel.send(f"{player.display_name}，加入")
    logger.info(f"{player.id} join a blackJack table {channel.id}")
    if table.getPlayerCount() >= table.maxPlayer:
        await blackJackGameStart(table, table.inviteMessage, self)
        logger.info(f"Table {channel.id} started automatically due to full")
