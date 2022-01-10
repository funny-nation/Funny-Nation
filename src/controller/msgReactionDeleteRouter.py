
from discord import Client, Reaction, User, TextChannel, RawReactionActionEvent, PartialEmoji
from typing import Dict
from pymysql import Connection

from src.Storage import Storage
from src.utils.casino.Casino import Casino
from src.utils.casino.table.Table import Table
from src.utils.casino.table.BlackJackTable import BlackJackTable
from src.controller.routes.quitGame import quitGameByReaction


async def msgReactionDeleteRouter(self: Client, channel: TextChannel, user: User, storage: Storage, db: Connection, event: RawReactionActionEvent):
    emoji: PartialEmoji = event.emoji
    if emoji.name == '✅':
        # For game
        tables: Dict[int, Table] = storage.casino.tables
        if channel.id in tables:
            await quitGameByReaction(tables[channel.id], user, channel, self, db, storage.casino)
