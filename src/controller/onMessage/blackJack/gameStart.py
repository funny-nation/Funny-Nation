from discord import User, DMChannel, Client, Message
from util.poker.pokerImage import getPokerImage
from util.casino.table.BlackJackTable import BlackJackTable

from loguru import logger


async def blackJackGameStart(table: BlackJackTable, message: Message, self: Client):
    table.gameStart()
    await message.channel.send("开始了，底牌已经私聊你们了，请各位查看自己的牌")
    playerListStr = ""
    for userID in table.players:
        playerListStr += str(userID) + ", "
        user: User = await self.fetch_user(userID)
        dmChannel: DMChannel = await user.create_dm()
        await dmChannel.send("这是你的牌：")
        cards = table.viewCards(userID)
        await dmChannel.send(file=getPokerImage(cards))
        await dmChannel.send("你还要牌吗，要的话，在这里回复\"要\"或者\"不要\"")

    logger.info(f"Black Jack started in table {table.inviteMessage.channel.id} with players: {playerListStr}")