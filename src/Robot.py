import discord
from loguru import logger
from .model.makeDatabaseConnection import makeDatabaseConnection
from .controller.whenSomeoneSendMessage import whenSomeoneSendMessage
from .controller.checkIfMessagerIsBooster import checkIfMessagerIsBooster
from .controller.addMoneyToUsersInVoiceChannels import addMoneyToUserInVoiceChannels
from .controller.messageAnalysis.messageParser import messageParser


class Robot(discord.Client):
    async def on_ready(self):
        # robot start
        logger.info('Logged in as ' + self.user.name)
        # designed for only this server, so the server should be at index 0
        myGuild = self.guilds[0]
        # list of boosters in server
        self.boostedRole = myGuild.premium_subscriber_role
        # a thread to increase money after checking user status
        addMoneyToUserInVoiceChannels(self)


    async def on_message(self, message):
        # ignore own message
        if message.author == self.user:
            return
        # print info in console
        logger.info(f"{message.author.name} : {message.content}")
        db = makeDatabaseConnection()
        isBooster = checkIfMessagerIsBooster(self, message.author)
        # analyze message
        whenSomeoneSendMessage(message.author.id, isBooster, db)
        await messageParser(self, message, db)
        db.close()

