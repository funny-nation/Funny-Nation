import discord
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
from src.utils.gameWaiting.main import startPlayerWaitingThread


class Robot(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.boostedRole = None
        self.casino: Casino = Casino()

    async def on_ready(self):
        logger.info('Logged in as ' + self.user.name)
        myGuild: Guild = self.guilds[0]
        self.boostedRole: Role = myGuild.premium_subscriber_role
        addMoneyToUserInVoiceChannels(self)
        startPlayerWaitingThread()


    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        db: Connection = makeDatabaseConnection()
        logger.info(f"{message.author.name} : {message.content}")
        if message.channel != message.author.dm_channel:
            isBooster: bool = checkIfMessagerIsBooster(self.boostedRole, message.author)
            whenSomeoneSendMessage(message.author.id, isBooster, db)
            await onPublicMessage(self, message, db, self.casino)
        else:
            await onPrivateMessage(self, message, db, self.casino)
        db.close()

    async def on_reaction_add(self, reaction: Reaction, user: User):
        if user != self.user:
            db: Connection = makeDatabaseConnection()
            await onMessageReaction(self, reaction, user, self.casino, db)
            db.close()

    async def on_raw_reaction_remove(self, event: RawReactionActionEvent):
        user: User = await self.fetch_user(event.user_id)
        channel: TextChannel = await self.fetch_channel(event.channel_id)
        if user != self.user:
            db: Connection = makeDatabaseConnection()
            await onMessageReactionDelete(self, channel, user, self.casino, db)
            db.close()
