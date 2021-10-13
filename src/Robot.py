import discord
import random
from loguru import logger
from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.controller.whenSomeoneSendMessage import whenSomeoneSendMessage
from src.controller.checkIfMessagerIsBooster import checkIfMessagerIsBooster
from src.controller.addMoneyToUsersInVoiceChannels import addMoneyToUserInVoiceChannels
from src.controller.messageAnalysis.messageParser import messageParser


class Robot(discord.Client):

    async def on_ready(self):
        logger.info('Logged in as ' + self.user.name)
        myGuild = self.guilds[0]
        self.boostedRole = myGuild.premium_subscriber_role

        # self.casino = {
        #     123: {
        #         'game': 'blackJack',
        #         'money': 100,
        #         'alphaPlayer': {
        #             'id': 123123,
        #             'cards': None,
        #         },
        #         'betaPlayer': {
        #             'id': 123123123,
        #             'cards': None,
        #         }
        #     }
        #
        # }
        addMoneyToUserInVoiceChannels(self)


    async def on_message(self, message):
        if message.author == self.user:
            return
        logger.info(f"{message.author.name} : {message.content}")
        db = makeDatabaseConnection()
        isBooster = checkIfMessagerIsBooster(self, message.author)
        whenSomeoneSendMessage(message.author.id, isBooster, db)
        await messageParser(self, message, db)
        db.close()

