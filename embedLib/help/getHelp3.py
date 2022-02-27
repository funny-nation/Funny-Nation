from discord import Embed
from src.utils.readConfig import getGiftConfig
from src.utils.readConfig import getGeneralConfig

def getEmbed(field: str) -> Embed:
    embed = Embed()
    generalConfig = getGeneralConfig()
    prefix = generalConfig['command']['prefix']
    embed.title = "3 - 用户可以使用货币送礼物"
    embed.description = f"礼物指令：{prefix} 送 礼物名称 @玩家昵称"
    embed.add_field(name="礼物名称/价格一览", value=f"{field}", inline=False)

    embed.colour = 0xff9900
    return embed