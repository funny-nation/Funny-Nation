from discord import Client, TextChannel, Member
from pymysql import Connection

from src.controller.routes.holdem.endGame import holdemEndGame
from src.controller.routes.holdem.next.nextPlayer import holdemNextPlayer
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.runWhenBotStart.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.model.holdemRecordManagement import setHoldemRecordStatus
from loguru import logger


async def fold(table: HoldemTable, user: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    table.fold(user.id)
    await channel.send(f"玩家{user.display_name}弃牌")
    logger.info(f"Player {user.id} fold in holdem table {channel.id}")

    databaseResult = True
    databaseResult = databaseResult and setHoldemRecordStatus(db, user.id, table.uuid, 1)
    if not databaseResult:
        await channel.send(f"炸了，麻烦通知一下群主")
        logger.error("Database Error while set holdem game status")
        return

    if table.numberOfPlayersNotFold == 1:
        await holdemEndGame(table, channel, self, db, casino, gamePlayerWaiting, publicForCards=False)
        return

    await holdemNextPlayer(table, channel, self, db, casino, gamePlayerWaiting)

