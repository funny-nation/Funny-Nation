from typing import List
from discord import User, DMChannel, Client, Member, Guild, Invite, TextChannel, RawReactionActionEvent, Message
import src.model.eventAwardManagement as eventAwardManagement
import json
from src.utils.readConfig import getLanguageConfig, getMajorConfig


async def applyForAward(self: Client, db, event: RawReactionActionEvent):
    '''

    :param event:
    :param self:
    :param db:
    :return:
    '''
    myGuild: Guild = self.guilds[0]
    languageConfig = getLanguageConfig()
    userID: int = event.user_id
    messageID: int = event.message_id
    user: Member = await myGuild.fetch_member(userID)
    channels: List[TextChannel] = myGuild.text_channels
    targetChannel: TextChannel or None = None
    for channel in channels:
        if channel.id == event.channel_id:
            targetChannel = channel
            break
    authorMSG = await targetChannel.fetch_message(messageID)
    author = authorMSG.author
    eventInfo = eventAwardManagement.getEventAward(db, messageID)

    if eventAwardManagement.searchRecipientByEventIDandRecipientID(db, messageID, userID) is not None:
        msg = languageConfig['eventAward']['alreadyApply'] \
            .replace('?@user_name', user.display_name)
        await targetChannel.send(msg)
        return


    dmChannel: DMChannel = await user.create_dm()

    if eventInfo[4] == 1:
        msg = languageConfig['eventAward']['AfterClose']
        await dmChannel.send(msg)
        return

    msg = languageConfig['eventAward']['Apply']
    await dmChannel.send(msg)


    msgForAuthor = languageConfig['eventAward']['tryGetAward'] \
        .replace('?@user_name', user.display_name)\
        .replace('?@event_name', eventInfo[3])\
        .replace('?@money', str(eventInfo[2] / 100))

    authorDM: DMChannel = await author.create_dm()
    authorPrivateMessage: Message = await authorDM.send(msgForAuthor)
    if eventAwardManagement.addRecipient(db, messageID, authorPrivateMessage.id, userID) is False:
        msg = languageConfig['error']['dbError']
        await targetChannel.send(msg)
        return
    await authorPrivateMessage.add_reaction('⭕')
    await authorPrivateMessage.add_reaction('🚫')

