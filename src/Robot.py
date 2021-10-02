import discord
from loguru import logger


class Robot(discord.Client):
    async def on_ready(self):
        logger.info('Logged in as ' + self.user.name)
        for channel in self.get_all_channels():
            print(channel)

    async def on_message(self, message):
        logger.info(message.author.name + ' : ' + message.content)

