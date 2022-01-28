from typing import List
from discord import User, DMChannel, Client, Member, Guild, Invite
import src.model.eventAwardManagement as eventAwardManagement
import json


async def adminProof(self: Client, db, messageID: int, userID: int):
    AwardInfo = eventAwardManagement.getEventAward(db, messageID)
    involve: List = json.loads(AwardInfo[5])
    recepients = {}
    recepients['id'] = userID
    recepients['status'] = 0
    involve.append(json.dumps(recepients))
    myGuild: Guild = self.guilds[0]
    user: Member = await myGuild.fetch_member(userID)
    author: Member = await myGuild.fetch_member(messageID)
    dmChannel: DMChannel = await author.create_dm()
    msg = await dmChannel.fetch_message(messageID)
    await dmChannel.send(user.display_name)
    await msg.add_reaction('❌')
    await msg.add_reaction('⭕')
    return
