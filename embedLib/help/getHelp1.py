from discord import Embed


def getEmbed() -> Embed:
    embed = Embed()
    embed.title = "1 - 如何获取货币" #大标题
    embed.description = "1. 在服务器内发送文字消息" \
                        "\n2. 在服务器内语音语音聊天（闭麦不会获得货币，AKF频道内无法获得货币）" \
                        "\n3. 在服务器内直播（闭麦不会获得货币，AKF频道内无法获得货币）" \
                        "\n4. 参加GHS活动赢取活动奖金，详情可以关注活动公告" \
                        "\n5. 邀请玩家加入服务器，每新增5人获得100货币，玩家凭邀请链接在管理处领取奖金" \
                        "\n6. 赞助服务器活动，获取人民币1:10服务器货币" \
                        "\n7. 抢红包，21点游戏，德州扑克游戏等等"    # 详情说明
    embed.colour = 0xff9900
    return embed