import discord
from discord.ext import tasks
from loguru import logger
from discord import Guild, Role, Message, User, RawReactionActionEvent, TextChannel
from pymysql import Connection
from typing import List

from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.controller.whenSomeoneSendMessage import whenSomeoneSendMessage
from src.controller.checkIfMessagerIsBooster import checkIfMessagerIsBooster
from src.controller.addMoneyToUsersInVoiceChannels import addMoneyToUserInVoiceChannels
from src.controller.onPublicMessage import onPublicMessage
from src.controller.onPrivateMessage import onPrivateMessage
from src.utils.casino.Casino import Casino
from src.controller.onMessage.onMessageReaction import onMessageReaction
from src.controller.onMessage.onMessageReactionDelete import onMessageReactionDelete
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.utils.printMemoryStatus.main import PrintMemoryLogThread
from src.utils.poker.pokerImage import getPokerImage
from src.utils.poker.Card import Card
from src.utils.poker.Poker import Poker
import src.utils.fetchChannel as fetchChannel
from src.utils.getVipRoles import getVipRoles
from src.checkPermissions import checkPermissions
from src.readAdminList import getAdmin

class Robot(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.boostedRole = None
        self.announcementChannel = None
        self.vipRoles = {}
        self.casino: Casino = Casino()
        self.gamePlayerWaiting = GamePlayerWaiting()
        self.runPerSecond.start()
        self.admin = []

    async def on_ready(self):
        logger.info('Logged in as ' + self.user.name)
        myGuild: Guild = self.guilds[0]
        self.boostedRole: Role = myGuild.premium_subscriber_role
        logger.info('Got boosted role')
        self.announcementChannel = fetchChannel.fetchAnnouncementChannel(myGuild)
        logger.info('found announcement channel')
        self.vipRoles = await getVipRoles(myGuild)
        logger.info('Located VIP roles')
        if not await checkPermissions(self):
            logger.error('Permission check failed')
            exit(1)
        logger.info("Permission checked")
        self.admin = await getAdmin(self)
        logger.info("admin list get")
        logger.info(self.admin)
        addMoneyToUserInVoiceChannels(self)
        printMemoryLog = PrintMemoryLogThread(self.casino, self.gamePlayerWaiting)
        printMemoryLog.start()

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        db: Connection = makeDatabaseConnection()
        logger.info(f"{message.author.name} : {message.content}")
        if message.channel != message.author.dm_channel:
            isBooster: bool = checkIfMessagerIsBooster(self.boostedRole, message.author)
            whenSomeoneSendMessage(message.author.id, isBooster, db)
            await onPublicMessage(self, message, db, self.casino, self.gamePlayerWaiting, self.announcementChannel, self.vipRoles, self.admin)
        else:
            await onPrivateMessage(self, message, db, self.casino, self.gamePlayerWaiting)
        db.close()
        # Test on poker image
        # await testOnPokerImage(message.channel)

    async def on_raw_reaction_add(self, event: RawReactionActionEvent):
        if event.user_id != self.user.id:
            db: Connection = makeDatabaseConnection()
            await onMessageReaction(self, event, self.casino, db, self.gamePlayerWaiting)
            db.close()

    async def on_raw_reaction_remove(self, event: RawReactionActionEvent):
        user: User = await self.fetch_user(event.user_id)
        channel: TextChannel = await self.fetch_channel(event.channel_id)
        if user != self.user:
            db: Connection = makeDatabaseConnection()
            await onMessageReactionDelete(self, channel, user, self.casino, db, event)
            db.close()

    @tasks.loop(seconds=1)
    async def runPerSecond(self):
        await self.gamePlayerWaiting.countDown()


async def testOnPokerImage(channel: TextChannel):
    poker = Poker()
    pokerList: List[Card] = poker.getAllCards()
    await channel.send(file=getPokerImage(pokerList))

