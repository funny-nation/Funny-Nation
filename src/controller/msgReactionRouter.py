import json

from discord import Client, Reaction, Member, RawReactionActionEvent, Guild, TextChannel, PartialEmoji,message
from typing import Dict
from pymysql import Connection

from src.Storage import Storage
from src.controller.routes.holdem.allIn import holdemAllIn
from src.controller.routes.holdem.callAndCheck import holdemCallAndCheck
from src.controller.routes.holdem.fold import fold
from src.utils.casino.Casino import Casino
from src.utils.casino.table.Table import Table
from src.utils.casino.table.BlackJackTable import BlackJackTable
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.controller.routes.joinGame import joinGameByReaction
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.routes.luckyMoney.getLuckyMoney import getLuckyMoney
from src.controller.routes.eventAward.adminProof import adminProof
import src.model.eventAwardManagement as eventAwardManagement

async def msgReactionRouter(self: Client, event: RawReactionActionEvent, db: Connection, storage: Storage, Message: message):
    emoji: PartialEmoji = event.emoji
    involve = []

    if emoji.name == '💰':
        await getLuckyMoney(self, event.message_id, db, event.channel_id, event.user_id)
        return

    # For game
    tables: Dict[int, Table] = storage.casino.tables
    myGuild: Guild = self.guilds[0]
    user: Member = event.member
    channel: TextChannel = myGuild.get_channel(event.channel_id)
    msg = await channel.fetch_message(event.message_id)




    # For Finding game
    if emoji.name == '✅':
        for tableID in tables:
            if tables[tableID].isInviteMessage(msg):
                table: Table = tables[tableID]
                await joinGameByReaction(table, user, channel, self, db, storage.casino, storage.gamePlayerWaiting)
                return
        return

    # Holdem fold
    if emoji.name == '❌':
        tables: Dict[int, HoldemTable]
        for tableID in tables:
            if tables[tableID].whosTurn == user.id:
                await fold(tables[tableID], user, channel, self, db, storage.casino, storage.gamePlayerWaiting)
                return
        return

    # Holdem all in
    if emoji.name == '⬆':
        tables: Dict[int, HoldemTable]
        for tableID in tables:
            if tables[tableID].whosTurn == user.id:
                await holdemAllIn(tables[tableID], user, channel, self, db, storage.casino, storage.gamePlayerWaiting)
                return
        return

    # Holdem call and check
    if emoji.name == '➡':
        tables: Dict[int, HoldemTable]
        for tableID in tables:
            if tables[tableID].whosTurn == user.id:
                await holdemCallAndCheck(tables[tableID], user, channel, self, db, storage.casino, storage.gamePlayerWaiting)
                return
        return

    # for eventAward
    if emoji.name == 'alal':
        AwardInfo = eventAwardManagement.getEventAward(db, event.message_id)
        involve = json.load(AwardInfo[4])
        await adminProof(self, Message, event.message_id, db, event.channel_id, event.user_id, involve)
        return
