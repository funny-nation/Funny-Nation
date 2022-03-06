
from discord import Client, Message, Guild, Member
from src.utils.readConfig import getLanguageConfig
import embedLib.help.getHelp as help
languageConfig = getLanguageConfig()

async def getHelp(self: Client, message: Message):
    embed = help.getEmbed()
    await message.channel.send(embed=embed)
