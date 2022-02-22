from discord import DMChannel, Client, Message, Member, Guild
from src.utils.poker.pokerImage import getPokerImage
from src.utils.casino.table.BlackJackTable import BlackJackTable
from src.runWhenBotStart.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.controller.routes.blackJack.stay import blackJackStay
from src.utils.casino.Casino import Casino
from loguru import logger
from pymysql import Connection
from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.utils.readConfig import getLanguageConfig

languageConfig = getLanguageConfig()


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
        thisIsyourCards = str(languageConfig["blackJack"]["thisIsyourCards"])
        await dmChannel.send(thisIsyourCards)
        cards = table.viewCards(userID)
        await dmChannel.send(file=getPokerImage(cards))
        needCard = str(languageConfig["blackJack"]["needCard"])
        await dmChannel.send(needCard)
        await creategamePlayerWaiting(member, message, self, casino, gamePlayerWaiting, db)
    logger.info(f"Black Jack started in table {table.inviteMessage.channel.id} with players: {playerListStr}")


async def creategamePlayerWaiting(member: Member, message: Message, self: Client, casino: Casino, gamePlayerWaiting: GamePlayerWaiting, db: Connection):

    async def timeoutFun():
        dbTemp = makeDatabaseConnection()
        await blackJackStay(self, dbTemp, message, casino, member.id, member, gamePlayerWaiting, removeWait=False)
        dbTemp.close()

    async def warningFun():
        warning = str(languageConfig["blackJack"]["timeOutWarning"])\
            .replace("?@user", f" {member.display_name} ")
        await message.channel.send(warning)

    await gamePlayerWaiting.newWait(member.id, timeoutFun, warningFun)
