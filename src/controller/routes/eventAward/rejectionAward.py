from typing import List
from discord import Client, TextChannel, Guild, Member, message, DMChannel, RawReactionActionEvent, Role
from pymysql import Connection
import src.model.eventAwardManagement as eventAwardManagement
from src.utils.readConfig import getLanguageConfig, getMajorConfig
from loguru import logger

async def rejectAward(self: Client, event: RawReactionActionEvent, db: Connection, eventAdmin: dict):
    languageConfig = getLanguageConfig()
    myGuild: Guild = self.guilds[0]
    eventMSGID: int = event.message_id
    targetChannel: TextChannel or None = myGuild.get_channel(event.channel_id)
    userID: int = event.user_id
    user: Member = await myGuild.fetch_member(userID)
    rolesBelongsToMember: List[Role] = user.roles

    recipientInfo = eventAwardManagement.searchRecipientsByPrivateMSGID(db, eventMSGID)
    event = eventAwardManagement.getEventAward(db, recipientInfo[0])

    author: Member = await myGuild.fetch_member(event[0])
    recipient: Member = await myGuild.fetch_member(recipientInfo[1])
    recipientDMChannel: DMChannel = await recipient.create_dm()
    authorDMChannel: DMChannel = await author.create_dm()

    if eventAdmin['eventManger'] not in rolesBelongsToMember:
        msg = languageConfig['eventAward']['notEventAdmin'] \
            .replace('?@user_name', user.display_name)
        await targetChannel.send(msg)
        return


    if event[4] == 1:
        msg = languageConfig['eventAward']['AfterClose']
        await authorDMChannel.send(msg)
        return

    if recipientInfo[3] == 1:
        msg = languageConfig['eventAward']['alreadyReject']
        await authorDMChannel.send(msg)
        return

    if recipientInfo[3] == 2:
        return

    if eventAwardManagement.rejectRecipients(db, eventMSGID) is False:
        msg = languageConfig['error']['dbError']
        await targetChannel.send(msg)
        return

    msg = languageConfig['eventAward']['rejectionAdmain'] \
        .replace('?@user_name', recipient.display_name)
    await recipientDMChannel.send(msg)