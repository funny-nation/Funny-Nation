from discord import TextChannel, Member, Message


async def sendPromptMsg(channel: TextChannel, whoID: int or None, currentPot: int, amountForCall: int = 0):
    if whoID is None:
        return
    currentPotMoneyDisplay = currentPot / 100
    if amountForCall != 0:
        moneyDisplay = amountForCall / 100
        msg = f"轮到你了 <@{whoID}> 你跟的话，需要{moneyDisplay}元，当前底池里有{currentPotMoneyDisplay}元。\n点击❌弃牌，点击➡跟牌，点击⬆全压，发送指令可以加注"
    else:
        msg = f"轮到你了 <@{whoID}>，当前底池里有{currentPotMoneyDisplay}元。\n点击❌弃牌，点击➡过牌，点击⬆全压，发送指令可以加注。"
    message: Message = await channel.send(msg)
    await message.add_reaction('❌')
    await message.add_reaction('➡')
    await message.add_reaction('⬆')
