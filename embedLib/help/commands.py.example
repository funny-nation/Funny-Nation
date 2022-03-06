from discord import Embed

def getEmbed(prefix: str) -> Embed:
    embed = Embed()
    embed.title = "2 - 指令一览"
    embed.description = "用户可在服务器内发送指令使用bot"
    embed.add_field(name=f"{prefix} 帮助", value="获取bot使用说明", inline=False)
    embed.add_field(name=f"{prefix} 余额", value="查看服务期内自己的账户余额", inline=False)
    embed.add_field(name=f"{prefix} 富豪榜", value="查看服务器内排名前十的用户和金额", inline=False)
    embed.add_field(name=f"{prefix} 转账 金额 @收款人", value="转账给被@的用户，数额可以自定义"
                                                 f"\n（例：{prefix} 转账 100 @昵称）", inline=False)
    embed.add_field(name=f"{prefix} 账单", value="查看近期10条流水记录", inline=False)
    embed.add_field(name=f"{prefix} 账单 X", value="查看XX近期10条流水记录"
                                           f"\n（例：{prefix} 账单 直播收益）"
                                           "\n可查看的流水内容：转账，消息收益，每日签到收益，直播收益，语音在线收益，领奖", inline=False)
    embed.add_field(name=f"{prefix} 买vip", value="购买服务器vip服务，默认从vip1开始购买", inline=False)
    embed.add_field(name=f"{prefix} 送 礼物 @收礼人", value="送出小礼物给收礼人，送礼信息会在相关频道播报"
                                                f"\n（例：{prefix} 送 爱心 @昵称）", inline=False)
    embed.add_field(name=f"{prefix}开局21点 金额", value="在文字频道内开始一局21点游戏，入池金额可以自定义"
                                               f"\n（例：{prefix} 开局 21点 10）", inline=False)
    embed.add_field(name=f"{prefix} 开局德州扑克", value="在文字频道内开始一局德州扑克游戏", inline=False)
    embed.add_field(name=f"{prefix} 加注 金额", value="在德州扑克游戏中，到玩家轮次，玩家可以加注"
                                            f"\n（例：{prefix} 加注 100）", inline=False)
    embed.add_field(name=f"{prefix} 掀桌", value="游戏发起者关闭游戏（21点游戏和德州扑克游戏通用）", inline=False)
    embed.add_field(name=f"{prefix} 发红包 总金额 红包数量", value="在文字频道内发红包，金额和数量不能是0"
                                                   f"\n（例：{prefix} 发红包 100 10）", inline=False)
    embed.add_field(name=f"{prefix} 抽奖 奖品名称 抽奖券价格 奖品数量", value="频道内用户可以发起抽奖活动"
                                                         f"\n（例：{prefix} 抽奖 比心 100 1）", inline=False)
    embed.colour = 0xff9900
    return embed