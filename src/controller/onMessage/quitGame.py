from discord import Client, Message, Reaction, TextChannel, User
from pymysql import Connection
from src.utils.casino.Casino import Casino
from src.utils.casino.table import Table
from src.controller.onMessage.blackJack.quitGame import quitBlackJack
from src.controller.onMessage.holdem.quitGame import quiteHoldemGame
import configparser

languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read("config.ini")


async def quitGame(self: Client, message: Message, db: Connection, casino: Casino):
    table: Table = casino.getTable(message.channel.id)
    playerID = message.author.id
    if table is None:
        noGameHere = str(languageConfig['game']["noGameHere"])\
            .replace('?@user', message.author.display_name)
        await message.channel.send(noGameHere)
        return
    if not table.hasPlayer(playerID):
        notInGame = str(languageConfig['game']["notInGame"])\
            .replace('?@user', message.author.display_name)
        await message.channel.send(notInGame)
        return

    if table.gameStarted:
        noChanceToQuit = str(languageConfig['game']["noChanceToQuit"])\
            .replace('?@user', message.author.display_name)
        await message.channel.send(noChanceToQuit)
        return

    if table.owner == message.author:
        youAreOwner = str(languageConfig['game']["youAreOwner"])\
            .replace('?@user', message.author.display_name)
        await message.channel.send(youAreOwner)
        return

    casino.onlinePlayer.remove(playerID)

    if table.game == 'blackJack':
        await quitBlackJack(table, message.author, message.channel, self, db)

    if table.game == 'holdem':
        await quiteHoldemGame(table, message.author, message.channel, self, db)


async def quitGameByReaction(table: Table, user: User, channel: TextChannel, self: Client, db: Connection, casino: Casino):
    if table.gameStarted:
        noChanceToQuit = str(languageConfig['game']["noChanceToQuit"])\
            .replace("?@user", user.display_name)
        await channel.send(noChanceToQuit)
        return

    if not table.hasPlayer(user.id):
        notInGame = str(languageConfig['game']["youAreOwner"])\
            .replace("?@user", user.display_name)
        await channel.send(notInGame)
        return

    if table.owner == user:
        youAreOwner = str(languageConfig['game']["youAreOwner"])\
            .replace("?@user", user.display_name)
        await channel.send(youAreOwner)
        return

    casino.onlinePlayer.remove(user.id)
    if table.game == 'blackJack':
        await quitBlackJack(table, user, channel, self, db)

    if table.game == 'holdem':
        await quiteHoldemGame(table, user, channel, self, db)
