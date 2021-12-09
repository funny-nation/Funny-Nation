from discord import User, DMChannel, Client, Message, Member, Guild, Invite
from src.utils.poker.pokerImage import getPokerImage
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.onMessage.blackJack.stay import blackJackStay
from src.utils.casino.Casino import Casino
from loguru import logger
from pymysql import Connection
from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.controller.onMessage.holdem.sendPromptMsg import sendPromptMsg


async def holdemGameStart(table: HoldemTable, message: Message, self: Client, gamePlayerWaiting: GamePlayerWaiting, casino: Casino, db: Connection):
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
        await dmChannel.send("点击下面链接回到牌桌")
        invite: Invite = await message.channel.create_invite(max_age=60)
        await dmChannel.send(invite.url)
    await sendPromptMsg(message.channel, table.whosTurn)


    logger.info(f"Holdem started in table {table.inviteMessage.channel.id} with players: {playerListStr}")
