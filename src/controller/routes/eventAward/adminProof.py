import json
from typing import List
from discord import Client, TextChannel, Guild, Member, Message
from pymysql import Connection
from loguru import logger
from src.controller.routes.eventAward.getAward import getAward

def adminProof(self:Client, message: Message, messageID: int, db: Connection, channelID: int, userID: int, involve: List):
    for each in range(len(involve)):
        await involve[each]
        await message.add_reaction("alal")
    await getAward(self, message, messageID, db, channelID, userID)
