from discord import Client, Message
from src.utils.readConfig import getLanguageConfig
from src.utils.readConfig import getGiftConfig
import embedLib.help.getHelp3 as help
languageConfig = getLanguageConfig()
giftConfig = getGiftConfig()

async def getHelpForGift(self: Client, message: Message):
    sections: str = giftConfig.sections()
    description: str = ""

    for i in range(0, len(giftConfig.sections())):
        giftName: str = sections[i]
        giftMoney = giftConfig[giftName]['amount']
        description += f"{giftName}: {giftMoney}元\n"
    embed = help.getEmbed(description)
    await message.channel.send(embed=embed)