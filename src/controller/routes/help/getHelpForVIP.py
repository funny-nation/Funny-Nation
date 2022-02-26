from discord import Client, Message
from src.utils.readConfig import getLanguageConfig
import embedLib.help.getHelp4 as help
languageConfig = getLanguageConfig()

async def getHelpForVIP(self: Client, message: Message):
    embed = help.getEmbed()
    await message.channel.send(embed=embed)