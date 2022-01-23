import json
from typing import List


from discord import Client, TextChannel, Guild, Member, Message, Role
from pymysql import Connection
import src.model.eventAwardManagement as eventAwardManagement
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.utils.readConfig import getLanguageConfig, getMajorConfig
import re

async def sendAward(self: Client, message: Message, db: Connection, money: int, userID: int, eventAdmin: list, command: str):
    languageConfig = getLanguageConfig()
    author = message.author.id
    eventName: str = re.findall(f"^领奖 .+ [0-9]+$", command)[0]
    msgSender: Member = message.author
    rolesBelongsToMember: List[Role] = msgSender.roles
    eventManagerRole = 896546278761189397
    if eventManagerRole not in rolesBelongsToMember:
        await message.channel.send("失败")
        return

    uuid = eventAwardManagement.newAward(db, userID, message.id, money, eventName)

    if uuid == '':
        msg = languageConfig['error']['dbError']
        await message.channel.send(msg)
        return

    msg = languageConfig['eventAward']['awardPublish'].replace('?@user', author.display_name)
    await message.channel.send(msg)
    await message.add_reaction(':game_die:')

