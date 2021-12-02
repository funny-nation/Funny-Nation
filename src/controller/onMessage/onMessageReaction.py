from discord import Client, Reaction, Member, RawReactionActionEvent, Guild, TextChannel, PartialEmoji
from typing import Dict
from pymysql import Connection

from src.controller.onMessage.holdem.fold import fold
from src.utils.casino.Casino import Casino
from src.utils.casino.table.Table import Table
from src.utils.casino.table.BlackJackTable import BlackJackTable
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.controller.onMessage.joinGame import joinGameByReaction
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting


async def onMessageReaction(self: Client, event: RawReactionActionEvent, casino: Casino, db: Connection, gamePlayerWaiting: GamePlayerWaiting):

    # For game
    tables: Dict[int, Table] = casino.tables
    myGuild: Guild = self.guilds[0]
    user: Member = event.member
    channel: TextChannel = myGuild.get_channel(event.channel_id)
    msg = await channel.fetch_message(event.message_id)
    emoji: PartialEmoji = event.emoji

    # For Finding game
    if emoji.name == '✅':
        for tableID in tables:
            if tables[tableID].isInviteMessage(msg):
                table: Table = tables[tableID]
                await joinGameByReaction(table, user, channel, self, db, casino, gamePlayerWaiting)
                return
        return

    if emoji.name == '❌':
        tables: Dict[int, HoldemTable]
        for tableID in tables:
            if tables[tableID].whosTurn.id == user.id:
                await fold(tables[tableID], user, channel, self, db, casino, gamePlayerWaiting)
                return
        return

    if emoji.name == '🔺':
        return

    if emoji.name == '➡':
        return
