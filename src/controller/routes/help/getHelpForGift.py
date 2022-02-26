from discord import Client, Message
from src.utils.readConfig import getLanguageConfig
import embedLib.help.getHelp3 as help
languageConfig = getLanguageConfig()

async def getHelpForGift(self: Client, message: Message):
    embed = help.getEmbed()
    await message.channel.send(embed=embed)