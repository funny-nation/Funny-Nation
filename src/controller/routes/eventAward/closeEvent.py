import json
from typing import List
from discord import Client, TextChannel, Guild, Member, Message, Role
from pymysql import Connection
import src.model.eventAwardManagement as eventAwardManagement
from src.utils.readConfig import getLanguageConfig, getMajorConfig
import re

async def closeEvent(self: Client, message: Message, db: Connection, messageID: int, eventAdmin: dict, command: str):
    languageConfig = getLanguageConfig()
    author = message.author.id
    eventName: str = re.findall(f"^关闭活动 (.+)$", command)[0]
    msgSender: Member = message.author
    myGuild: Guild = self.guilds[0]
    user: Member = await myGuild.fetch_member(author)
    rolesBelongsToMember: List[Role] = msgSender.roles
    if eventAdmin['admin'] not in rolesBelongsToMember:
        msg = languageConfig['eventAward']['notEventAdmin'] \
            .replace('?@user_name', user.display_name)
        await message.channel.send(msg)
        return


    eventAwardManagement.deletAwardByEventName(db, eventName)
    await message.channel.send(eventName + "活动关闭")