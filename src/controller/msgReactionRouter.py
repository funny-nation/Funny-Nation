from discord import Client, Member, RawReactionActionEvent, Guild, TextChannel, PartialEmoji
from typing import Dict
from pymysql import Connection

from src.Storage import Storage
from src.controller.routes.holdem.allIn import holdemAllIn
from src.controller.routes.holdem.callAndCheck import holdemCallAndCheck
from src.controller.routes.holdem.fold import fold
from src.utils.casino.table.Table import Table
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.controller.routes.joinGame import joinGameByReaction
from src.controller.routes.luckyMoney.getLuckyMoney import getLuckyMoney
from src.controller.routes.eventAward.rejectionAward import rejectAward
from src.controller.routes.eventAward.applyForAward import applyForAward
from src.controller.routes.eventAward.approveAward import approveAward
from src.controller.routes.lottery.joinLottery import joinLottery
from src.controller.routes.lottery.openLotteryResult import openLotteryResult
from src.controller.routes.lottery.closeLottery import closeLottery

async def msgReactionRouter(self: Client, event: RawReactionActionEvent, db: Connection, storage: Storage):
    myGuild: Guild = self.guilds[0]
    channel: TextChannel or None = myGuild.get_channel(event.channel_id)
    emoji: PartialEmoji = event.emoji

    if channel is None:
        if emoji.name == '⭕':
            await approveAward(self, event, db, storage.adminRole)
            return

        if emoji.name == '🚫':
            await rejectAward(self, event, db, storage.adminRole)
            return

    # for eventAward
    if emoji.name == '🎲':
        await applyForAward(self, db, event)
        return


    if emoji.name == '💰':
        await getLuckyMoney(self, event.message_id, db, event.channel_id, event.user_id)
        return

    # lottery-related
    if emoji.name == '🎟️':
        await joinLottery(self, db, event.user_id, event.message_id, event.member, event.channel_id, emoji)
        return

    if emoji.name == '🟩':
        await openLotteryResult(self, db, event.user_id, event.message_id, event.member, event.channel_id, emoji)
        return

    if emoji.name == '🟥':
        await closeLottery(self, db, event.user_id, event.message_id, event.member, event.channel_id, emoji)
        return

    # For game
    tables: Dict[int, Table] = storage.casino.tables
    user: Member = event.member
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
