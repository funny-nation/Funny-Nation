import json
from typing import List


from discord import Client, TextChannel, Guild, Member, Message, Role
from pymysql import Connection
import src.model.eventAwardManagement as eventAwardManagement
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.utils.readConfig import getLanguageConfig, getMajorConfig
import re

async def sendAward(self: Client, message: Message, db: Connection, money: int, userID: int, eventAdmin: dict, command: str):
    languageConfig = getLanguageConfig()
    author = message.author.id
    eventName: str = re.findall(f"^领奖 .+ [0-9]+$", command)[0]
    msgSender: Member = message.author
    myGuild: Guild = self.guilds[0]
    user: Member = await myGuild.fetch_member(author)
    rolesBelongsToMember: List[Role] = msgSender.roles
    print(rolesBelongsToMember)
    print(eventAdmin)
    if eventAdmin not in rolesBelongsToMember:
        msg = languageConfig['eventAward']['notEventAdmin'] \
            .replace('?@user_name', user.display_name)
        await message.channel.send(msg)
        return
    uuid = eventAwardManagement.newAward(db, userID, message.id, money, eventName)

    if uuid == '':
        msg = languageConfig['error']['dbError']
        await message.channel.send(msg)
        return

    if eventName in uuid[4]:
        msg = languageConfig['eventAward']['sameEvent'] \
            .replace('?@user_name', user.display_name)
        await message.channel.send(msg)
        return

    msg = languageConfig['eventAward']['awardPublish'] \
        .replace('?@user_name', user.display_name) \
        .replace('?@event_name', eventName)
    await message.channel.send(msg)
    await message.add_reaction('🎲')

