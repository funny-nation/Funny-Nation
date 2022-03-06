from discord import Embed


def getEmbed(prefix: str) -> Embed:
    embed = Embed()
    embed.title = "7 - 发布抽奖"
    embed.add_field(name=f"指令：{prefix} 抽奖 奖品名称 抽奖券价格 奖品数量"
                         f"\n（例：{prefix} 抽奖 比心 100 1）", value="bot发布抽奖信息后"
                                                        "\n任意用户可点击“🎟️”购买抽奖券"
                                                        "\n发布者点击“🟩”开奖"
                                                        "\n发布者点击“🟥”关闭抽奖", inline=False)
    embed.colour = 0xff9900
    return embed
