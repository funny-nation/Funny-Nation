from src.utils.casino.table.BlackJackTable import BlackJackTable
from discord import User, Client, TextChannel
from src.controller.onMessage.blackJack.gameStart import blackJackGameStart
from pymysql import Connection

from loguru import logger
from src.model.userManagement import getUser


async def quitBlackJack(table: BlackJackTable, player: User, channel: TextChannel, self: Client, db: Connection):
    userInfo: tuple = getUser(db, player.id)

    table.dropPlayer(player.id)
    logger.info(f"Player {player.id} quit the talbe")
    await channel.send(f"{player.display_name}退出了游戏")
