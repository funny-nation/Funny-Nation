from discord import Embed


def getEmbed() -> Embed:
    embed = Embed()
    embed.title = "6 - 德州扑克游戏玩法介绍" \
                  "\n（游戏规则大家可以自行谷歌哦）"
    embed.description = "1. 创建游戏：在游戏频道（#vegas赌场）发送“ghs 开局德州扑克，默认入场费10货币。" \
                        "\n2. 加入游戏： 任意用户只要账户上有足够金额，都可以加入游戏，加入游戏请点击✅图标，即可加入。" \
                        "\n3. 加注：ghs 加注 100（数额自定义）- 加注是在跟的基础上进行叠加" \
                        "\n4. 退出游戏： 在游戏未开始之前都可以退出当前赌桌，你只需要再点击一下✅图标就可以退出当前游戏了。" \
                        "\n5. 关闭游戏：ghs 掀桌"
    embed.colour = 0xff9900
    return embed