from discord import Embed

def getEmbed(field: str, prefix: str) -> Embed:
    embed = Embed()
    embed.title = "4 - 用户可以用货币购买服务器VIP"
    embed.description = f"指令：{prefix} 买vip （默认从V1开始买）"
    embed.add_field(name="服务器VIP福利如下：", value="1. 单独tag分类，VIP播报"
                                              "\n2. GHS活动策划参与/服务器福利"
                                              "\n3. 歌会额外票"
                                              "\n4. GHS活动特别福利"
                                              "\n5. 歌会贵宾席"
                                              "\n6. 别墅休息去使用权，别墅区小屋购买权"
                                              "\n7. 组队摇人@权限"
                                              "\n8. 永久个性化tag"
                                              "\n9. 服务器股东", inline=False)
    embed.add_field(name="VIP等级-所需金额-福利编号", value=f"{field}", inline=False)
    embed.colour = 0xff9900
    return embed