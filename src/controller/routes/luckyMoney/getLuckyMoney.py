from discord import Client, TextChannel, Guild
from pymysql import Connection
import src.model.luckyMoneyManagement as luckyMoneyManagement
from typing import List
import json


async def getLuckyMoney(self: Client, messageID: int, db: Connection, channelID: int, userID: int):

    myGuild: Guild = self.guilds[0]
    channels: List[TextChannel] = myGuild.text_channels
    targetChannel: TextChannel or None = None
    for channel in channels:
        if channel.id == channelID:
            targetChannel = channel
            break


    luckyMoneyInfo = luckyMoneyManagement.getLuckyMoney(db, messageID)

    if luckyMoneyInfo is None:
        await targetChannel.send("找不到红包")
        return

    if luckyMoneyInfo[3] == 0:
        await targetChannel.send("你来晚了，红包被抢完了")
        return

    whoTake: List = json.loads(luckyMoneyInfo[5])

    if userID in whoTake:
        await targetChannel.send("你已经拿了")
        return

    whoTake.append(userID)

    luckyMoneyManagement.editWhoTake(db, messageID, json.dumps(whoTake))

