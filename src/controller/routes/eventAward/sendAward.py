import json

from discord import Client, TextChannel, Guild, Member, Message
from pymysql import Connection
import src.model.eventAwardManagement as eventAwardManagement
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.utils.readConfig import getLanguageConfig, getMajorConfig

async def sendAward(self: Client, message: Message, db: Connection, money: int, userID: int, eventAdmin: list, quantity: int):
    languageConfig = getLanguageConfig()
    author = message.author.id

    if author not in eventAdmin:
        await message.channel.send("失败")
        return

    database = True
    database = database and addMoneyToUser(db, userID, money)
    if not database:
        msg = languageConfig['error']['dbError']
        await message.channel.send(msg)
        return
    uuid = eventAwardManagement.newAward(db, author, message.id, money, quantity)

    if uuid == '':
        msg = languageConfig['error']['dbError']
        await message.channel.send(msg)
        return

    msg = languageConfig['eventAward']['awardPublish'].replace('?@user', author.display_name)
    await message.channel.send(msg)
    await message.add_reaction(':game_die:')

