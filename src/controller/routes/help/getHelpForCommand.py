from discord import Client, Message
from src.utils.readConfig import getLanguageConfig
import embedLib.help.getHelp2 as help
languageConfig = getLanguageConfig()

async def getHelpForCommand(self: Client, message: Message):
    embed = help.getEmbed()
    await message.channel.send(embed=embed)