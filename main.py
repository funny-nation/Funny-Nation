import discord
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == '庞林彬是一家之主吗':
            await message.channel.send('是')


client = MyClient()
client.run(config['private']['token'])

