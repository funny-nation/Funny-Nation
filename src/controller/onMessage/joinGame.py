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
config.read("config.ini")


async def joinGame(self: Client, message: Message, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    table: Table = casino.getTable(message.channel.id)
    playerID = message.author.id
    if table is None:
        noGameHere = str(languageConfig['game']["noGameHere"])\
            .replace("?@user", f"{message.author.display_name}")
        await message.channel.send(noGameHere)
        return
    if table.hasPlayer(playerID):
        youHaveAlreadyJoin = str(languageConfig['game']["youHaveAlreadyJoin"])\
            .replace("?@user", f"{message.author.display_name}")
        await message.channel.send(youHaveAlreadyJoin)
        return
    if table.getPlayerCount() >= table.maxPlayer:
        fullMSG = str(languageConfig['game']["full"]).replace("?@user", f"{message.author.display_name}")
        await message.channel.send(fullMSG)
        return
    if table.gameStarted:
        gameHasAlreadyStarted = str(languageConfig['game']["gameHasAlreadyStarted"])\
            .replace("?@user", f"{message.author.display_name}")
        await message.channel.send(gameHasAlreadyStarted)
        return

    if table.game == 'blackJack':
        await joinBlackJack(table, message.author, message.channel, self, db, casino, gamePlayerWaiting)

    if table.game == 'holdem':
        await joinHoldemGame(table, message.author, message.channel, self, db, casino, gamePlayerWaiting)


async def joinGameByReaction(table: Table, user: Member, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    if table.hasPlayer(user.id):
        youHaveAlreadyJoin = str(languageConfig['game']["youHaveAlreadyJoin"])\
            .replace("?@user", f"{user.display_name}")
        await channel.send(youHaveAlreadyJoin)
        return
    if table.gameStarted:
        gameHasAlreadyStarted = str(languageConfig['game']["gameHasAlreadyStarted"])\
            .replace("?@user", f"{user.display_name}")
        await channel.send(gameHasAlreadyStarted)
        return
    if table.getPlayerCount() >= table.maxPlayer:
        gameIsFull = str(languageConfig['game']["gameIsFull"])\
            .replace("?@user", f"{user.display_name}")
        await channel.send(gameIsFull)
        return
    if table.game == 'blackJack':
        await joinBlackJack(table, user, channel, self, db, casino, gamePlayerWaiting)

    if table.game == 'holdem':
        await joinHoldemGame(table, user, channel, self, db, casino, gamePlayerWaiting)
