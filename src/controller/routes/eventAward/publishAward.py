import json
from typing import List


from discord import Client, TextChannel, Guild, Member, Message, Role
from pymysql import Connection
import src.model.eventAwardManagement as eventAwardManagement
from src.utils.readConfig import getLanguageConfig, getMajorConfig
from loguru import logger
import re

async def publishAward(self: Client, message: Message, db: Connection, money: int, userID: int, eventAdmin: dict, command: str):
    languageConfig = getLanguageConfig()
    author = message.author.id
    eventName: str = re.findall(f"^领奖 (.+) [0-9]+$", command)[0]
    msgSender: Member = message.author
    myGuild: Guild = self.guilds[0]
    user: Member = await myGuild.fetch_member(author)
    rolesBelongsToMember: List[Role] = msgSender.roles
    if eventAdmin['eventManger'] not in rolesBelongsToMember:
        msg = languageConfig['eventAward']['notEventAdmin'] \
            .replace('?@user_name', user.display_name)
        await message.channel.send(msg)
        return
    awardInfo = eventAwardManagement.getEventAwardByName(db, eventName)
    if awardInfo is not None:
        msg = languageConfig['eventAward']['sameEvent'] \
            .replace('?@user_name', user.display_name)
        await message.channel.send(msg)
        return
    if not eventAwardManagement.newAward(db, author, message.id, money, eventName):
        msg = languageConfig['error']['dbError']
        await message.channel.send(msg)
        return

    msg = languageConfig['eventAward']['awardPublish'] \
        .replace('?@user_name', user.display_name) \
        .replace('?@event_name', eventName)
    await message.channel.send(msg)
    await message.add_reaction('🎲')

