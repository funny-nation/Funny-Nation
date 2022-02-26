from discord import Embed


def getEmbed() -> Embed:
    embed = Embed()
    embed.title = "GHS霸道总裁使用手册" #大标题
    embed.description = "1 如何获取货币\n2 指令一览\n3 礼物打赏系统\n4 服务器VIP系统" \
                        "\n5 21点游戏\n6 德州扑克\n7 发布抽奖\n8 GHS小花园匿名墙```\n回复数字序号获取相关帮助\n例如：1```" #详情说明
    embed.colour = 0xff9900
    return embed