import discord
import random
from loguru import logger
from discord import Guild, Role, Message
from pymysql import Connection

from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.controller.whenSomeoneSendMessage import whenSomeoneSendMessage
from src.controller.checkIfMessagerIsBooster import checkIfMessagerIsBooster
from src.controller.addMoneyToUsersInVoiceChannels import addMoneyToUserInVoiceChannels
from src.controller.onMessage.onPublicMessage import onPublicMessage
from src.controller.onMessage.onPrivateMessage import onPrivateMessage
from src.data.casino.Casino import Casino


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
