import discord
from loguru import logger
from .model.makeDatabaseConnection import makeDatabaseConnection
from .controller.whenSomeoneSendMessage import whenSomeoneSendMessage
from .controller.checkIfMessagerIsBooster import checkIfMessagerIsBooster
from .controller.addMoneyToUsersInVoiceChannels import addMoneyToUserInVoiceChannels
from .controller.messageAnalysis.messageParser import messageParser


class Robot(discord.Client):
    async def on_ready(self):
        logger.info('Logged in as ' + self.user.name)
        myGuild = self.guilds[0]
        self.boostedRole = myGuild.premium_subscriber_role
        addMoneyToUserInVoiceChannels(self)


    async def on_message(self, message):
        if message.author == self.user:
            return
        logger.info(f"{message.author.id} : {message.content}")
        db = makeDatabaseConnection()
        isBooster = checkIfMessagerIsBooster(self, message.author)
        whenSomeoneSendMessage(message.author.id, isBooster, db)
        await messageParser(self, message, db)
        db.close()

