from discord import Client, Reaction, User, TextChannel
from typing import Dict
from pymysql import Connection

from src.utils.casino.Casino import Casino
from src.utils.casino.table.Table import Table
from src.utils.casino.table.BlackJackTable import BlackJackTable
from src.controller.onMessage.quitGame import quitGameByReaction


async def onMessageReactionDelete(self: Client, channel: TextChannel, user: User, casino: Casino, db: Connection):

    # For game
    tables: Dict[int, Table] = casino.tables
    if channel.id in tables:
        await quitGameByReaction(tables[channel.id], user, channel, self, db, casino)
