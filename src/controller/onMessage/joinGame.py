from discord import Client, Message, Reaction, TextChannel, User, Member
from pymysql import Connection

from src.controller.onMessage.holdem.joinGame import joinHoldemGame
from src.utils.casino.Casino import Casino
from src.utils.casino.table import Table
from src.controller.onMessage.blackJack.joinGame import joinBlackJack
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
import configparser

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read("Cconfig.ini")


async def joinGame(self: Client, message: Message, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    table: Table = casino.getTable(message.channel.id)
    playerID = message.author.id
    if table is None:
        nobodyInGame = str(languageConfig['game']["nobodyInGame"])
        await message.channel.send(nobodyInGame)
        return
    if table.hasPlayer(playerID):
        inGame = str(languageConfig['game']["inGame"])
        await message.channel.send(inGame)
        return
    if table.getPlayerCount() >= table.maxPlayer:
        full = str(languageConfig['game']["full"])
        fullMsg = full.replace("?@user", f" @{message.author.display_name} ")
        await message.channel.send(fullMsg)
        return
    if table.gameStarted:
        overTime1 = str(languageConfig['game']["overTime1"])
        overMsg = overTime1.replace("?@user", f" @{message.author.display_name} ")
        await message.channel.send(overMsg)
        return

    if table.game == 'blackJack':
        await joinBlackJack(table, message.author, message.channel, self, db, casino, gamePlayerWaiting)

    if table.game == 'holdem':
        await joinHoldemGame(table, message.author, message.channel, self, db, casino, gamePlayerWaiting)


async def joinGameByReaction(table: Table, user: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    if table.hasPlayer(user.id):
        inGame = str(languageConfig['game']["inGame"])
        inMsg = inGame.replace("?@user", f" @{user.display_name} ")
        await channel.send(inMsg)
        return
    if table.gameStarted:
        overTime1 = str(languageConfig['game']["overTime1"])
        overMsg = overTime1.replace("?@user", f" @{user.display_name} ")
        await channel.send(overMsg)
        return
    if table.getPlayerCount() >= table.maxPlayer:
        full = str(languageConfig['game']["full"])
        fullMsg = full.replace("?@user", f" @{user.display_name} ")
        await channel.send(fullMsg)
        return
    if table.game == 'blackJack':
        await joinBlackJack(table, user, channel, self, db, casino, gamePlayerWaiting)

    if table.game == 'holdem':
        await joinHoldemGame(table, user, channel, self, db, casino, gamePlayerWaiting)
