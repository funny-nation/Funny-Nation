from discord import Client, Reaction, User
from typing import Dict
from pymysql import Connection

from util.casino.Casino import Casino
from util.casino.table.Table import Table
from util.casino.table.BlackJackTable import BlackJackTable
from src.controller.onMessage.joinGame import joinGameByReaction


async def onMessageReaction(self: Client, reaction: Reaction, user: User, casino: Casino, db: Connection):

    # For game
    tables: Dict[int, Table] = casino.tables
    for tableID in tables:
        if tables[tableID].isInviteMessage(reaction.message):
            table: Table = tables[tableID]
            gameType: str = table.game
            if gameType == 'blackJack':
                table: BlackJackTable
                await joinGameByReaction(table, user, reaction, self, db)
                break

