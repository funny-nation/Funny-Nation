from src.utils.casino.table.BlackJackTable import BlackJackTable
from discord import User, Client, TextChannel, Member
from src.controller.onMessage.blackJack.gameStart import blackJackGameStart
from pymysql import Connection

from loguru import logger
from src.model.userManagement import getUser
from src.utils.casino.Casino import Casino
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting


async def joinBlackJack(table: BlackJackTable, player: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    userInfo: tuple = getUser(db, player.id)
    if userInfo[1] < table.money:
        await channel.send(f"{player.display_name}，你好像不太够钱")
        return

    if not table.addPlayer(player.id):
        await channel.send("炸了")
        return
    if userInfo[0] in casino.onlinePlayer:
        await channel.send("你已经在另一个游戏里了")
        return
    casino.onlinePlayer.append(userInfo[0])
    await channel.send(f"{player.display_name}，加入")
    logger.info(f"{player.id} join a blackJack table {channel.id}")
    if table.getPlayerCount() >= table.maxPlayer:
        await blackJackGameStart(table, table.inviteMessage, self, gamePlayerWaiting, casino)
        logger.info(f"Table {channel.id} started automatically due to full")
