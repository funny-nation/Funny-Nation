import json
from typing import List
from discord import User, DMChannel, Client, Message, Member, Guild, Invite
from pymysql import Connection
from loguru import logger
from src.controller.routes.eventAward.getAward import getAward

async def adminProof(self:Client, message: Message, involve: List):
    dmChannel: DMChannel = await Member.create_dm()
    for each in range(len(involve)):
        await dmChannel.send(involve[each])
        await message.add_reaction("o")
        await message.add_reaction("x")
    return
