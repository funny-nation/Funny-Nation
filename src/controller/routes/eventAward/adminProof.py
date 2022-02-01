from typing import List
from discord import User, DMChannel, Client, Member, Guild, Invite, TextChannel, RawReactionActionEvent, Message
import src.model.eventAwardManagement as eventAwardManagement
import json
from src.utils.readConfig import getLanguageConfig, getMajorConfig


async def adminProof(self: Client, db, event: RawReactionActionEvent):
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

    if eventAwardManagement.searchRecipientByEventIDandRecipientID(db, messageID, userID) is not None:
        msg = languageConfig['eventAward']['alreadyApply'] \
            .replace('?@user_name', user.display_name)
        await targetChannel.send(msg)
        return


    dmChannel: DMChannel = await user.create_dm()
    msg = languageConfig['eventAward']['Apply']
    privateMsg: Message = await dmChannel.send(msg)
    privateMsgID: int = privateMsg.id
    if eventAwardManagement.addRecipient(db, messageID, privateMsgID, userID) is False:
        msg = languageConfig['error']['dbError']
        await targetChannel.send(msg)
        return

    authorDM: DMChannel = await author.create_dm()
    authorPrivateMessage: Message = await authorDM.send(user.display_name)
    await authorPrivateMessage.add_reaction('⭕')
    await authorPrivateMessage.add_reaction('🚫')

