import discord
import random
from loguru import logger
from discord import Guild, Role, Message
from pymysql import Connection

from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.controller.whenSomeoneSendMessage import whenSomeoneSendMessage
from src.controller.checkIfMessagerIsBooster import checkIfMessagerIsBooster
from src.controller.addMoneyToUsersInVoiceChannels import addMoneyToUserInVoiceChannels
from src.controller.messageAnalysis.messageParser import messageParser
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
        # e = discord.Embed()
        # e.set_image(url='https://www.teenet.me/wp-content/uploads/2020/12/zcapt-1.png')
        # await message.channel.send(embed=e)
        db: Connection = makeDatabaseConnection()
        logger.info(f"{message.author.name} : {message.content}")
        if message.channel != message.author.dm_channel:
            isBooster: bool = checkIfMessagerIsBooster(self.boostedRole, message.author)
            whenSomeoneSendMessage(message.author.id, isBooster, db)
        await messageParser(self, message, db, self.casino)
        db.close()
