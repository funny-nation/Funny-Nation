import discord
from discord.ext import tasks
from loguru import logger
from discord import Message, User, RawReactionActionEvent, TextChannel
from pymysql import Connection

from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.controller.preRoute.registerAndAddMoneyWhenSendingMsg import registerAndAddMoneyWhenSendingMsg
from src.utils.checkIfMessagerIsBooster import checkIfMessagerIsBooster
from src.utils.addMoneyToUsersInVoiceChannels import addMoneyToUserInVoiceChannels
from src.controller.publicMsgRouter import publicMsgRouter
from src.controller.privateMsgRouter import privateMsgRouter
from src.controller.msgReactionRouter import msgReactionRouter
from src.controller.msgReactionDeleteRouter import msgReactionDeleteRouter
from src.utils.printMemoryStatus.main import PrintMemoryLogThread
from src.Storage import Storage

class Robot(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.storage: Storage = Storage()
        self.runPerSecond.start()

    async def on_ready(self):
        logger.info('Logged in as ' + self.user.name)
        await self.storage.initialize(self)

        addMoneyToUserInVoiceChannels(self)
        printMemoryLog = PrintMemoryLogThread(self.storage.casino, self.storage.gamePlayerWaiting)
        printMemoryLog.start()

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        db: Connection = makeDatabaseConnection()

        if message.channel != message.author.dm_channel:
            logger.info(f"{message.author.name} : {message.content}")
            # Pre-route
            isBooster: bool = checkIfMessagerIsBooster(self.storage.boostedRole, message.author)
            registerAndAddMoneyWhenSendingMsg(message.author.id, isBooster, db)

            await publicMsgRouter(self, message, db, self.storage)
        else:
            await privateMsgRouter(self, message, db, self.storage)
        db.close()

    async def on_raw_reaction_add(self, event: RawReactionActionEvent):
        if event.user_id != self.user.id:
            db: Connection = makeDatabaseConnection()
            await msgReactionRouter(self, event, db, self.storage)
            db.close()

    async def on_raw_reaction_remove(self, event: RawReactionActionEvent):
        user: User = await self.fetch_user(event.user_id)
        channel: TextChannel = await self.fetch_channel(event.channel_id)
        if user != self.user:
            db: Connection = makeDatabaseConnection()
            await msgReactionDeleteRouter(self, channel, user, self.storage, db, event)
            db.close()

    @tasks.loop(seconds=1)
    async def runPerSecond(self):
        await self.storage.gamePlayerWaiting.countDown()



