from discord import User, DMChannel, Client, Message, Member, Guild
from src.utils.poker.pokerImage import getPokerImage
from src.utils.casino.table.BlackJackTable import BlackJackTable
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.onMessage.blackJack.stay import blackJackStay
from src.utils.casino.Casino import Casino
from loguru import logger


async def blackJackGameStart(table: BlackJackTable, message: Message, self: Client, gamePlayerWaiting: GamePlayerWaiting, casino: Casino):
    table.gameStart()
    await message.channel.send("开始了，底牌已经私聊你们了，请各位查看自己的牌")
    playerListStr = ""
    myGuild: Guild = self.guilds[0]
    for userID in table.players:
        playerListStr += str(userID) + ", "
        member: Member = await myGuild.fetch_member(userID)
        dmChannel: DMChannel = await member.create_dm()
        await dmChannel.send("这是你的牌：")
        cards = table.viewCards(userID)
        await dmChannel.send(file=getPokerImage(cards))
        await dmChannel.send("你还要牌吗，要的话，在这里回复\"要\"或者\"不要\"")
        await creategamePlayerWaiting(member, message, self, casino, gamePlayerWaiting)
    logger.info(f"Black Jack started in table {table.inviteMessage.channel.id} with players: {playerListStr}")


async def creategamePlayerWaiting(member: Member, message: Message, self: Client, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):

    async def timeoutFun():
        await message.channel.send(f"玩家{member.display_name}由于长时间没反应，自动开牌")
        await blackJackStay(self, message, casino, member.id, member, gamePlayerWaiting, removeWait=False)

    async def warningFun():
        await message.channel.send(f"玩家{member.display_name}由于长时间没反应，将会在5秒后自动开牌")

    await gamePlayerWaiting.newWait(member.id, timeoutFun, warningFun)