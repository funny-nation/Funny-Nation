from typing import List
from discord import User, DMChannel, Client, Member, Guild, Invite, TextChannel, RawReactionActionEvent
import src.model.eventAwardManagement as eventAwardManagement
import json


async def adminProof(self: Client, db, event: RawReactionActionEvent):
    '''

    :param event:
    :param self:
    :param db:
    :return:
    '''
    awardInfo = eventAwardManagement.getEventAward(db, event.message_id)
    involve: List = json.loads(awardInfo[5])
    recepients = {}
    recepients['id'] = event.message_id
    recepients['status'] = 0

    myGuild: Guild = self.guilds[0]
    user: Member = await myGuild.fetch_member(event.user_id)
    channel: TextChannel = myGuild.get_channel(event.channel_id)
    Message = await channel.fetch_message(event.message_id)
    author: Member = Message.author
    dmChannel: DMChannel = await author.create_dm()
    msg: Message = await dmChannel.send(user.display_name)
    recepients['msgID'] = msg.id
    involve.append(recepients)
    eventAwardManagement.editRecipient(db, awardInfo[2], json.dumps(involve))
    await msg.add_reaction('🚫')
    await msg.add_reaction('⭕')
    return
