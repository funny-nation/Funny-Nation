from discord import User, DMChannel, Client, Message, Member, Guild
from src.utils.poker.pokerImage import getPokerImage
from src.utils.casino.table.BlackJackTable import BlackJackTable
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.onMessage.blackJack.stay import blackJackStay
from src.utils.casino.Casino import Casino
from loguru import logger
from pymysql import Connection
from src.model.makeDatabaseConnection import makeDatabaseConnection
import configparser

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read("Cconfig.ini")

async def blackJackGameStart(table: BlackJackTable, message: Message, self: Client, gamePlayerWaiting: GamePlayerWaiting, casino: Casino, db: Connection):
    table.gameStart()
    gameStart = str(languageConfig["blackJack"]["gameStart"])
    await message.channel.send(gameStart)
    playerListStr = ""
    myGuild: Guild = self.guilds[0]
    for userID in table.players:
        playerListStr += str(userID) + ", "
        member: Member = await myGuild.fetch_member(userID)
        dmChannel: DMChannel = await member.create_dm()
        ownCard = str(languageConfig["blackJack"]["ownCard"])
        await dmChannel.send(ownCard)
        cards = table.viewCards(userID)
        await dmChannel.send(file=getPokerImage(cards))
        needCard = str(languageConfig["blackJack"]["needCard"])
        needCard1 = str(languageConfig["blackJack"]["needCard1"])
        needCard2 = str(languageConfig["blackJack"]["needCard2"])
        needCard3 = str(languageConfig["blackJack"]["needCard3"])
        await dmChannel.send(needCard+"\n"+needCard1+"\n"+needCard2+"\n"+needCard3+"\n")
        await creategamePlayerWaiting(member, message, self, casino, gamePlayerWaiting, db)
    logger.info(f"Black Jack started in table {table.inviteMessage.channel.id} with players: {playerListStr}")


async def creategamePlayerWaiting(member: Member, message: Message, self: Client, casino: Casino, gamePlayerWaiting: GamePlayerWaiting, db: Connection):

    async def timeoutFun():
        dbTemp = makeDatabaseConnection()
        timeOut = str(languageConfig["blackJack"]["timeOut"])
        timeOut = timeOut.replace("?@user", f" {member.display_name} ")
        await message.channel.send(timeOut)
        await blackJackStay(self, dbTemp, message, casino, member.id, member, gamePlayerWaiting, removeWait=False)
        dbTemp.close()

    async def warningFun():
        warning = str(languageConfig["blackJack"]["warning"])
        warning = warning.replace("?@user", f" {member.display_name} ")
        await message.channel.send(warning)

    await gamePlayerWaiting.newWait(member.id, timeoutFun, warningFun)