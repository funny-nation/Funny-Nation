import json
from typing import List
from discord import User, DMChannel, Client, Message, Member, Guild, Invite


async def adminProof(self:Client, messageID: int, involve: List):
    dmChannel: DMChannel = await Member.create_dm()
    msg = await dmChannel.fetch_message(messageID)
    for each in range(len(involve)):
        await dmChannel.send(involve[each])
        await msg.add_reaction('❌')
        await msg.add_reaction('⭕')
    return
