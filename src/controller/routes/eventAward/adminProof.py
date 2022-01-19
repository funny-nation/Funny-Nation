import json
from typing import List
from discord import User, DMChannel, Client, Message, Member, Guild, Invite
from pymysql import Connection
from loguru import logger
from src.controller.routes.eventAward.getAward import getAward

async def adminProof(self:Client, message: Message, messageID: int, db: Connection, channelID: int, userID: int, involve: List):
    dmChannel: DMChannel = await Member.create_dm()
    for each in range(len(involve)):
        await dmChannel.send(involve[each])
        await message.add_reaction("alal")
    await getAward(self, message, messageID, db, channelID, userID)
