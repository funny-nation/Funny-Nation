import json
from typing import List
from discord import Client, TextChannel, Guild, Member, message, DMChannel, RawReactionActionEvent, Role
from pymysql import Connection
import src.model.eventAwardManagement as eventAwardManagement
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.utils.readConfig import getLanguageConfig, getMajorConfig
from loguru import logger

async def approveAward(self: Client, event: RawReactionActionEvent, db: Connection, eventAdmin: dict):
    languageConfig = getLanguageConfig()
    myGuild: Guild = self.guilds[0]
    eventMSGID: int = event.message_id
    targetChannel: TextChannel or None = myGuild.get_channel(event.channel_id)
    userID: int = event.user_id
    user: Member = await myGuild.fetch_member(userID)
    rolesBelongsToMember: List[Role] = user.roles
    if eventAdmin['eventManger'] not in rolesBelongsToMember:
        msg = languageConfig['eventAward']['notEventAdmin'] \
            .replace('?@user_name', user.display_name)
        await targetChannel.send(msg)
        return

    recipientInfo = eventAwardManagement.searchRecipientsByPrivateMSGID(db, eventMSGID)
    event = eventAwardManagement.getEventAward(db, recipientInfo[0])
    manager: Member = await myGuild.fetch_member(event[0])
    managerDMChannel: DMChannel = await manager.create_dm()

    if event[4] == 1:
        msg = languageConfig['eventAward']['AfterClose']
        await managerDMChannel.send(msg)
        return

    if recipientInfo[3] == 2:
        msg = languageConfig['eventAward']['alreadySent']
        await managerDMChannel.send(msg)
        return

    if eventAwardManagement.approveRecipients(db, eventMSGID) is False:
        msg = languageConfig['error']['dbError']
        await targetChannel.send(msg)
        return

    money: int = event[2]
    recipient: Member = await myGuild.fetch_member(recipientInfo[1])
    recipientDMChannel: DMChannel = await recipient.create_dm()




    if recipientInfo[3] == 1:
        return

    if not addMoneyToUser(db, recipientInfo[1], money):
        logger.error(f"Cannot add money to user {recipientInfo[1]}")
        await managerDMChannel.send("error")
        return
    if not addNewCashFlow(db, recipientInfo[1], money, '领奖'):
        logger.error(f"Cannot create cash flow for user {recipientInfo[1]}")
        return

    msg = languageConfig['eventAward']['approveAward'] \
            .replace('?@user_name', recipient.display_name)
    await recipientDMChannel.send(msg)









