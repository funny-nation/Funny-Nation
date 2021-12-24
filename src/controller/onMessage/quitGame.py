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
config.read("Cconfig.ini")


async def quitGame(self: Client, message: Message, db: Connection, casino: Casino):
    table: Table = casino.getTable(message.channel.id)
    playerID = message.author.id
    if table is None:
        nobodyInGame = str(languageConfig['game']["nobodyInGame"])
        await message.channel.send(nobodyInGame)
        return
    if not table.hasPlayer(playerID):
        notInGame = str(languageConfig['game']["notInGame"])
        await message.channel.send(notInGame)
        return

    if table.gameStarted:
        wannaQuitInGame = str(languageConfig['game']["wannaQuitInGame"])
        await message.channel.send(wannaQuitInGame)
        return

    if table.owner == message.author:
        youAreOwner = str(languageConfig['game']["youAreOwner"])
        await message.channel.send(youAreOwner)
        return

    casino.onlinePlayer.remove(playerID)

    if table.game == 'blackJack':
        await quitBlackJack(table, message.author, message.channel, self, db)

    if table.game == 'holdem':
        await quiteHoldemGame(table, message.author, message.channel, self, db)


async def quitGameByReaction(table: Table, user: User, channel: TextChannel, self: Client, db: Connection, casino: Casino):
    if table.gameStarted:
        wannaQuitInGame1 = str(languageConfig['game']["wannaQuitInGame1"])
        quitMsg = wannaQuitInGame1.replace("?@user", f" @{user.display_name} ")
        await channel.send(quitMsg)
        return

    if not table.hasPlayer(user.id):
        notInGame1 = str(languageConfig['game']["notInGame1"])
        quitMsg = notInGame1.replace("?@user", f" @{user.display_name} ")
        await channel.send(quitMsg)
        return

    if table.owner == user:
        youAreOwner1 = str(languageConfig['game']["youAreOwner1"])
        quitMsg = youAreOwner1.replace("?@user", f" @{user.display_name} ")
        await channel.send(quitMsg)
        return

    casino.onlinePlayer.remove(user.id)
    if table.game == 'blackJack':
        await quitBlackJack(table, user, channel, self, db)

    if table.game == 'holdem':
        await quiteHoldemGame(table, user, channel, self, db)
