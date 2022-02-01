import json
from typing import List
from discord import Client, TextChannel, Guild, Member, message, DMChannel, RawReactionActionEvent
from pymysql import Connection
import src.model.eventAwardManagement as eventAwardManagement
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.utils.readConfig import getLanguageConfig, getMajorConfig
from loguru import logger

async def getAward(self: Client, event: RawReactionActionEvent, db: Connection, channelID: int):
    languageConfig = getLanguageConfig()
    majorConfig = getMajorConfig()
    myGuild: Guild = self.guilds[0]
    awardInfo = eventAwardManagement.getEventAward(db, event.message_id)
    channel: TextChannel = myGuild.get_channel(channelID)
    print(awardInfo)
    # recipientID: int = awardInfo[5]['id']
    # user: Member = await myGuild.fetch_member(recipientID)


    # dmChannel: DMChannel = await user.create_dm()
    # msg = languageConfig['getAward']['getAward'] \
    #     .replace('?@user_name', user.display_name)
    #
    # if not addMoneyToUser(db, recipientID, awardInfo[4]):
    #     logger.error(f"Cannot add money to user {recipientID}")
    #     await channel.send("error")
    #     return
    # if not addNewCashFlow(db, recipientID, awardInfo[4], '活动'):
    #     logger.error(f"Cannot create cash flow for user {recipientID}")
    #     return
    #
    # await dmChannel.send(msg)



