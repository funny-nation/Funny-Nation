import discord
from discord.ext import tasks
from loguru import logger
from discord import Guild, Role, Message, Reaction, User, RawReactionActionEvent, TextChannel
from pymysql import Connection

from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.controller.whenSomeoneSendMessage import whenSomeoneSendMessage
from src.controller.checkIfMessagerIsBooster import checkIfMessagerIsBooster
from src.controller.addMoneyToUsersInVoiceChannels import addMoneyToUserInVoiceChannels
from src.controller.onMessage.onPublicMessage import onPublicMessage
from src.controller.onMessage.onPrivateMessage import onPrivateMessage
from src.utils.casino.Casino import Casino
from src.controller.onMessage.onMessageReaction import onMessageReaction
from src.controller.onMessage.onMessageReactionDelete import onMessageReactionDelete
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting


class Robot(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.boostedRole = None
        self.casino: Casino = Casino()
        self.gamePlayerWaiting = GamePlayerWaiting()
        self.runPerSecond.start()

    async def on_ready(self):
        logger.info('Logged in as ' + self.user.name)
        myGuild: Guild = self.guilds[0]
        self.boostedRole: Role = myGuild.premium_subscriber_role
        addMoneyToUserInVoiceChannels(self)

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        db: Connection = makeDatabaseConnection()
        logger.info(f"{message.author.name} : {message.content}")
        if message.channel != message.author.dm_channel:
            isBooster: bool = checkIfMessagerIsBooster(self.boostedRole, message.author)
            whenSomeoneSendMessage(message.author.id, isBooster, db)
            await onPublicMessage(self, message, db, self.casino, self.gamePlayerWaiting)
        else:
            await onPrivateMessage(self, message, db, self.casino, self.gamePlayerWaiting)
        db.close()

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
            await onMessageReactionDelete(self, channel, user, self.casino, db)
            db.close()

    @tasks.loop(seconds=1)
    async def runPerSecond(self):
        await self.gamePlayerWaiting.countDown()


