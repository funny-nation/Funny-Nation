from src.data.casino.table.BlackJackTable import BlackJackTable
from discord import User, DMChannel, File, Client, Message
from src.data.poker.pokerImage import getPokerImage


async def joinBlackJack(table: BlackJackTable, playerID: int, message: Message, self: Client):
    table.addPlayer(playerID)
    if not table.gameStart():
        await message.channel.send("炸了")
        return

    await message.channel.send("开始了，底牌已经私聊你们了，请各位查看自己的牌")

    for userID in table.players:
        user: User = await self.fetch_user(userID)
        dmChannel: DMChannel = await user.create_dm()
        await dmChannel.send("这是你的牌：")
        cards = table.viewCards(userID)
        await dmChannel.send(file=getPokerImage(cards))
        await dmChannel.send("你还要牌吗")