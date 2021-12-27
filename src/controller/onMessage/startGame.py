from discord import Client, Message
from src.utils.casino.Casino import Casino
from src.utils.casino.table.BlackJackTable import BlackJackTable
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.controller.onMessage.blackJack.gameStart import blackJackGameStart
from src.controller.onMessage.holdem.gameStart import holdemGameStart
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from pymysql import Connection
import configparser

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read("Cconfig.ini")


async def gameStartByTableOwner(self: Client, message: Message, casino: Casino, gamePlayerWaiting: GamePlayerWaiting, db: Connection):
    table: BlackJackTable = casino.getTable(message.channel.id)
    if table is None:
        nobodyInGame = str(languageConfig['game']["nobodyInGame"])
        await message.channel.send(nobodyInGame)
        return
    if table.getPlayerCount() == 1:
        userNotEnough = str(languageConfig['game']["userNotEnough"])
        await message.channel.send(userNotEnough)
        return
    if table.owner != message.author:
        notOwner = str(languageConfig['game']["notOwner"])
        await message.channel.send(notOwner)
        return
    if table.gameStarted:
        gameStart = str(languageConfig['game']["gameStart"])
        await message.channel.send(gameStart)
        return

    if table.game == 'blackJack':
        await blackJackGameStart(table, message, self, gamePlayerWaiting, casino, db)

    if table.game == 'holdem':
        table: HoldemTable
        await holdemGameStart(table, message, self, gamePlayerWaiting, casino, db)
