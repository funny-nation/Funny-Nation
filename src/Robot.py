import discord
import random
from loguru import logger
from .model.makeDatabaseConnection import makeDatabaseConnection
from .controller.whenSomeoneSendMessage import whenSomeoneSendMessage
from .controller.checkIfMessagerIsBooster import checkIfMessagerIsBooster
from .controller.addMoneyToUsersInVoiceChannels import addMoneyToUserInVoiceChannels
from .controller.messageAnalysis.messageParser import messageParser


class Robot(discord.Client):

    def newCasinoTable(self, game, *, players=None, alphaPlayer=None, betaPlayer=None, money=None):
        id = random.randint(0, 99999)
        while self.casino.has_key(id):
            id = random.randint(0, 99999)
        if game == 'blackJack':
            self.casino[id] = {
                'game': 'blackJack',
                'money': money,
                'alphaPlayer': {
                    'id': alphaPlayer,
                    'cards': []
                },
                'betaPlayer': {
                    'id': betaPlayer,
                    'cards': []
                }
            }


    async def on_ready(self):
        logger.info('Logged in as ' + self.user.name)
        myGuild = self.guilds[0]
        self.boostedRole = myGuild.premium_subscriber_role
        self.casino = {}

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

