from discord import Client, Message
from src.utils.casino.Casino import Casino
from src.utils.casino.table.BlackJackTable import BlackJackTable
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.controller.routes.blackJack.gameStart import blackJackGameStart
from src.controller.routes.holdem.gameStart import holdemGameStart
from src.runWhenBotStart.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from pymysql import Connection
from src.utils.readConfig import getLanguageConfig

languageConfig = getLanguageConfig()


async def gameStartByTableOwner(self: Client, message: Message, casino: Casino, gamePlayerWaiting: GamePlayerWaiting, db: Connection):
    table: BlackJackTable = casino.getTable(message.channel.id)
    if table is None:
        noGameHere = str(languageConfig['game']["noGameHere"])\
            .replace('?@user', message.author.display_name)
        await message.channel.send(noGameHere)
        return
    if table.getPlayerCount() == 1:
        playerNotEnough = str(languageConfig['game']["playerNotEnough"])\
            .replace('?@user', message.author.display_name)
        await message.channel.send(playerNotEnough)
        return
    if table.owner != message.author:
        notOwner = str(languageConfig['game']["notOwner"])\
            .replace('?@user', message.author.display_name)
        await message.channel.send(notOwner)
        return
    if table.gameStarted:
        gameStart = str(languageConfig['game']["gameHasAlreadyStartedForClosingGame"])\
            .replace('?@user', message.author.display_name)
        await message.channel.send(gameStart)
        return

    if table.game == 'blackJack':
        await blackJackGameStart(table, message, self, gamePlayerWaiting, casino, db)

    if table.game == 'holdem':
        table: HoldemTable
        await holdemGameStart(table, message, self, gamePlayerWaiting, casino, db)
