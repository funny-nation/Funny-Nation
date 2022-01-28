import json
from typing import List
from discord import Client, TextChannel, Guild, Member, message
from pymysql import Connection
import src.model.eventAwardManagement as eventAwardManagement
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.utils.readConfig import getLanguageConfig, getMajorConfig


async def getAward(self: Client, messageID: int, db: Connection, channelID: int, userID: int):
    languageConfig = getLanguageConfig()
    majorConfig = getMajorConfig()
    myGuild: Guild = self.guilds[0]
    user: Member = await myGuild.fetch_member(userID)
    channels: List[TextChannel] = myGuild.text_channels
    targetChannel: TextChannel or None = None
    for channel in channels:
        if channel.id == channelID:
            targetChannel = channel
            break
    Message = await targetChannel.fetch_message(messageID)
    AwardInfo = eventAwardManagement.getEventAward(db, messageID)
    ApprovedRecipient: dict = json.loads(AwardInfo[6])


    if AwardInfo is None:
        msg = languageConfig['eventAward']['AfterClose']
        await Message.channel.send(msg)
        return

    moneyAward: int = AwardInfo[3]
    dbResult = True
    dbResult = dbResult and addMoneyToUser(db, userID, moneyAward)
    dbResult = dbResult and addNewCashFlow(db, userID, moneyAward, majorConfig['cashFlowMessage']['getAward'])
    dbResult = dbResult and eventAwardManagement.editdRecipient(db, messageID, json.dumps(ApprovedRecipient))

    if not dbResult:
        msg = languageConfig['error']['dbError']
        await targetChannel.send(msg)
        return

    if userID in AwardInfo[6]:
        msg = languageConfig['eventAward']['alreadySent']
        await Message.channel.send(msg)
        return

    await targetChannel.send("you got it")

