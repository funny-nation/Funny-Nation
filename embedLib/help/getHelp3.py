from discord import Embed


def getEmbed() -> Embed:
    embed = Embed()
    embed.title = "3 - 用户可以使用货币送礼物"
    embed.description = "礼物指令：ghs 送 礼物名称 @玩家昵称"
    embed.add_field(name="礼物名称/价格一览", value="爱心：52"
                                            "\n生日灯牌：100"
                                            "\n冲鸭：100"
                                            "\n荧光棒：100"
                                            "\n锁了：150"
                                            "\n爆笑：233"
                                            "\n比心：300"
                                            "\n花束：500"
                                            "\n皇冠：888"
                                            "\n钻石：1314"
                                            "\n元宝：2222"
                                            "\n巨轮：3600"
                                            "\n表白：5200"
                                            "\n劳斯莱斯：10000", inline=False)
    embed.colour = 0xff9900
    return embed